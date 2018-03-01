
## 0、简介

记录一些自己进行实战的爬虫demo。
尽量将详细的注释撰写在代码中，增强可读性。

### 1、algorithm
   记录一些常用的算法

### 2、coco_movie
   是电影《寻梦环游记》的影评爬取和词云制作

### 3、taobao_spider
   关于淘宝的爬虫，商品类目，商品评论等等

### 4、pywin32_install
   该脚本是用于注册python的安装路径，安装pywin32模块找不到路径时使用
   
### 5、uitl
   存储一些爬虫常用的工具，例如user_agent库
   
### 6、2018/02/28 更新 添加scrapy爬虫工程，toscrape为爬虫练习网站
   入门爬取1000本书籍信息，考察 **书本链接的提取和进一步爬取，下一页链接的提取和循环爬取**，
   不考虑爬虫速度，ip等带来的封禁
   在工程目录下输入 scrapy crawel -o books.csv 将会直接将item实例宝保存到该csv文件，
   pipeline钩子函数在输出文件前得到执行，可再次对item进行额外的操作，例如数据的处理，输入到数据库等等