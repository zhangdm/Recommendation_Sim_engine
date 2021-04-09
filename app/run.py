
#!/usr/bin/env python
# -*- coding:UTF-8 -*-


from dao import CalSim
from dao import FecthData
from dao import SimSaveText
from dao import TextToHive
import argparse
import logging
logging.basicConfig(format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s', level=logging.INFO)

logger = logging.getLogger(__name__)



def main():
	logging.info(u"参数")
	parser = argparse.ArgumentParser(description='Set the date range...')
	parser.add_argument('-c',type=str,default="config_prod.ini")
	args = parser.parse_args()

	if args.c:
		configini = args.c

	logging.info(u"开始计算")
	SimSaveText.CalSimToText(configini)

if __name__ == '__main__':
	main()
