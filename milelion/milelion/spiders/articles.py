import os

import scrapy
from bs4 import BeautifulSoup

from milelion.items import MilelionArticle


class ArticlesSpider(scrapy.Spider):
    name = "articles"
    allowed_domains = ["milelion.com"]

    def start_requests(self):
        urls = [
            "https://milelion.com/blog/",
        ]
        for i in range(2, int(os.getenv('MAX_PAGES', 24))):
            urls.append(f"https://milelion.com/blog/page/{i}/")
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse_list)

    def parse_list(self, response):
        soup = BeautifulSoup(response.text, 'html5lib')
        article_list = soup.find("div", class_="tdi_78")
        for link in article_list.find_all("a", class_="td-image-wrap"):
            yield scrapy.Request(url=link['href'], callback=self.parse)

    def parse(self, response, **kwargs):
        url = response.url
        soup = BeautifulSoup(response.text, 'html5lib')
        time_tag = soup.find('time')
        pub_date = time_tag['datetime']
        post = soup.find('div', class_="td-post-content")
        title_tag = soup.find('meta', property="og:title")
        title = title_tag['content'].split("-")[0]
        summary_tag = soup.find('meta', property="og:description")
        yield MilelionArticle(summary=summary_tag['content'], date_pub=pub_date, text=post.div.text, title=title)
