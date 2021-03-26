# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import mysql.connector
import json
# from article_rep import article_represent
from .NCKH.article_rep_crawler import article_rep
# import keras
# from keras.layers import *
# from keras.models import Model
# from keras import backend as K
# from keras.optimizers import *
# from sklearn.metrics import roc_auc_score
# from keras.callbacks import ModelCheckpoint
# import tensorflow as tf
# import pickle


class VnexpresscrawlerPipeline:
    con = None
    cur = None
    tag_set = set()
    categories_set = set()

    def __init__(self):
        self.create_connection()
        self.cur.execute("""select tag from tags""")
        for tag in self.cur.fetchall():
            self.tag_set.add(tag[0])
        self.cur.execute("""select category from category""")
        for category in self.cur.fetchall():
            self.categories_set.add(category[0])

    def create_connection(self):
        self.con = mysql.connector.connect(
            host='localhost',
            user='root',
            passwd='1234',
            database='pnrec_database'
        )
        self.cur = self.con.cursor(buffered=True)

    def process_item(self, item, spider):
        self.save_article_to_db(item)
        self.save_tag_to_db(item['tags'])
        self.save_category_to_db(item['category'])
        self.save_article_tag_to_db(item['tags'], item['articleID'])
        self.save_article_category_to_db(
            item['category'], item['articleID'])
        print("Finish saving articles, article_tag, article_category to db")
        return item

    def save_tag_to_db(self, tag_list):

        for tag in tag_list:
            if tag in self.tag_set:
                continue
            else:
                self.tag_set.add(tag)
                self.cur.execute(
                    """insert into tags(tag) value('{}') on duplicate key update tag = tag""".format(tag))
                self.con.commit()

    def save_category_to_db(self, category_list):
        # data to categories
        for level, category in enumerate(category_list):
            if category in self.categories_set:
                continue
            else:
                self.categories_set.add(category)
                self.cur.execute("""insert into category(category, level) values (%s, %s)""", (
                    category, level
                ))
                self.con.commit()

    def save_article_tag_to_db(self, tag_list, articleID):
        for tag in tag_list:
            self.cur.execute(
                "select tagID from tags where tag='{}'".format(tag))
            tagID = self.cur.fetchone()
            if tagID == None:
                print("Encountered a None type")
                continue
            self.cur.execute("insert into article_tags(tagID, articleID) values({},{})".format(
                tagID[0], articleID))
            self.con.commit()

    def save_article_category_to_db(self, category_list, articleID):
        for category in category_list:
            self.cur.execute(
                "select categoryID from category where category='{}'".format(category))
            categoryID = self.cur.fetchone()
            if categoryID == None:
                print("Encountered a None type")
                continue
            self.cur.execute("insert into article_category(categoryID, articleID) values({},{})".format(
                categoryID[0], articleID))
            self.con.commit()

    def save_article_to_db(self, item):
        representation = (article_rep.article_represent(
            item['articleID'], item['sapo'], article_rep.modelExtractor))
        represent_json = json.dumps(representation.tolist())
        # test

        self.cur.execute(
            """insert into articles(articleID, link, content, time, title, displayContent, sapo, thumbnail, representation)
                    values ( %s, %s, %s, %s, %s, %s, %s, %s,%s)
                    on duplicate key update articleID = articleID""", (
                item['articleID'],
                item['link'],
                item['content'],
                item['time'],
                item['title'],
                item['displayContent'],
                item['sapo'],
                item['thumbnail'],
                represent_json
            ))
        self.con.commit()
