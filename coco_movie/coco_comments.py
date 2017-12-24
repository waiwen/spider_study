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

cookies_douban="ll=\"108231\"; bid=r-bI1Vt9RPo; ct=y; ps=y; OUTFOX_SEARCH_USER_ID_NCOO=528656800.4120224; __yadk_uid=iuzdV23AcYIoIPrtXt81CnoK3tlxvobv; dbcl2=\"114209081:S72c66T/A/0\"; ap=1; _vwo_uuid_v2=F26B9FA21B10CD82C4A4752B4A42864F|658f39908828d3dcf57618ec9fc2c63b; push_noty_num=0; push_doumail_num=0; __utmv=30149280.11420; ck=heTK; __utmc=30149280; _pk_ref.100001.8cb4=%5B%22%22%2C%22%22%2C1513484217%2C%22https%3A%2F%2Fwww.baidu.com%2Flink%3Furl%3DsyMTHbtlOF9RXbNUNE5sgUOuv9hcwjCuS0ca6ej6_ui%26wd%3D%26eqid%3Db425af30000132b3000000065a35efaf%22%5D; _pk_ses.100001.8cb4=*; __utma=30149280.1639511408.1512613247.1513476620.1513484218.12; __utmz=30149280.1513484218.12.9.utmcsr=baidu|utmccn=(organic)|utmcmd=organic; __utmt=1; _pk_id.100001.8cb4=eb4b186427b54ef1.1512644275.11.1513484227.1513476619.; __utmb=30149280.6.9.1513484227200"     #这是你的豆瓣cookie

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
se = requests.session()
se.cookies = requests.utils.cookiejar_from_dict(cookie_dict=get_cookies(cookies_douban),cookiejar=None,overwrite=True)
se.headers = headers

#请求网页的代码整合
def get_response(url):
    resp = se.get(url,headers=headers)
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
    #res = comments.insert_many(infos)
    print('-----数据保存到mongodb-----:  ')
    if next_p != '':
        start(asolute_url+next_p)
    else:
        print('爬取结束。。。。')
        return


if __name__=='__main__':
    start(start_url)
