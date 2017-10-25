""" 
@author:jansonlv
@file: webparser.py 
@time: 2017/10/25 
@IDE: PyCharm
@project:Simple_distributed_crawler 
"""
import lxml
from bs4 import BeautifulSoup
import requests
url = 'https://baike.baidu.com/item/%E8%9C%98%E8%9B%9B/8135707'
user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
headers = {'User-Agent': user_agent}

html = requests.get(url, headers=headers)
print(html.content)

soup = BeautifulSoup(html.content, 'html.parser', from_encoding='utf-8')

a = soup.select('body > div.body-wrapper > div.content-wrapper > div > div.main-content > div.lemma-summary > div')

for i in a:
    print(a)

