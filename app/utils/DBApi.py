#coding=utf-8

from impala.dbapi import connect
from impala.util import as_pandas
import pandas as pd

impala_config = {
    "host": "10.21.130.61",
    "port": 21050,
    "user": "hdfs",
    "auth_mechanism": "GSSAPI",
    "kerberos_service_name": 'impala'
        }

hive_config = {
    "host": "10.21.130.61",
    "port": 10000,
    "user": "hdfs",
    "auth_mechanism": "GSSAPI",
    "kerberos_service_name": 'hive'
        }


def impala_query(sql):
    conn = connect(**impala_config)
    cur = conn.cursor()
    cur.execute(sql)
    df = as_pandas(cur)
    conn.close()
    return df


def impala_exec(sql):
    conn = connect(**impala_config)
    cur = conn.cursor()
    cur.execute(sql)
    conn.close()


def hive_query(sql):
    conn = connect(**hive_config)
    cur = conn.cursor()
    cur.execute(sql)
    data = cur.fetchall()
    conn.close()
    return pd.DataFrame(data)



def hive_exec(sql):
    conn = connect(**hive_config)
    cur = conn.cursor()
    cur.execute(sql)
    conn.close()
