# -*- coding: utf-8 -*-
import scrapy


class ZwduSpider(scrapy.Spider):
    name = 'zwdu'
    allowed_domains = ['www.zwdu.com']
    start_urls = ['http://www.zwdu.com/book/13587/']

    base_url = 'http://www.zwdu.com'
        

    def parse(self, response):
        articles = response.selector.xpath('//*[@id="list"]/dl/dd/a/@href').extract()
        for article in articles:
            yield scrapy.Request(
                url=self.base_url + article, 
                callback=self.write_file, 
            )
        pass
    
    def write_file(self, response):
        article_title = response.selector.xpath('//div[@class="bookname"]/h1/text()').extract()[0]
        artical_content = response.selector.xpath('//div[@id="content"]/text()').extract()
        f = open('cswmsd.txt','a')
        f.write(article_title + '\n\n\n')
        for item in artical_content:
            f.write(item + '\n')
        f.close()
        
