#!/usr/bin/env python
# -*- coding:UTF-8 -*-


"""
从特征物料库中获取数据
"""

import sys
sys.path.append("./app")
from utils import DBApi as DB
import numpy as np
from scipy.sparse import csc_matrix
import pandas as pd
import configparser
import time
import os
from utils.utils import getparam
import logging
logging.basicConfig(format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s', level=logging.INFO)

logger = logging.getLogger(__name__)


# curpath = os.path.dirname(os.path.realpath(__file__))
# abspath = os.path.abspath(os.path.join(os.path.dirname(__file__),"../.."))
# cfgpath = os.path.join(abspath,"config_dev.ini")




def getAllFeatureData(configini):
	feaTable = getparam(configini,"hivetable","featables")
	invalidatetable = "invalidate metadata {feaTable}".format(feaTable=feaTable)
	print(invalidatetable)
	DB.impala_exec(invalidatetable)
	time.sleep(15)

	print(feaTable)
	sql = """
	select 
		cid,
		features
	from
		{feaTable}
	order by
		cid asc
	""".format(feaTable=feaTable)
	print(sql)
	df = DB.impala_query(sql)
	
	ID = list(df['cid'].values)
	features = df['features']

	return ID,features