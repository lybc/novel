# -*- coding: utf-8 -*-
import scrapy
from novel.models import *
from novel.items import NovelItem
from urllib.parse import urlparse


class ZwduSpider(scrapy.Spider):
    name = 'zwdu'
    allowed_domains = ['www.zwdu.com']

    base_url = 'http://www.zwdu.com'
        
    def start_requests(self):
        for n in Novel.select():
            request = scrapy.Request(url=n.source_url, callback=self.parse)
            request.meta['novel'] = n
            yield request


    def parse(self, response):
        '''
        获取所有小说章节，与已存在的章节取差集,得到新章节
        '''
        all_chapter_urls = response.selector.xpath('//*[@id="list"]/dl/dd/a/@href').extract()
        novel = response.meta['novel']
        exsit_chapter_urls = [chapter.source_url for chapter in Chapter.select().where(Chapter.novel_id == novel.id)]
        new_chapter_urls = list(set(all_chapter_urls).difference(set(exsit_chapter_urls)))
        for chapter_url in new_chapter_urls:
            yield scrapy.Request(
                url=self.base_url + chapter_url, 
                callback=self.process_content,
                meta=response.meta
            )
        pass
    
    def process_content(self, response):
        novel = response.meta['novel']
        rs = urlparse(response.url)
        item = NovelItem()
        item['title'] = response.selector.xpath('//div[@class="bookname"]/h1/text()').extract()[0]
        item['content'] = response.selector.xpath('//div[@id="content"]/text()').extract()
        item['novel_id'] = novel.id
        item['chapter_source_url'] = rs.path
        return item