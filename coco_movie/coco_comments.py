# -*- coding:utf-8 -*-

#author:waiwen
#email:iwaiwen@163.com
#time: 2017/12/7 21:16

import requests
import time
from bs4 import BeautifulSoup
from pymongo import MongoClient
client =  MongoClient('mongodb://xxxxxxxxxxxxxxxxx') #这里是你的Mongodb链接
movie = client.movie
comments = movie.coco_comm

cookies_douban="xxxxxxxxxxxxxxxxxxxxx"     #这是你的豆瓣cookie

asolute_url ='https://movie.douban.com/subject/20495023/comments'

headers={
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36',
     'Connection':'keep-alive',
      }

#将cookie进行处理
def get_cookies(cookie):
    cookie_ls = cookie.split(';')
    cookies={}
    for c in cookie_ls:
        name,value = c.split('=',1)
        cookies[name]=value
    return cookies

#请求网页的代码整合
def get_response(url):

    resp = requests.get(url,headers=headers,cookies=get_cookies(cookies_douban))
    resp.raise_for_status()              #如果发送了一个错误请求(一个 4XX 客户端错误，或者 5XX 服务器错误响应)，
                                         # 我们可以通过 Response.raise_for_status() 来抛出异常：
    soup = BeautifulSoup(resp.content, 'lxml')
    return soup

start_url ='https://movie.douban.com/subject/20495023/comments?start=0&limit=20&sort=new_score&status=P&percent_type='
import random
def get_comm_from_page(url):
    time.sleep(random.randint(1,9)/10)
    print('爬取链接： ',url)
    soup = get_response(url)
    comms = soup.find_all('div',attrs={'class':'comment'})
    infos = []
    for comm in comms:
        vote = int(comm.h3.find('span',attrs={'class':'comment-vote'}).span.text)
        name = comm.h3.find('span',attrs={'class':'comment-info'}).a.text
        comment = comm.p.text.strip().replace('\n','')
        info = {'name':name,'vote':vote,'comment':comment}
        infos.append(info)
    next_page = ''
    try:
        next_page = soup.find('a',attrs={'class':'next'}).get('href')
    except BaseException as e:
        print(e)
    return infos,next_page

def start(s_url):
    infos,next_p = get_comm_from_page(s_url)
    res = comments.insert_many(infos)
    print('-----数据保存到mongodb-----:  ',res)
    if next_p != '':
        start(asolute_url+next_p)
    else:
        print('爬取结束。。。。')
        return


if __name__=='__main__':
    start(start_url)
