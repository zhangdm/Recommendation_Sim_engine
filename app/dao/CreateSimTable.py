#!/usr/bin/env python
# -*- coding:UTF-8 -*-


import sys
sys.path.append("./app")
import os
from utils import DBApi as DB
import subprocess
from utils.utils import getparam
import logging
logging.basicConfig(format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s', level=logging.INFO)

logger = logging.getLogger(__name__)



def createtable(configini):
	SimItemTable = getparam(configini,"hivetable","SimItemTable")


	logging.info(u"创建相似推荐结果表{SimItemTable}".format(SimItemTable=SimItemTable))
	sql = """
	CREATE TABLE IF NOT EXISTS {SimItemTable}(
	cid int COMMENT "物料ID",
	sim string COMMENT "相似物料集合"
	)PARTITIONED BY(scene_id int COMMENT "推荐场景ID",algorithm string COMMENT "算法名称",item_type string COMMENT "物料类型名称",version string COMMENT "数据版本",update_time string  COMMENT "更新时间") ROW FORMAT DELIMITED FIELDS TERMINATED BY '\001' LINES TERMINATED BY '\n' STORED AS textfile
	""".format(SimItemTable=SimItemTable)
	print(sql)
	DB.hive_exec(sql)




