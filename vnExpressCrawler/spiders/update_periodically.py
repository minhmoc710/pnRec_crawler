import scrapy
from bs4 import BeautifulSoup
from ..items import ArticleItem
import mysql.connector

NEWS_ARTICLE = 'article'


class UpdatePeriodicallySpider(scrapy.Spider):
    name = 'update_periodically'
    allowed_domains = ['vnexpress.net']
    start_urls = [
        'https://vnexpress.net/tin-tuc-24h']
    def parse(self, response):
        for link in response.css(".title-news a::attr(href)").getall():
             yield scrapy.Request(url=link, callback=self.parse_article)
    def parse_article(self, response):
        website_type = response.css(
            "meta[name='tt_page_type']::attr(content)").get()
        if website_type == NEWS_ARTICLE:
            objectid = response.css(
                "meta[name='tt_article_id']::attr(content)").get()
            article_items = ArticleItem()
            article_items['articleID'] = objectid
            article_items['content'] = " ".join(response.css(
                ".Normal ::text, .description ::text").getall())
            article_items['tags'] = response.css(
                "meta[name='its_tag'] ::attr(content)").extract()[0].split(", ")
            article_items['title'] = response.css(
                "meta[property='og:title']::attr(content)").get()
            article_items['time'] = response.css(
                "meta[name='its_publication'] ::attr(content)").get()
            article_items['link'] = response.url
            article_items['category'] = response.css(
                "meta[name='its_subsection']::attr(content)").get().split(", ")
            # article_items['displayContent'] = response.css(".fck_detail").get()
            article_items['displayContent'] = self.clean_html(
                response.css(".fck_detail").get())
            article_items['sapo'] = response.css(
                "meta[itemprop='description']::attr(content)").get()
            article_items['thumbnail'] = response.css(
                "meta[itemprop='thumbnailUrl']::attr(content)").get()
            yield article_items

    def clean_html(self, html_code):
        # clean html code for
        soup = BeautifulSoup(html_code, 'html.parser')
        # remove all styles, name, id
        for tag in soup():
            for attribute in ["style", "name", "id"]:
                del tag[attribute]
        images = soup.findAll('img')

        # make image visible if it is not
        for img in images:
            if img.has_attr('src') and img.has_attr('data-src'):
                if "data:image" in img['src']:
                    img['src'] = img['data-src']
                    del img['data-src']
        # remove all svg
        for s in soup.select('svg'):
            s.extract()
        # remove links under the articles if there is any
        for s in soup.select("ul[data-campaign='Box-Related']"):
            s.extract()
        # make give author name a class = right
        try:
            soup.find('strong')['class'] = 'right'
        except:
            print("except nothing at all")
        return str(soup).replace('\n', '')
