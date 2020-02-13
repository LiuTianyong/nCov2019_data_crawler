# -*- coding: utf-8 -*-
# @Author  : 刘天勇
# @Time    : 2020/2/13 23:02
# @Function:
from datetime import datetime
import logging


date = datetime.now().strftime('%Y%m%d%H%M%S')
logging_path = 'spider/log/CrawlerRun_{}.log'.format(date)

logging.basicConfig(level=logging.INFO, filename=logging_path, format='%(asctime)s - %(message)s')
logger = logging.getLogger(__name__)