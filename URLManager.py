""" 
@author:jansonlv
@file: URLManager.py 
@time: 2017/10/25 
@IDE: PyCharm
@project:Simple_distributed_crawler 
"""
import pickle   # 存入什么类型数据,取出还是什么类型数据!  参考http://www.cnblogs.com/cobbliu/archive/2012/09/04/2670178.html
import hashlib

class URLManager(object):

    def __init__(self):
        # 定义未爬取的urls
        self.new_urls = self.load_progress('new_urls.txt')
        # 定义已爬取的urls
        self.old_urls = self.load_progress('old_urls.txt')

    @staticmethod
    def md5_encrypt_16(url):
        '''
        md5加密
        :param url: 需要加密的url
        :return: 返回中间的16位加密码
        '''
        # md5加密
        m = hashlib.md5()
        m.update(url.encode())
        # 返回md5密码中间的16位
        return m.hexdigest()[8:-8]

    def has_new_url(self):
        '''
        判断是否还有新的url
        :return:bool类型
        '''
        return self.new_url_size() != 0

    def get_new_url(self):
        '''
        获取一个未爬取的url
        :return:url字符串
        '''
        # 获取一个未爬取的url
        new_url = self.new_urls.pop()
        # 将加密的中间16位写入已爬取的urls集合中
        self.old_urls.add(URLManager.md5_encrypt_16(new_url))
        return new_url

    def add_url(self, url):
        '''
        将url加入未爬取的urls
        :param url:
        :return:
        '''
        url_md5 = URLManager.md5_encrypt_16(url)
        # 判断该url是否加入urls中或者已爬取
        if url in self.new_urls or url_md5 in self.old_urls:
            # 已爬取或已存在则返回
            return
        else:
            # 加入
            # print(url)
            # print(type(self.new_urls))
            self.new_urls.add(url)

    def add_new_url(self, url):
        '''
        将获取的url添加到未爬取的urls集合中
        :param url: 未爬取的url
        :return:
        '''
        if not url:
            return
        self.add_url(url)


    def add_new_urls(self, urls):
        '''
        将获取的urls集合加入未爬取的urls集合中
        :param urls: 获取的urls集合
        :return:
        '''
        # 获取的urls为空则返回
        if not urls:
            return
        for url in urls:
            # 获取的url为空则跳开
            if not url:
                continue
            self.add_url(url)

    def new_url_size(self):
        '''
        获取未爬取的url集合的大小
        :return:
        '''
        return len(self.new_urls)

    def old_url_size(self):
        '''
        获取已爬取的url_md5集合的大小
        :return:
        '''
        return len(self.old_urls)

    def save_progress(self, path, data):
        '''
        将数据pickle化写入
        :param path:对象文件
        :param data:数据
        :return:
        '''
        with open(path, 'wb') as f:
            pickle.dump(data, f)

    def load_progress(self, path):
        '''
        将pickle对象文件中的对象返回
        :param path:
        :return:
        '''
        print('[+] 从文件加载进度:{}'.format(path))
        f = open(path, 'rb')
        try:
            temp = pickle.load(f)
            f.close()
            return temp
        except Exception as error:
            f.close()
            print('error----->', error)
            print('[!] 无文件进度,创建:{}'.format(path))
            return set()


def main():
    a = URLManager()
    a.save_progress('new_urls.txt', set(['1', '2']))
    urlmanager = URLManager()

    urlmanager.add_new_url('aaa')
    print(urlmanager.new_urls)
    test_list = ['bbb', 'aaa', '', 'ccc', 'bbb']
    urlmanager.add_new_urls(test_list)
    print(urlmanager.new_urls)

if __name__ == '__main__':
    main()

'''
Q1:AttributeError: 序列化返回后'tuple' object has no attribute 'add'
测试时,添加数据为元组类型,元组定以后不能修改


'''