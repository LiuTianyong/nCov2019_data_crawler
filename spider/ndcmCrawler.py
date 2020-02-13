# -*- coding: utf-8 -*-
# @Author  : 刘天勇
# @Time    : 2020/2/13 19:04
# @Function:

import requests
from spider.db import MySqlDB
import time
import csv
import pandas as pd
from spider.run_log import logger

headers = {
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.117 Safari/537.36'
}

save_path = 'spider/data/covid_patient_track.csv'


class NdcmCrawler:

    def __init__(self, type='csv'):
        # session初始化
        self.session = requests.session()
        # 增加请求头
        self.session.headers.update(headers)

        # 省级
        self.province = ''

        # 请求失败次数
        self.request_error_count = 0
        self.request_error_message = ''

        # 数据存储器初始化
        if type == 'db':
            self.mysql_db = MySqlDB(type)
            self.db = self.mysql_db.db
            self.cursor = self.mysql_db.cursor

            sql = 'truncate table covid_patient_track'
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
        provinces_dict = {'广东省': 'guangdong', '云南省': 'yunnan', '河南省': 'henan', '贵州省': 'guizhou', '四川省': 'sichuan',
                          '天津市': 'tianjin', '安徽省': 'anhui', '江西省': 'jiangxi', '河北省': 'hebei', '北京市': 'beijing',
                          '福建省': 'fujian', '浙江省': 'zhejiang', '江苏省': 'jiangsu', '山西省': 'shanxi', '吉林省': 'jilin',
                          '陕西省': 'shaanxi', '内蒙古': 'neimenggu', '山东省': 'shandong', '重庆市': 'chongqing',
                          '海南省': 'hainan', '湖南省': 'hunan', '辽宁省': 'liaoning', '甘肃省': 'gansu', '宁夏自治区': 'ningxia',
                          '上海市': 'shanghai', '广西省': 'guangxi', '黑龙江省': 'heilongjiang', '青海省': 'qinghai',
                          '湖北省': 'hubei'}

        for key in provinces_dict:
            province = provinces_dict[key]
            self.province = key
            self.request_patient_track(province)

        if self.save_type == 'csv':
            df = pd.read_csv(save_path)
            df.columns = ['city', 'district', 'street', 'place', 'location', 'remark', 'source', 'link', 'is_today',
                          'province']
            df.to_csv(save_path, index=False)

        self.logging.error(self.request_error_message)

    def request_patient_track(self, province):
        url_format = 'https://m.mp.oeeee.com/data/uploads/PneumoniaArea/json/all_{}.json'
        url = url_format.format(province)
        while True:
            try:
                res = self.session.get(url)
                res_json = res.json()

                if res_json['errcode'] == 0:
                    result = res_json['data']
                    self.save_patient_track(result)
                    self.request_error_count = 0
                    break
                else:
                    self.request_error_count += 1
                    if self.request_error_count > 5:
                        self.request_error_message = '连续五次失败，检查程序bug'
                    time.sleep(60)

            except Exception as e:
                self.request_error_message = e

    def save_patient_track(self, res):
        if self.save_type == 'db':
            for line in res:
                for district_ in line['districtList']:
                    for place in district_['placeList']:
                        place['province'] = self.province

                        cols = ", ".join('`{}`'.format(k) for k in place.keys())
                        val_cols = ', '.join('%({})s'.format(k) for k in place.keys())
                        sql = "insert into covid_patient_track(%s) values(%s)"
                        res_sql = sql % (cols, val_cols)
                        self.cursor.execute(res_sql, place)
                        self.db.commit()
                        # try:
                        #     self.cursor.execute(res_sql, place)
                        #     self.db.commit()
                        # except Exception as e:
                        #     self.request_error_message = e

        else:
            with open(self.save_path, 'a+', newline='', encoding='utf-8') as fp:
                writer = csv.writer(fp)
                for line in res:
                    for district_ in line['districtList']:
                        for place in district_['placeList']:
                            place['province'] = self.province
                            writer.writerow(place.values())


if __name__ == '__main__':
    ndcm_crawler = NdcmCrawler('csv')
    ndcm_crawler.run()
