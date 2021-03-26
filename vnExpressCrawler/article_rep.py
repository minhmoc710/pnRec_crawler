'''
# requirements:
pip install vncorenlp
pip install keras 
pip install pickle

'''
import json
import mysql.connector
from vncorenlp import VnCoreNLP
import tensorflow as tf
from keras.callbacks import ModelCheckpoint
from sklearn.metrics import roc_auc_score
from keras.optimizers import *
from keras import backend as K
from keras.models import Model
from keras.layers import *
import keras
import os
import numpy as np
import pickle
print("still work up until here")
# import torch
os.environ["CUDA_VISIBLE_DEVICES"] = "0"


# load word_dict
file = open('NCKH\\article_rep_crawler\\phobert_news_preprocess.pkl', 'rb')
word_dict, news_words, news_index, news = pickle.load(file)
file.close()

# load modelExtractor
modelExtractor = keras.models.load_model(
    'NCKH\\article_rep_crawler\\new_embedding_extractor')

# load vncorenlp
VnCoreNLP_jar_file = 'NCKH/article_rep_crawler/vncorenlp/VnCoreNLP-1.1.1.jar'
rdrsegmenter = VnCoreNLP(VnCoreNLP_jar_file, annotators='wseg')


def news_word2index(word_dict, sapo):
    news_tokenizer = rdrsegmenter.tokenize(sapo)[0]

    word_id = []
    for word in news_tokenizer:  # quét các tokens
        if word in word_dict:
            word_id.append(word_dict[word][0])
    word_id = word_id[:30]  # lấy word_id của article (embedd)
    news_words = (word_id + [0]*(30-len(word_id)))  # max 30 tokens, <30 cho =0

    return news_words


def article_represent(articleID, sapo, modelExtractor):
    article_sapo = sapo
    print(article_sapo)
    sapo_index = news_word2index(word_dict, article_sapo)

    article = np.array([sapo_index], dtype='int32')
    print(article.shape)

    represent = modelExtractor.predict(article)

    return represent


# sapo_test = 'Trung vệ Leonardo Bonucci tiết lộ Cristiano Ronaldo rất phấn khích trước lượt về vòng 1/8 Champions League với Porto.'
# reprentation = article_represent(
#     2207856, "Ngoài nguyên nhân uống rượu-bia hay cố tình bỏ chạy, đôi khi chỉ vì không quen xe, lần đầu lái số tự động hay bực dọc với người khác.", modelExtractor)
# representation = (article_represent(
#     2207856, sapo_test, modelExtractor))

# represent_json = json.dumps(representation.tolist())
# test
# rep_convert = json.loads(represent_json)
# rep_convert = np.array(rep_convert, dtype='float32').reshape(1, 30, 768)
# print(rep_convert.shape)
# con = mysql.connector.connect(
#     host='localhost',
#     user='root',
#     passwd='1234',
#     database='pnrec'
# )
# cur = con.cursor(buffered=True)

# cur.execute("insert into articles (representation, articleID) value(%s, %s)", (
#     str(reprentation.tobytes()), 2207446))
# con.commit()
