# -*- coding: utf-8 -*-
# @Author  : 刘天勇
# @Time    : 2020/2/12 19:43
# @Function:


import requests
import time
from spider.run_log import logger
from spider.db import MySqlDB

try:
    import pymysql
    import csv
except:
    import csv
import re

headers = {
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.117 Safari/537.36'
}

save_path = ['spider/data/covid_news.csv', 'spider/data/covid_virus_trip.csv', 'spider/data/covid_rumor.csv']


class DxyCrawler:
    def __init__(self, type='csv'):
        # session初始化
        self.session = requests.session()
        # 增加请求头
        self.session.headers.update(headers)

        # 数据量用于监视
        self.data_count = []

        # 请求失败次数
        self.request_error_count = 0
        self.request_error_message = ''

        # 数据初始化
        self.mysql_db = MySqlDB(type)
        self.db = self.mysql_db.db
        self.cursor = self.mysql_db.cursor

        # 保存类型
        self.save_type = type

        # 日志初始化
        self.logging = logger

    # 新闻采集
    def run(self):
        self.request_news()
        self.request_virus_trip()
        self.request_rumor()
        self.logging.error(self.request_error_message)

    def request_rumor(self):
        while True:
            try:
                res = requests.get('https://file1.dxycdn.com/2020/0130/454/3393874921745912507-115.json')
                res_json = res.json()
                if res_json['code'] == 'success':
                    result = res_json['data']
                    self.save_rumor(result)
                    self.request_error_count = 0
                    break
                else:
                    self.request_error_count += 1
                    if self.request_error_count > 5:
                        self.request_error_message = '连续五次失败，检查程序bug'
                    time.sleep(60)
            except Exception as e:
                self.request_error_message = e

    def save_rumor(self, res):
        if self.save_type == 'db':
            sql = 'truncate table covid_rumor'
            self.cursor.execute(sql)
            self.db.commit()
            for line in res:
                line['rumor_id'] = line.pop('id')
                cols = ", ".join('`{}`'.format(k) for k in line.keys())
                val_cols = ', '.join('%({})s'.format(k) for k in line.keys())
                sql = "insert into covid_rumor(%s) values(%s)"
                res_sql = sql % (cols, val_cols)
                try:
                    self.cursor.execute(res_sql, line)
                    self.db.commit()
                except Exception as e:
                    self.request_error_message = e
        else:
            with open(save_path[2], 'a+', newline='', encoding='utf-8') as fp:
                writer = csv.writer(fp)
                writer.writerow(res[0].keys())
                for line in res:
                    writer.writerow(line.values())

    def save_news(self, res):
        if self.save_type == 'db':
            sql = 'truncate table covid_news'
            self.cursor.execute(sql)
            self.db.commit()
            for line in res:
                line['new_id'] = line.pop('id')
                cols = ", ".join('`{}`'.format(k) for k in line.keys())
                val_cols = ', '.join('%({})s'.format(k) for k in line.keys())
                sql = "insert into covid_news(%s) values(%s)"
                res_sql = sql % (cols, val_cols)
                try:
                    self.cursor.execute(res_sql, line)
                    self.db.commit()
                except Exception as e:
                    self.request_error_message = e
        else:
            with open(save_path[0], 'a+', newline='', encoding='utf-8') as fp:
                writer = csv.writer(fp)
                writer.writerow(res[0].keys())
                for line in res:
                    writer.writerow(line.values())

    def save_virus_trip(self, res):
        if self.save_type == 'db':
            sql = 'truncate table covid_virus_trip'
            self.cursor.execute(sql)
            self.db.commit()

            for line in res:
                line['virus_trip_id'] = line.pop('id')
                cols = ", ".join('`{}`'.format(k) for k in line.keys())
                val_cols = ', '.join('%({})s'.format(k) for k in line.keys())
                sql = "insert into covid_virus_trip(%s) values(%s)"
                res_sql = sql % (cols, val_cols)
                try:
                    self.cursor.execute(res_sql, line)
                    self.db.commit()
                except Exception as e:
                    self.request_error_message = e
        else:
            with open(save_path[1], 'a+', newline='', encoding='utf-8') as fp:
                writer = csv.writer(fp)
                writer.writerow(res[0].keys())
                for line in res:
                    writer.writerow(line.values())

    def request_news(self):
        while True:
            try:
                res = self.session.get('https://file1.dxycdn.com/2020/0130/492/3393874921745912795-115.json')
                res_json = res.json()
                if res_json['code'] == 'success':
                    result = res_json['data']
                    self.save_news(result)
                    self.request_error_count = 0
                    break
                else:
                    self.request_error_count += 1
                    if self.request_error_count > 5:
                        self.request_error_message = '连续五次失败，检查程序bug'
                    time.sleep(60)
            except Exception as e:
                self.request_error_message = e

    def request_virus_trip(self):
        while True:
            try:
                res = self.session.get('https://2019ncov.133.cn/virus-trip/list')
                res_json = res.json()

                if res_json['code'] == 1:
                    result = res_json['data']['list']
                    self.save_virus_trip(result)
                    self.request_error_count = 0
                    break
                else:
                    self.request_error_count += 1
                    if self.request_error_count > 5:
                        self.request_error_message = '连续五次失败，检查程序bug'
                    time.sleep(60)
            except Exception as e:
                self.request_error_message = e


if __name__ == '__main__':
    # 保存类型 MySQL_DB / CSV  (db/csv)  默认：csv
    save_type = 'db'
    dxy_crawler = DxyCrawler(save_type)
    dxy_crawler.run()
