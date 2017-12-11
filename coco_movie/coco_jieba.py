# -*- coding:utf-8 -*-

#author:waiwen
#email:iwaiwen@163.com
#time: 2017/12/8 11:05

from collections import Counter
from os import path
import jieba
from wordcloud import WordCloud,STOPWORDS,ImageColorGenerator
import jieba.analyse
from coco_movie.coco_mtime_comm import mtime_comm
from coco_movie.coco_comments import comments
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image

def get_comms():
    comms = comments.find({}, {'comment': 1, '_id': 0})
    comms = [c.get('comment') for c in comms]
    print('豆瓣影评数量： ',len(comms))
    mtime_comms = mtime_comm.find({}, {'comment': 1, '_id': 0})
    mtime_comms = [t.get('comment') for t in mtime_comms]
    print('时光网影评数量： ', len(mtime_comms))
    s = ''.join(comms + mtime_comms).strip()
    return s
# pic_path='C:\Users\95815\Desktop\python\coco\coco.jpg'

def out_excel(data):
    import xlwt
    file = xlwt.Workbook()
    table = file.add_sheet('coco_comments',cell_overwrite_ok=True)
    for i in range(len(data)):
        table.write(i,0,data[i][0])
        table.write(i,1,data[i][1])
    file.save('coco_comms.xls')

d = path.dirname(__file__)

if __name__ == '__main__':

   comms = get_comms()
   comm_tf= jieba.analyse.extract_tags(comms,topK=200)

   print('权重',comm_tf)

   word_c = Counter(jieba.lcut(comms,cut_all=True))

   c_list = [t for t in word_c.most_common(200) if t[0] in comm_tf]
   out_excel(c_list)
   c_d = {}
   for t in c_list:
       c_d[str(t[0])]=t[1]

   print('词频统计 ： ',c_d)

   f_path='E:\downloads\hye4gjm.ttf'  #字体的路径
   print(path.join(d,'coco.jpg'))
   coco_color = np.array(Image.open(path.join(d,'guitar.jpg')))
   wc = WordCloud(font_path=f_path,background_color='white',max_words=2000,mask=coco_color,max_font_size=80)

   wc.fit_words(c_d)

   image_colors = ImageColorGenerator(coco_color)

   plt.imshow(wc,interpolation='bilinear')
   plt.axis('off')
   plt.figure()

# recolor wordcloud and show
# we could also give color_func=image_colors directly in the constructor
   plt.imshow(wc.recolor(color_func=image_colors), interpolation="bilinear")
   plt.axis("off")

   plt.show()
