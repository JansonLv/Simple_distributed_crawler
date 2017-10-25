""" 
@author:jansonlv
@file: HtmlParser.py 
@time: 2016/8/2
@IDE: PyCharm
@project:spider 
"""

import re
from bs4 import BeautifulSoup
import lxml

class HtmlParser(object):
    def parser(self, page_url, html_content):
        '''
        用于解析网页内容,抽取url和数据
        :param page_url: 下载页面的url????
        :param html_content: 下载的网页内容
        :return: 返回url和数据
        '''
        if page_url is None or not html_content:
            pass
        soup = BeautifulSoup(html_content, 'html.parser', from_encoding='utf-8')

        new_urls = self._get_new_urls(page_url, soup)
        new_data = self._get_new_data(page_url, soup)
        return new_urls, new_data

    def _get_new_urls(self, page_url, soup):
        '''
        抽取新的url集合
        :param page_url: 下载页面的url???
        :param html_content: html页面内容
        :return: 返回新的url集合
        '''
        new_urls = set()
        '''
        抽取url地址
        '''
        links = soup.select('body > div.body-wrapper > div.content-wrapper > div > div.main-content > div.lemma-summary > div > a')
        # print(p)
        for link in links:
            url = link.get('href')
            new_urls.add('https://baike.baidu.com' + url)


        return new_urls

    def _get_new_data(self, page_url, soup):
        '''
        抽取有效数据
        :param page_url: 下载页面的url
        :param html_content: html页面内容
        :return: 返回有效数据
        '''
        data = {}
        data['url'] = page_url
        '''
        提取data数据
        '''
        title = soup.select('body > div.body-wrapper > div.content-wrapper > div > div.main-content > dl.lemmaWgt-lemmaTitle.lemmaWgt-lemmaTitle- > dd > h1')[0].get_text()


        data['title'] = title
        return data
'''

    body > div.body-wrapper > div.content-wrapper > div > div.main-content > div.lemma-summary > div:nth-child(1) > a
    body > div.body-wrapper > div.content-wrapper > div > div.main-content > div.lemma-summary > div:nth-child(2) > a:nth-child(1)
    body > div.body - wrapper > div.content - wrapper > div > div.main - content > div.lemma - summary > div > a.xh - highlight
'''
#coding:utf-8
# import re
# from urllib.parse import urljoin
# from bs4 import BeautifulSoup
#
#
# class HtmlParser(object):
#
#     def parser(self,page_url,html_cont):
#         '''
#         用于解析网页内容抽取URL和数据
#         :param page_url: 下载页面的URL
#         :param html_cont: 下载的网页内容
#         :return:返回URL和数据
#         '''
#         if page_url is None or html_cont is None:
#             return
#         soup = BeautifulSoup(html_cont,'html.parser',from_encoding='utf-8')
#         new_urls = self._get_new_urls(page_url,soup)
#         new_data = self._get_new_data(page_url,soup)
#         return new_urls,new_data
#
#
#     def _get_new_urls(self,page_url,soup):
#         '''
#         抽取新的URL集合
#         :param page_url: 下载页面的URL
#         :param soup:soup
#         :return: 返回新的URL集合
#         '''
#         new_urls = set()
#         #抽取符合要求的a标签
#         # 原书代码
#         # links = soup.find_all('a', href=re.compile(r'/view/\d+\.htm'))
#         #2017-07-03 更新,原因百度词条的链接形式发生改变
#         links = soup.find_all('a',href=re.compile(r'/item/.*'))
#         for link in links:
#             #提取href属性
#             new_url = link['href']
#             #拼接成完整网址
#             # new_full_url = urlparse.urljoin(page_url,new_url)
#             new_full_url =
#             new_urls.add(new_full_url)
#         return new_urls
#     def _get_new_data(self,page_url,soup):
#         '''
#         抽取有效数据
#         :param page_url:下载页面的URL
#         :param soup:
#         :return:返回有效数据
#         '''
#         data={}
#         data['url']=page_url
#         title = soup.find('dd',class_='lemmaWgt-lemmaTitle-title').find('h1')
#         data['title']=title.get_text()
#         summary = soup.find('div',class_='lemma-summary')
#         #获取到tag中包含的所有文版内容包括子孙tag中的内容,并将结果作为Unicode字符串返回
#         data['summary']=summary.get_text()
#         return data