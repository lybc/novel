# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from peewee import MySQLDatabase
from novel.models import Chapter
from json import *

class NovelPipeline(object):
    allow_chinese_digitals = ['零', '一', '二', '三', '四', '五', '六', '七', '八', '九', '十', '百', '千']
    chs_arabic_map = {
        u'零':0, 
        u'一':1, 
        u'二':2, 
        u'三':3, 
        u'四':4,
        u'五':5, 
        u'六':6,
        u'七':7, 
        u'八':8, 
        u'九':9,
        u'十':10, 
        u'百':100, 
        u'千':10 ** 3, 
        u'万':10 ** 4,
    }
        # u'〇':0, u'壹':1, u'贰':2, u'叁':3, u'肆':4,
        # u'伍':5, u'陆':6, u'柒':7, u'捌':8, u'玖':9,
        # u'拾':10, u'佰':100, u'仟':10 ** 3, u'萬':10 ** 4,
        # u'亿':10 ** 8, u'億':10 ** 8, u'幺': 1,
        # u'０':0, u'１':1, u'２':2, u'３':3, u'４':4,
        # u'５':5, u'６':6, u'７':7, u'８':8, u'９':9}

    def process_item(self, item, spider):
        # item['chapter_num'] = self.parseChineseDigital(item['title'])

        for index, paragraph in enumerate(item['content']):
            paragraph.replace('\xa0', '')
            item['content'][index] = paragraph
        
        chapter = Chapter(
            title=item['title'],
            content=dumps(item['content']),
            seq=int(item['chapter_source_url'].split('/')[-1].split('.')[0]),
            novel_id=item['novel_id'],
            source_url=item['chapter_source_url']
        )
        chapter.save()
        return item

    def parseChineseDigital(self, digital):
        result  = 0
        tmp     = 0
        hnd_mln = 0
        for count in range(len(digital)):
            if digital[count] not in self.allow_chinese_digitals: continue
            curr_digit = self.chs_arabic_map.get(digital[count])
            if curr_digit == 10 ** 8:
                result  = result + tmp
                result  = result * curr_digit
                # get result before 「亿」 and store it into hnd_mln
                # reset `result`
                hnd_mln = hnd_mln * 10 ** 8 + result
                result  = 0
                tmp     = 0
            # meet 「万」 or 「萬」
            elif curr_digit == 10 ** 4:
                result = result + tmp
                result = result * curr_digit
                tmp    = 0
            # meet 「十」, 「百」, 「千」 or their traditional version
            elif curr_digit >= 10:
                tmp    = 1 if tmp == 0 else tmp
                result = result + curr_digit * tmp
                tmp    = 0
            # meet single digit
            elif curr_digit is not None:
                tmp = tmp * 10 + curr_digit
            else:
                return result
        result = result + tmp
        result = result + hnd_mln
        return result
        pass
