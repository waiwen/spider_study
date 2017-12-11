# -*- coding:utf-8 -*-

#author:waiwen
#email:iwaiwen@163.com
#time: 2017/12/8 12:25
from coco_movie.coco_comments import movie,get_response

mtime_comm = movie.coco_mt_comm

def get_comm_from_page(page_num):

    url = 'http://movie.mtime.com/227434/reviews/short/new-{0}.html'.format(str(page_num))
    if page_num == 1:
        url = 'http://movie.mtime.com/227434/reviews/short/new.html'

    soup = get_response(url)
    infos = []
    divs= soup.find_all('div',attrs={'class':'mod_short'})
    for div in divs:
        comm= div.h3.text.strip().replace('\n', '')
        name= div.find('div', attrs={'class': 'pic_58'}).a.get('title').strip().replace('\n', '')
        info = {'name': name, 'comment': comm}
        print(info)
        infos.append(info)

    return infos

#开始爬取时光网
def start():
    infos = []
    for i in range(1, 11):
        print('*' * 100, i)
        info = get_comm_from_page(i)
        infos = infos + info
    res = mtime_comm.insert_many(infos)
    print(res)

def get_comm_form_mongo():
    resp = mtime_comm.find({},{'_id':0})
    return list(resp)

if __name__ =="__main__":
    start()