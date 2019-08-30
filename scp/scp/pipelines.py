# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import pymysql
from pymysql import cursors
from scp import settings
from twisted.enterprise import adbapi

class ScpPipeline(object):
    def __init__(self):
        # 连接数据库
        dbparams = {
            'host': settings.MYSQL_HOST,
            'port': 3306,
            'user': 'root',
            'password': settings.MYSQL_PASSWD,
            'database': settings.MYSQL_DBNAME,
            'charset': 'utf8',
            'cursorclass': cursors.DictCursor
        }
        self.dbpool = adbapi.ConnectionPool('pymysql', **dbparams)
        self._sql = None

    @property
    def sql(self):
        if not self._sql:
            self._sql = """insert into scp_table (name,content,imgs) value (%s,%s,%s)"""
            return self._sql
        return self._sql

    def process_item(self, item, spider):
        #对sql语句进行处理
        defer = self.dbpool.runInteraction(self.insert_item,item)  #执行函数insert_item 去插入数据
        defer.addErrback(self.handle_error, item, spider)            #遇到错误信息调用 handle_error方法

    def insert_item(self, cursor, item):
        cursor.execute(self.sql, (
            item['name'],
            item['content'],
            item['imgs']
        ))

    def handle_error(self, error, item, spider):
        print('=' * 20 + 'error' + '=' * 20)
        print(error)
        print('=' * 20 + 'error' + '=' * 20)


