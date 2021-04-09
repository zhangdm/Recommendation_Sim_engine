#!/usr/bin/env python
# -*- coding:UTF-8 -*-
import sys
sys.path.append("./app")
import codecs
from utils import utils
import os
import collections
import json
import jieba
import time
import subprocess
from utils.utils import getparam
import logging
logging.basicConfig(format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s', level=logging.INFO)

logger = logging.getLogger(__name__)


def put_sim_to_hdfs(configini,itemHdfsPath,itemLocalPath,scene_id,item_type):
	"""
	file:存放特征数据的文件，是txt文件
	item_type:分为文章和视频两种类型，用article表示文章，video表示视频
	algorithm:算法，表示表示生成特征的算法
	"""
	import time
	update_time = time.strftime("%Y-%m-%d %H:%M:%S")
	hdfspath = getparam(configini,"hdfspath","hdfspath")
	# SimDataVideoPath = getparam(configini,"data_path","SimDataVideoPath")
	# VideoHdfsPath = getparam(configini,"hdfspath","VideoHdfsPath")

	algorithm = getparam(configini,"algorithm_param","algorithm")
	# SimDataVideoFile = getparam(configini,"data_path","SimDataVideoFile")
	SimItemTable = getparam(configini,"hivetable","SimItemTable")
	version = getparam(configini,"algorithm_param","version")

	rescode = utils.put_to_hdfs(hdfspath,itemHdfsPath,itemLocalPath)
	logging.info(u"将{itemLocalPath}上传到{itemHdfsPath}的状态码为{rescode}".format(itemLocalPath=itemLocalPath,itemHdfsPath=itemHdfsPath,rescode=rescode))

	logging.info(u"将数据从HDFS加载到hive表中")

	rescode = utils.load_data_into_hdfs(itemHdfsPath,SimItemTable,scene_id,algorithm,item_type,version,update_time)
	logging.info(u"将{itemHdfsPath}从HDFS加载到hive表{SimItemTable}中状态码为{rescode}".format(itemHdfsPath=itemHdfsPath,SimItemTable=SimItemTable,rescode=rescode))