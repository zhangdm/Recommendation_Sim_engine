#!/usr/bin/env python
# -*- coding:UTF-8 -*-

"""
从特征引擎得到特征向量，根据规则，保留与每个物料匹配的Top N类型

"""

import sys
sys.path.append("./app")
import pickle
import os
import codecs
import re
import jieba
from six import iteritems
import collections
from utils import utils
import json
import logging
import re
import time
from .FecthData import *
from .CalSim import *
from .TextToHive import *
from .CreateSimTable import *
from utils.utils import getparam,GetOfflineItemId,GetDiffTypeItem,deal_ini
logging.basicConfig(format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s', level=logging.INFO)

logger = logging.getLogger(__name__)



def CalSimToText(configini):
	"""

	"""
	logging.info(u"创建表")
	createtable(configini)


	logging.info(u"开始执行")
	ID,features = getAllFeatureData(configini)

	logging.info(u"计算相似度")
	Lsi_sims = calsim(configini,features)


	logging.info(u"获取物料数据表")
	item_table = getparam(configini,"db_info","item_table")

	algorithm_res_path = getparam(configini,"data_path","algorithm_res_path")

	logging.info(u"mysql数据库配置信息")
	HOST = getparam(configini,"db_info","HOST")
	USER = getparam(configini,"db_info","USER")
	PASSWORD = getparam(configini,"db_info","PASSWORD")
	DB = getparam(configini,"db_info","DB")
	PORT = getparam(configini,"db_info","PORT")

	logging.info(u"获取已下线文章ID")
	offlineItemID = GetOfflineItemId(HOST,USER,PASSWORD,DB,PORT,item_table)

	logging.info(u"获取相似配置信息")
	# itemName = deal_ini(getparam(configini,"sim","itemName"))   # 物料类型名称
	itemName = getparam(configini,"sim","itemName").split(":::")

	matchItem = deal_ini(getparam(configini,"sim","matchItem"))  # 物料名称

	logging.info(u"本地路径")
	# itemFilePath = deal_ini(getparam(configini,"sim","itemFilePath"))
	itemFilePath = getparam(configini,"sim","itemFilePath").split(":::")

	logging.info(u"保留前N个最相似的物料")
	simLen = deal_ini(getparam(configini,"sim","simLen"))
	logging.info(u"相似度结果数据存放的HDFS目录")
	# itemHdfsPath = deal_ini(getparam(configini,"sim","itemHdfsPath"))
	itemHdfsPath = getparam(configini,"sim","itemHdfsPath").split(":::")


	logging.info(u"相似度匹配关系类型个数")
	ItemTypeLen = getparam(configini,"sim","ItemTypeLen").split(":::")

	logging.info(u"场景类型ID")
	scene_id_all=getparam(configini,"sim","scene_id").split(":::")



	# 创建多级目录
	if not os.path.exists(os.path.join(os.getcwd(),algorithm_res_path)):
		os.makedirs(os.path.join(os.getcwd(),algorithm_res_path)) 

	# 清空本地文件
	for path_index,_ in enumerate(itemFilePath):
		if os.path.exists(itemFilePath[path_index]):
			os.remove(itemFilePath[path_index])


	for scene_index,scene_id in enumerate(scene_id_all):
		if len(scene_id) > 1:
			for itemindex,signal_matchItem in enumerate(matchItem[scene_index]):
				temp = signal_matchItem.split(":")
				N = int(simLen[scene_index][itemindex])

				matchItemid_key = GetDiffTypeItem(HOST,USER,PASSWORD,DB,PORT,temp[0],item_table)   # 待匹配类型的物料ID
				matchItemid_value = GetDiffTypeItem(HOST,USER,PASSWORD,DB,PORT,temp[1],item_table)   # 被匹配类型的物料ID

				# 文章
				with open(itemFilePath[scene_index],"a+") as f:

					for index,lsi_sim_list in enumerate(Lsi_sims):
						# 在待匹配ID中，且物料没有下线
						if ID[index] in matchItemid_key and ID[index] not in offlineItemID:
							lsi_sim_sorted = sorted(enumerate(lsi_sim_list),key=lambda item:item[1],reverse=True)


							lsi_sim_doc_all = {}

							count_index = 0
							for count,value in enumerate(lsi_sim_sorted):
								lsi_sim_doc={}

								# count=0表示自己，在被匹配物料ID中，且物料没有下线
								if ID[index] != ID[value[0]] and count_index <= N and int(ID[value[0]]) in matchItemid_value and int(ID[value[0]]) not in offlineItemID: # 去掉自己本身，此处添加想匹配的物料ID
									lsi_sim_doc[str(ID[value[0]])] = round(float(value[1]),8)
									lsi_sim_doc_all.update(lsi_sim_doc)
									count_index += 1


							LineValue = str(ID[index]) + "\001" + json.dumps(lsi_sim_doc_all) + "\n"
							f.write(LineValue)



			# 将数据存入HDFS目录中，并写入hive表中
			put_sim_to_hdfs(configini,itemHdfsPath=itemHdfsPath[scene_index],itemLocalPath=itemFilePath[scene_index],scene_id=scene_id,item_type=itemName[scene_index])