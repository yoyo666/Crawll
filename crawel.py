#!/usr/bin/python
# -*- coding:utf-8 -*-
 
import requests #用来抓取网页的html源码
import random   #取随机数
from bs4 import BeautifulSoup #用于代替正则式 取源码中相应标签中的内容
import time #时间相关操作
import re
 
 
class downloader(object):
    def __init__(self):
        self.server = 'https://www.chuanyuemi.com'
        self.target = 'https://www.chuanyuemi.com/B/306756/306756384/index.shtml'
        self.names = [] #章节名
        self.urls = []  #章节链接
        self.nums = 0   #章节数
 
    """
    获取html文档内容
    """
    def get_content(self,url):
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
 
    """
    获取下载的章节目录
    """
    def get_download_catalogue(self,url):
        html = self.get_content(url)
        bf = BeautifulSoup(html,'html.parser')
        texts = bf.find_all('div',{'class':'section-box'})
        iurls = texts[1].find_all("a")
        # print(iurls)
        # text = iurls[6:-2] #我们需要去掉重复的最新章节列表 只为演示 我们只取 不重复的前5章
        self.nums += len(iurls)
        for each in iurls:
                self.names.append(each.string)
                self.urls.append(self.server + each.get('href'))
        # print(self.names)
    """
    获取下载的具体章节
    """
    def get_download_content(self, url):
        flag = True
        content = ''
        html = self.get_content(url)
        bf = BeautifulSoup(html,'html.parser')

        while flag:
            texts = bf.find_all('div', {'class': 'content', 'id': 'content'})
            # text = texts[0].text.replace('\xa0'*7,'\n\n')#\xa0表示连续的空白格
            text = texts[0].find_all('p')
            for i in range(len(text)):
                content += text[i].text + '\n\n'

            get_url = bf.find_all('div', {'class': 'section-opt m-bottom-opt'})
            next_page = get_url[0]
            button = next_page.find_all('a', {'id': 'next_url'})
            # print(button)
            link = button[0].get("href")
            next_url = 'https://www.chuanyuemi.com' + link
            # print(next_url)
            title = button[0].text
            # print(title)
            if title == ' 下一页':
                flag = True
                next_html = self.get_content(next_url)
                bf = BeautifulSoup(next_html, 'html.parser')
            else:
                flag = False
            # time.sleep(random.choice(range(8, 15)))
        return content


    """
    将文章写入文件
    """
    def writer(self,name,path,text):
        write_flag = True
        with open(path, 'a', encoding='utf-8') as f:
            f.write(name + '\n')
            f.writelines(text)
            f.write('\n\n')
 
if __name__ == '__main__':
    dl = downloader()
    # print(dl.target)
    dl.get_download_catalogue(dl.target)
    for i in range(dl.nums):
        print(dl.names[i])
        dl.writer(dl.names[i], 'src\女法医的洗冤路gl.txt', dl.get_download_content(dl.urls[i]))
        print("已下载：%.2f%%"% float((i+1)/dl.nums * 100) + '\r')
        time.sleep(random.choice(range(5, 12)))
    print('下载完成！')