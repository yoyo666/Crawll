#!/usr/bin/python
# -*- coding:utf-8 -*-
 
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
        'Accept-Language':'zh-cn',
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
    flag = True
    content = ''
    bf = BeautifulSoup(html,'html.parser')

    # content = bf.find_all('div',{'class':'nr_function'})[0].find_all("h1")
    # pages_str = content[0].get_text()
    # pat=re.compile(r'[0-9]+') # 正则匹配数字
    # res=pat.findall(pages_str)
    # pages = int(res[-1])
    #
    # print(pages_str)
    # print(pages)

    while flag:
        texts = bf.find_all('div',{'class':'content','id':'content'})
        # text = texts[0].text.replace('\xa0'*7,'\n\n')#\xa0表示连续的空白格
        text = texts[0].find_all('p')
        for i in range(len(text)):
            content += text[i].text + '\n\n'

        get_url = bf.find_all('div',{'class':'section-opt m-bottom-opt'})
        next_page = get_url[0]
        button = next_page.find_all('a',{'id':'next_url'})
        print(button)
        link = button[0].get("href")
        next_url = 'https://www.chuanyuemi.com' + link
        print(next_url)
        title = button[0].text
        print(title)
        if title == ' 下一页':
            flag = True
            next_html = get_content(next_url)
            bf = BeautifulSoup(next_html, 'html.parser')
        else:
            flag = False
        # time.sleep(random.choice(range(8, 15)))
        # next_html = get_content(next_url)
        # bf = BeautifulSoup(next_html, 'html.parser')
    print(content)


if __name__ == '__main__':
    url = 'https://www.chuanyuemi.com/C/127/127795/46333514.shtml'
    html = get_content(url)
    # print(html)
 
    get_data(html)


