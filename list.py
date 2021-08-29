#!/usr/bin/python
# -*- coding:utf-8 -*-
 
from typing import Text
import requests #用来抓取网页的html源码
import random   #取随机数
import re
import time #时间相关操作
import sys
from bs4 import BeautifulSoup #用于代替正则式 取源码中相应标签中的内容
 
 
def get_content(url, data = None):
    #设置headers是为了模拟浏览器访问 否则的话可能会被拒绝 可通过浏览器获取
    header = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Connection': 'keep-alive',
        # 'Accept-Encoding': 'br, gzip, deflate',
        'Accept-Language':'zh',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_4) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/11.1 Safari/605.1.15'
    }
    #设置一个超时时间 取随机数 是为了防止网站被认定为爬虫
    timeout = random.choice(range(80,180))
 
    while True:
        try:
            req = requests.get(url=url, headers = header, timeout = timeout)
            req.encoding = req.apparent_encoding
            break
        except Exception as e:
            print('3' + e)
            time.sleep(random.choice(range(8, 15)))
    return req.text
 
def get_data(html):
    bf = BeautifulSoup(html,'html.parser')
#    for i in range(6):
    texts = bf.find_all('div',{'class':'section-box'})
    urls = texts[1].find_all("a")
    print(urls)
    # text = urls[6:-2]
    # print(texts)
    # next = urls[-1].get("href")
    # link  = 'https://www.chuanyuemi.com' + next
    # time.sleep(random.choice(range(8, 15)))
    # next_html = get_content(link)
    # bf = BeautifulSoup(next_html,'html.parser')
    # texts = bf.find_all('div',{'class':'info_chapters'})
    # urls = texts[0].find_all("a")
    # print(urls)
    # text = urls[6:-2]
    # print(text)


if __name__ == '__main__':
    url = 'https://www.chuanyuemi.com/B/306756/306756384/index.shtml'
    html = get_content(url)
    # print(html)
 
    get_data(html)


