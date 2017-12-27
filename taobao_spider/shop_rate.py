# -*- coding:utf-8 -*-

#author:waiwen
#email:iwaiwen@163.com
#time: 2017/12/24 11:35

import requests
import re
import pandas as pd
import json
import numpy as np


def get_detail_count(url):
    rates = requests.get(url).text
    rate_count = re.search(r'rateCount[\s\S]*?rateDance',rates)
    rate_detail = re.search(r'paginator[\s\S]*?rateCount', rates)
    d_detail = eval(rate_detail.group()[11:-11])
    d_count = eval(rate_count.group()[11:-11])
    return d_count,d_detail


def get_df(url):
    r = requests.get(url)
    r.raise_for_status()
    rates = r.text
    rate_list = re.search((r'rateList\"\:\[[\s\S]*?\]\,\"search'), rates)

    rate_l = rate_list.group()[10:-8]

    l_df = pd.read_json(rate_l)         # 读取符合格式的json对象（这里读取的是符合json规范的一段字符串），返回pandas的dataframe对象

    l_df.dropna(axis=1)                                  #删除所有包含空值的列
    return l_df
import time
if __name__ == '__main__':

    result = pd.DataFrame()

    for i in range(1,5):
        time.sleep(1)
        url = 'http://rate.tmall.com/list_detail_rate.htm?itemId=41464129793&sellerId=1652490016&currentPage={}'.format(str(i))
        try:
            l_df= get_df(url)
            print('获取 %s 页数据成功'%str(i))
            result = pd.concat([result,l_df],ignore_index=True)
        except Exception as e:
            print(e)
            continue

    result.to_csv('E:\\taobao_rate.csv',encoding="utf_8_sig")     #utf-8编码输出到csv文件，否则会乱码


