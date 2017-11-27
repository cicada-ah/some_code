import requests
from lxml import etree
from threading import Thread
import os
import time
import re
import ips
import random
import configs
import configs_log
from DBMysql import DbMysql
from queue import Queue

re_queue = Queue()

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36',
}

log = configs_log.Logging('sxc_log', 'cate_log')

# 开代理获取HTML内容


def re_requests(url, proxies=None):
    try:
        r = requests.get(url, headers=headers, proxies=proxies, timeout=2)
        r.raise_for_status()
        time.sleep(random.random() + 0.3)
        r.encoding = r.apparent_encoding
        return r.text
    except Exception as e:
        log.warn('requests error:{},tans ip'.format(e))
        proxies = {'http': ips.get_ips()}
        re_requests(url, proxies=proxies)


class get_cate():
    def __init__(self, starturl):
        self.starturl = starturl

    def go_cate(self):
        html = re_requests(self.starturl)
        tree = etree.HTML(html)
        languages = tree.xpath('//div[@data-type="IT互联网"]/div[1]/a/text()')[1:]
        urls = tree.xpath('//div[@data-type="IT互联网"]/div[1]/a/@href')[1:]
        urls = ['https://www.shixiseng.com' + url for url in urls]
        log.warn('get_cate already...')
        return languages, urls

    def parse_cate(self, url, language):
        try:
            html = re_requests(url)
            tree = etree.HTML(html)
            urls = tree.xpath('//div[@class="names cutom_font"]/a/@href')
            urls = ['https://www.shixiseng.com' + url for url in urls]
            try:
                page = tree.xpath(
                    '//div[@id="pagebar"]/ul/li[@class="active"]/a/text()')[0]
            except:
                log.info('{} only has one page'.format(language))
                page = 1
            for url in urls:
                item = {'url': url, 'page': str(page), 'language': language}
                re_queue.put_nowait(item)
            try:
                next_url = tree.xpath(
                    '//div[@id="pagebar"]/ul/li[9]/a/@href')
            except:
                pass
            if next_url:
                next_url = 'https://www.shixiseng.com' + next_url[0]
                print(language, next_url)
                log.info('parse_cate:{}'.format(next_url))
                return self.parse_cate(next_url, language)
        except ValueError as e:
            log.info(e)
            return self.parse_cate(url, language)

    def save_to_tb(self, db, table, data):
        db.save_one_data(table, data)

    def save_to_db(self):
        db = DbMysql(configs.TEST_DB)
        table = 'cate'
        while 1:
            try:
                data = re_queue.get_nowait()
                self.save_to_tb(db, table, data)
            except Exception as e:
                print("queue is empty wait for a while")
                time.sleep(2)

    def cate_run(self):
        languages, urls = self.go_cate()
        thread1 = []
        thread2 = []
        for i in range(len(urls)):
            t = Thread(target=self.parse_cate, args=(urls[i], languages[i]))
            thread1.append(t)
            t.start()
        for t in thread1:
            t.join()

        for i in range(10):
            t = Thread(target=self.save_to_db)
            thread2.append(t)
            t.start()
        for t in thread2:
            t.join()
        # with ThreadPoolExecutor(max_workers=5) as executor:
        #     future = [executor.submit(
        #         self.parse_cate, language, url) for url in urls for language in languages]
        #     for f in future:
        #         f.running()
        # with ThreadPoolExecutor(max_workers=5) as executor:
        #     future = [executor.submit(self.save_to_db) for i in range(10)]
        #     for f in future:
        #         f.running()


if __name__ == '__main__':
    cate = get_cate('https://www.shixiseng.com')
    cate.cate_run()
