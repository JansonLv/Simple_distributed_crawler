""" 
@author:jansonlv
@file: control_scheduler.py 
@time: 2017/10/25 
@IDE: PyCharm
@project:Simple_distributed_crawler 
"""
import time
from multiprocessing import Queue, Process
from multiprocessing.managers import BaseManager

from control_node.DataOutpt import DataOutput

from control_node.URLManager import URLManager


class ControlScheduler(object):

    def create_manager(self, url_queue, result_queue):
        '''
        创建一个分布式管理器
        :param url_queue:url任务队列,管理器将url传递给爬虫节点的通道,需要注册到网络
        :param result_queue: 爬虫节点将数据返回给数据提取进程的通道,需要注册到网络
        :return:
        '''
        # 将创建的两个队列注册在网络上,callable应该是两个队列变量
        BaseManager.register('get_task_queue', callable=lambda:url_queue)
        BaseManager.register('get_result_queue', callable=lambda:result_queue)

        # 绑定端口,实例化并返回
        server_addr = ('192.168.10.128', 8004)
        return BaseManager(server_addr, authkey='janson'.encode())

    def url_manager_proc(self, url_task_q, url_from_data_solve_q, start_url):
        '''

        :param url_task_q: 需要发送给爬虫节点的进程
        :param url_from_data_solve_q: url从数据处理进程发过来的数据
        :param start_url: 起始爬取的url地址
        :return:
        '''
        url_manager = URLManager()
        url_manager.add_new_url(start_url)

        while True:
            while url_manager.has_new_url():
                # 获取一个url地址
                new_url = url_manager.get_new_url()
                # 发送给队列
                url_task_q.put(new_url)
                # ??
                print('old_url=', url_manager.old_url_size())
                # 加一个判断条件,当爬取过200个网页时关闭
                if url_manager.old_url_size() > 200:
                    url_task_q.put('end')
                    print('控制节点发起结束通知')

                    # 关闭节点,同时存储
                    url_manager.save_progress('new_urls.txt', url_manager.new_urls)
                    url_manager.save_progress('old_urls.txt', url_manager.old_urls)

                    return

            # 将从result_solve_proc获取到url添加到url管理器
            try:
                # print('将从result_solve_proc获取到url添加到url管理器')
                if not url_from_data_solve_q.empty():
                    urls = url_from_data_solve_q.get()
                    url_manager.add_new_urls(urls)
            except Exception as error:
                print('url_manager_process---------->:', error)
                # 延时休息
                time.sleep(0.5)

    def data_solve_proc(self, data_from_spider_node_q, url_to_url_manager_q, data_to_data_output_q):
        '''
        数据提取进程
        :param data_from_spider_node_q: 爬虫节点返回的数据
        :param url_to_url_manager_q: 向urlmanager发送url的队列
        :param data_to_data_output_q: 向dataoutput发送data的队列
        :return:
        '''
        while True:
            try:
                # 爬虫节点返回的数据不为空
                if not data_from_spider_node_q.empty():
                    content = data_from_spider_node_q.get(True)
                    if content['new_urls'] == 'end':
                        print('结果分析进程接收通知并结束')
                        # 数据向数据存储进程发送结束
                        data_to_data_output_q.put('end')
                        return
                    # set类型
                    url_to_url_manager_q.put(content['new_urls'])
                    data_to_data_output_q.put(content['data'])
                    # print(content['data'])
                    '''
                    {'url': 'https://baike.baidu.com/item/FOAF', 'content': 'FOAF', 'title': 'FOAF'}
                    '''
                else:
                    time.sleep(0.2)
            except Exception as error:
                print('result_solve_proc------>', error)
                time.sleep(0.1)

    def data_save_proc(self, data_from_data_solve_q):
        '''
        数据存储进程
        :param data_from_data_solve_q:从数据处理进程返回的数据队列
        :return:
        '''
        output = DataOutput()
        while True:

            if not data_from_data_solve_q.empty():
                data = data_from_data_solve_q.get()
                if data == "end":
                    print('存储器进程接收end通知并结束')
                    output.ouput_end(output.filepath)
                    return
                output.store_data(data)
            else:
                time.sleep(0.1)

def main():
    # 要爬取的连接地址
    start_url = 'https://baike.baidu.com/item/%E8%9C%98%E8%9B%9B/8135707'
    # 初始化四个队列
    url_to_spider_node_q = Queue()
    data_from_spider_node_q = Queue()
    url_to_url_manager_q = Queue()
    data_to_data_output_q = Queue()

    # 创建对象
    control_scheduler = ControlScheduler()
    # 创建分布式管理器
    manager = control_scheduler.create_manager(url_to_spider_node_q, data_from_spider_node_q)
    # 创建urlmanager进程 url_task_q, url_from_data_solve_q, start_url
    url_manager_proc = Process(target=control_scheduler.url_manager_proc, args=(url_to_spider_node_q,
                                                                                url_to_url_manager_q,
                                                                                start_url))
    #  创建数据处理进程 data_from_spider_node_q, url_to_url_manager_q, data_to_data_output_q
    data_solve_proc = Process(target=control_scheduler.data_solve_proc, args=(data_from_spider_node_q,
                                                                              url_to_url_manager_q,
                                                                              data_to_data_output_q))
    # 创建dataoutput进程 data_from_data_solve_q
    data_output_proc = Process(target=control_scheduler.data_save_proc, args=(data_to_data_output_q,))

    # 启动3个进程
    data_output_proc.start()
    data_solve_proc.start()
    url_manager_proc.start()

    # 启动管理器
    manager.get_server().serve_forever()


if __name__ == '__main__':
    main()
