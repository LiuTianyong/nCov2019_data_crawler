# -*- coding: utf-8 -*-
# @Author  : 刘天勇
# @Time    : 2020/2/17 17:09
# @Function:
# @source：腾讯新闻

import requests
import re
import json
from spider.db import MySqlDB
from spider.run_log import logger
import csv
import time
import random
import pandas as pd

headers = {
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.117 Safari/537.36'
}

save_path = 'spider/data/covid_txnew_track.csv'


class PatientTrajectiory:

    def __init__(self, type='csv'):
        # session初始化
        self.session = requests.session()
        # 增加请求头
        self.session.headers.update(headers)

        # 请求失败次数
        self.request_error_count = 0
        self.request_error_message = ''

        # 数据存储器初始化
        if type == 'db':
            self.mysql_db = MySqlDB(type)
            self.db = self.mysql_db.db
            self.cursor = self.mysql_db.cursor

            sql = 'truncate table covid_txnew_track'
            self.cursor.execute(sql)
            self.db.commit()

        elif type == 'csv':
            self.save_path = save_path
        else:
            print('目前不支持你输入的保存类型')

        # 保存类型
        self.save_type = type

        # 日志初始化
        self.logging = logger

    def run(self):
        url_format = 'https://pacaio.match.qq.com/virus/trackList?page={}&num=10&&callback=__jp{}'
        for i in range(99999):
            while True:
                try:
                    url = url_format.format(i, i + 1)
                    res = self.session.get(url)

                    res_json = res.text.replace('__jp{}('.format(i + 1), '')
                    result = json.loads(res_json[:-1])
                    if len(result['data']['list']) == 0:
                        break

                    if result['code'] == 0:
                        self.save_data(result)
                        self.request_error_count = 0
                        time.sleep(random.randrange(1, 3))
                        break
                    else:
                        self.request_error_count += 1
                        if self.request_error_count > 5:
                            self.request_error_message = '连续五次失败，检查程序bug'
                        time.sleep(60)

                except Exception as e:
                    self.request_error_message = e

        if self.save_type == 'csv':
            df = pd.read_csv(save_path)
            df.columns = ['confid', 'province', 'city', 'county', 'location', 'user_num', 'user_name', 'other_info',
                          'track', 'target', 'pub_time', 'source', 'source_url', 'contact', 'contact_detail', 'hashtag',
                          'lasttime'
                          ]
            df.to_csv(save_path, index=False)

        self.logging.error(self.request_error_message)

    def save_data(self, result):
        if self.save_type == 'db':
            for line in result['data']['list']:
                cols = ", ".join('`{}`'.format(k) for k in line.keys())
                val_cols = ', '.join('%({})s'.format(k) for k in line.keys())
                sql = "insert into covid_txnew_track(%s) values(%s)"
                res_sql = sql % (cols, val_cols)
                self.cursor.execute(res_sql, line)
                self.db.commit()

        else:
            with open(self.save_path, 'a+', newline='', encoding='utf-8') as fp:
                writer = csv.writer(fp)
                for line in result['data']['list']:
                    writer.writerow(line.values())


if __name__ == '__main__':
    patient_trajectiory = PatientTrajectiory()
    patient_trajectiory.run()
