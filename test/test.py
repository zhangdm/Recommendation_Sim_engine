#!/usr/bin/env python
# -*- coding:UTF-8 -*-

import configparser
import os

curpath = os.path.dirname(os.path.realpath(__file__))

abspath = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
cfgpath = os.path.join(abspath,"config_dev.ini")

print(cfgpath)

conf = configparser.ConfigParser()
conf.read(cfgpath,encoding="utf-8")
sections = conf.sections()

item = conf.items("py_config")

# print(item['filepath'])

print(conf.get("py_config","filepath"))