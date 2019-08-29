# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
from czScrapy.config import *
from czScrapy.db_utils import *
import logging
from logging.config import fileConfig
from czScrapy.db_utils import *

class czScrapyPipeline(object):
    def process_item(self, item, spider):
        white_key = False
        black_key = True
        for keyword in KEYWORDS:
            if keyword in item["title"]:
                white_key = True

        for keyword in BLACK_LIST:
            if keyword in item["title"]:
                black_key = False

        if not white_key or not black_key:
            logging.info('标题不在白名单或者存在黑名单:%s' % id)
            return

            # 检查是否存在重复的通告
        if check_dup_record(item):
            logging.info('%s:%s已存在数据库中，忽略...' %(item.get('id'), item.get('title')))
            return;
        logging.info('新发现公告%s' % item.get('id'))
        if upsert_to_mongo({'id': item.get('id')}, item):
            logging.info('更新/插入[%s]成功' % item.get('id'))
        return item
