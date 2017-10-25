""" 
@author:jansonlv
@file: spiderWork.py 
@time: 2016/8/2
@IDE: PyCharm
@project:Simple_distributed_crawler 
"""

#coding:utf-8
from multiprocessing.managers import BaseManager
from HtmlDownloader import HtmlDownloader
from HtmlParser import HtmlParser


class SpiderWork(object):

    def __init__(self):
        #初始化分布式进程中的工作节点的连接工作
        class QueueManager(BaseManager):
            pass

        # 实现第一步：使用BaseManager注册获取Queue的方法名称
        QueueManager.register('get_task_queue')
        QueueManager.register('get_result_queue')

        # 实现第二步：连接到服务器:
        server_addr = ('192.168.10.128', 8004)
        print('Connect to server {}...' .format(server_addr))

        # 端口和验证口令注意保持与服务进程设置的完全一致:
        self.m = QueueManager(address=server_addr, authkey='janson'.encode())

        # 从网络连接:
        self.m.connect()

        # 实现第三步：获取Queue的对象:
        self.task = self.m.get_task_queue()
        self.result = self.m.get_result_queue()

        #初始化网页下载器和解析器
        self.downloader = HtmlDownloader()
        self.parser = HtmlParser()
        print('init finish')

    def crawl(self):
        '''
        分布式爬虫节点调度器
        :return:
        '''
        while True:
            try:
                # url任务节点不为空时
                if not self.task.empty():
                    # 获取url
                    url = self.task.get()
                    # 当url为end时,说明控制节点通知关闭
                    if url == 'end':
                        print('控制节点通知爬虫节点停止工作...')
                        # 接着通知其它节点停止工作
                        self.result.put({'new_urls': 'end', 'data': 'end'})
                        return
                    else:
                        # 否则解析数据
                        print('爬虫节点正在解析:%s' % url.encode('utf-8'))
                        # 下载器下载
                        content = self.downloader.download(url)
                        # 解析数据
                        new_urls, data = self.parser.parser(url, content)
                        # 提交队列
                        self.result.put({"new_urls": new_urls, "data": data})
            except Exception as error:
                print('error-------->', error)
                print("连接工作节点失败")
                return


if __name__ == "__main__":
    spider = SpiderWork()
    spider.crawl()


'''
TypeError: 'Queue' object is not callable
控制调度器确实匿名函数

'''