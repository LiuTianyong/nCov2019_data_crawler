# -*- coding: utf-8 -*-
# @Author  : 刘天勇
# @Time    : 2020/2/13 19:07
# @Function:

import pymysql


class MySqlDB:
    def __init__(self,type='csv'):
        self.db = ''
        self.cursor = ''

        if type == 'db':
            # 数据库初始化
            self.db = pymysql.connect(host='127.0.0.1', port=3306, user='root', password='123456', db='covid_19')
            self.cursor = self.db.cursor()
        elif type == 'csv':
            pass
        else:
            print('保存类型有误')