
# 相似度计算模块说明

## 运行程序

1、搭建python3.6虚拟环境

```
conda create --prefix=./venv_py36 python=3.6
source activate ./venv_py36
```

2、按照依赖包
```
pip install -i https://pypi.tuna.tsinghua.edu.cn/simple -r requirements.txt
```

3、运行程序


运行方式：

```
python ./app/run.py -c 配置文件
```



- 测试环境

默认为配置文件为config_db_test.ini

```
python ./app/run.py -c config_db_test.ini

```

测试环境：将数据写入/hive/warehouse/recommend_test.db 和 recommend_test.similar_recommed_items_discover、 recommend_test.similar_recommed_items_discover_videos 表中


- 生产环境


默认为配置文件为config_db_prod.ini

```
python ./app/run.py -c config_db_prod.ini
```

测试环境：将数据写入/hive/warehouse/recommend.db 和 recommend.similar_recommed_items_discover、 recommend.similar_recommed_items_discover_videos 表中



- 开发环境

第一步：使用config_dev.ini配置文件，并做如下修改

![待修改四处](/data/image/ex.png)

将画圈的四处做修改，改为使用者自己的HDFS用户名

第二步：执行

```
python ./app/run.py -c config_dev.ini

```

开发环境：将数据写入个人库中，如zhangxiang， 写入/user/zhangxiang/ 和 zhangxiang.similar_recommed_items_discover、 zhangxiang.similar_recommed_items_discover_videos 表中






说明：

1、给定一个输入的物料，输出与指定类型相关的物料，参考视频相似度计算的

2、