# -*- coding: utf-8 -*-
# @Author  : 刘天勇
# @Time    : 2020/2/12 19:39
# @Function:

from spider.dxyCrawler import DxyCrawler
from spider.ndcmCrawler import NdcmCrawler
import time

if __name__ == '__main__':
    # 保存类型 MySQL_DB / CSV  (db/csv)  默认：csv
    save_type = 'csv'
    dxy_crawler = DxyCrawler(save_type)
    ndcm_crawler = NdcmCrawler(save_type)

    while True:
        dxy_crawler.run()
        ndcm_crawler.run()
        print('完成一次')
        time.sleep(60 * 60)