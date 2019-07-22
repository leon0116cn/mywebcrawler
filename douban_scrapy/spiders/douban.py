# -*- coding: utf-8 -*-
import scrapy
from douban_scrapy.itemloaders import DoubanMovieTop250ItemLoader
from douban_scrapy.items import DoubanMoviesTop250Item


class DoubanMovieTop250Spider(scrapy.Spider):
    name = 'douban_movie_top250'
    allowed_domains = ['douban.com']
    start_urls = ['https://movie.douban.com/top250']

    def parse(self, response):
        for movie_item in response.xpath("//div[@class='item']"):
            movie_item_loader = DoubanMovieTop250ItemLoader(
                item=DoubanMoviesTop250Item(), selector=movie_item
            )
            movie_item_loader.add_xpath('movie_rank', "./div[@class='pic']/em/text()")
            movie_item_loader.add_xpath('image_urls', "./div[@class='pic']//img/@src")
            movie_item_loader.add_xpath('movie_name', ".//div[@class='hd']/a/span/text()")
            movie_item_loader.add_xpath('movie_detail', ".//div[@class='hd']/a/@href")
            movie_item_loader.add_xpath('rating_num', ".//div[@class='star']/span[@class='rating_num']/text()")
            movie_item_loader.add_xpath('comment_num', ".//div[@class='star']/span/text()", re=r"(\d+)人评价")
            movie_item_loader.add_xpath('quote', ".//div[@class='bd']/p[@class='quote']/span/text()")
            movie_item_loader.add_value('request_url', response.url)
            yield movie_item_loader.load_item()

        next_url = response.xpath(".//div[@class='paginator']//span[@class='next']/a/@href").get()
        if next_url is not None:
            yield response.follow(next_url, callback=self.parse)
