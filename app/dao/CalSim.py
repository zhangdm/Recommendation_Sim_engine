#!/usr/bin/env python
# -*- coding:UTF-8 -*-


import numpy as np
from scipy.sparse import csc_matrix
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from utils.utils import getparam
import logging
logging.basicConfig(format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)



def calsim(configini,features):

	topics = int(getparam(configini,"algorithm_param","topics"))

	rows = []
	cols = []
	res = []

	rows_classlabel = []
	cols_classlabel = []
	res_classlabel = []

	logging.info(u"将算法生成的特征与classlabel特征分开")
	for colindex,line in enumerate(features):
		line = str(line).split(" ")

		for value in line:
			value = value.strip().split(":")

			if int(value[0]) <= topics:
				res.append(float(value[1].strip()))
				rows.append(colindex)
				cols.append(int(value[0]))
			else:
				res_classlabel.append(float(value[1].strip()))
				rows_classlabel.append(colindex)
				cols_classlabel.append(float(value[0].strip()))

	
	logging.info(u"算法生成的特征")
	res0 = np.array(res)
	cols0 = list()
	for col in cols:
		cols0.append(col - 1)
	cols0 = np.array(cols0)

	rows0 = np.array(rows)

	dataalgor = csc_matrix((res0,(rows0,cols0)),shape = (features.shape[0],topics)).toarray()

	# print(dataalgor)


	logging.info(u"class、label组成的特征")
	res0_classlabel = np.array(res_classlabel)
	cols0_classlabel = list()
	for col in cols_classlabel:
		cols0_classlabel.append(col - 10000)
	cols0_classlabel = np.array(cols0_classlabel)


	rows0_classlabel = np.array(rows_classlabel)

	datalclasslabel = csc_matrix((res0_classlabel,(rows0_classlabel,cols0_classlabel)),shape=(features.shape[0],int(max(cols0_classlabel)+1))).toarray()

	logging.info(u"数据合并")

	AllData = pd.concat([pd.DataFrame(dataalgor),pd.DataFrame(datalclasslabel)],axis = 1)
	

	# 计算相似度，输出相似度值和index
	cidsim = cosine_similarity(AllData)

	return cidsim