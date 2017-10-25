""" 
@author:jansonlv
@file: HtmlDownloader.py 
@time: 2016/8/2
@IDE: PyCharm
@project:spider 
"""

import requests


class HtmlDownloader(object):

    def downlooad(self, url):
        '''
        将url网址下载,并以utf-8格式返回
        :param url:
        :return:
        '''
        if not url:
            return None
        # 随机获取下载头
        user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
        headers = {'User-Agent': user_agent}

        html = requests.get(url, headers=headers)

        if html.status_code == 200:
            html.encoding = 'utf-8'
            return html.content
        return None

def main():
    test = HtmlDownloader()
    test.downlooad('https://baike.baidu.com/item/%E8%9C%98%E8%9B%9B/8135707')

# 测试
if __name__ == '__main__':
    main()
