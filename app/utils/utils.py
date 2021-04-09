#!/usr/bin/env python
# -*- coding:UTF-8 -*-

import sys
sys.path.append("./app")
import codecs
import os
import json
import jieba
import pymysql
import pymysql.cursors
import time
import subprocess
import logging
logging.basicConfig(format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s', level=logging.INFO)

logger = logging.getLogger(__name__)


def compose_vec(Lsivec,LabelClassList,LabelClass_index):
	print(len(LabelClassList))
	for index in range(len(LabelClassList)):
		label_dict = {}
		for labelclass in LabelClassList[index]:
			if labelclass in LabelClass_index:
				indexlabelclass = 10000 + LabelClass_index[labelclass]
				

				label_dict[indexlabelclass] = 1

		Lsivec[index].extend(list(label_dict.items()))


	return Lsivec


def getini(configini):
	configini = str(configini)
	import os
	import configparser
	curpath = os.path.dirname(os.path.realpath(__file__))
	abspath = os.path.abspath(os.path.join(os.path.dirname(__file__),"../.."))
	cfgpath = os.path.join(abspath,configini)

	conf = configparser.ConfigParser()
	conf.read(cfgpath,encoding="utf-8")

	return conf

def getparam(configini,configsec,configname):
	"""
	configini:表示文件名
	configsec:ini配置文件中的项目名
	configname:某个项目的子项的名称
	"""

	conf = getini(configini)
	res = conf.get(configsec,configname)

	return res



def mkdir_hdfs(hdfspath):
	"""
	创建HDFS目录，包括多级目录
	"""
	command_mkdir = """
	hadoop fs -mkdir -p {hdfspath}
	""".format(hdfspath=hdfspath)
	print(command_mkdir)
	p = subprocess.Popen(command_mkdir,shell=True)
	rescode = p.wait()

	return rescode


def put_to_hdfs(hdfspath,hdfsfile,localfile):
	logging.info(u"创建目录{hdfspath}".format(hdfspath=hdfspath))
	command = """
	hadoop fs -mkdir -p {hdfspath}
	""".format(hdfspath=hdfspath)
	print(command)
	
	p = subprocess.Popen(command,shell=True)
	code = p.wait()

	logging.info(u"创建目录{hdfspath}的状态码为{code}".format(hdfspath=hdfspath,code=code))

	logging.info(u"上传文件到HDFS")
	command = """
	hadoop fs -put -f {localfile} {hdfsfile}
	""".format(hdfsfile=hdfsfile,localfile=localfile)
	p = subprocess.Popen(command,shell=True)
	out3 = p.wait()

	return out3



def load_data_into_hdfs(hdfsfile,hivetable,scene_id,algorithm,item_type,version,update_time):
	"""
	将数据从本地load到hdfs目录中
	"""
	command_to_table="""
	/usr/local/bin/h2cmd -e "load data inpath '{hdfsfile}' overwrite into table {hivetable} partition(scene_id={scene_id},algorithm='{algorithm}',item_type='{item_type}',version='{version}',update_time= '{update_time}')"
	""".format(hdfsfile=hdfsfile,hivetable=hivetable,scene_id=scene_id,algorithm=algorithm,item_type=item_type,version=version,update_time=update_time)
	print(command_to_table)
	p = subprocess.Popen(command_to_table,shell=True)
	rescode = p.wait()

	return rescode




def LinkToMysql(HOST,USER,PASSWORD,DB,PORT):
	"""
	链接MYSQL数据库
	
	"""
	db = pymysql.connect(host=HOST,
		user=USER,
		password=PASSWORD,
		db=DB,
		port=int(PORT),
		charset="utf8mb4",
		cursorclass=pymysql.cursors.DictCursor
		)
	cursor = db.cursor()

	return cursor,db


def DataFromMysql(HOST,USER,PASSWORD,DB,PORT,sql):
	"""
	获取已下线的物料item_id
	"""
	cursor,db = LinkToMysql(HOST,USER,PASSWORD,DB,PORT)

	try:
		cursor.execute(sql)
		result = cursor.fetchall()
		return result
	except:
		print("Error:unable to fetch data")



def GetOfflineItemId(HOST,USER,PASSWORD,DB,PORT,item_table):
	"""
	返回已经下线的物料ID，类型：list

	"""

	sql = """
	select
		distinct item_id
	from
		{item_table}
	where
		publish=0
	""".format(item_table=item_table)

	data = DataFromMysql(HOST,USER,PASSWORD,DB,PORT,sql)

	item_id = []
	for i in data:
		item_id.append(i['item_id'])

	return item_id




def GetDiffTypeItem(HOST,USER,PASSWORD,DB,PORT,itemtype,item_table):
	"""
	某类型物料只能与特定类型的物料之间计算相似度
	"""
	sql = """
	select
		distinct item_id
	from
		{item_table}
	where
		type in ({itemtype})
		and publish=1
	""".format(itemtype=itemtype,item_table=item_table)
	print(sql)

	data = DataFromMysql(HOST,USER,PASSWORD,DB,PORT,sql)

	item_id=[]
	for i in data:
		item_id.append(i['item_id'])

	return item_id


def deal_ini(input):
	"""
	处理输入的ini文件中的section
	如temp=1:1,2,4;2:2;4:1,2,4:::4:3;2:43,32;1:32:::
	结果为[['1:1,2,4', '2:2', '4:1,2,4'], ['4:3', '2:43,32', '1:32']]

	"""

	res = []
	for i in input.strip().split(":::"):
		if len(i) > 1:
			res.append(i.strip().split(";"))
	return res




