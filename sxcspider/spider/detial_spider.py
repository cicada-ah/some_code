import requests
from concurrent.futures import ThreadPoolExecutor as Pool
import os
import time
import re
from ips import ips
import random
from configs import configs
from configs_log import configs_log
from DBmodel.DBMysql import DbMysql
from queue import Queue
import threading

re_queue = Queue()
lock = threading.Lock()
i = 0
headers = {
    'Connection': 'close',
    'Host': 'www.shixiseng.com',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36',
}

log = configs_log.Logging('sxc_log', 'detial_log')

# 开代理获取HTML内容


def re_requests(url, proxies=None):
    try:
        time.sleep(random.random() * 3 + 2)
        r = requests.get(url, headers=headers, proxies=proxies, timeout=2)
        r.raise_for_status()
        r.encoding = r.apparent_encoding
        return r.text
    except Exception as e:
        log.warn('requests error:{},tans ip...'.format(e))
        proxies = {"http": random.choice(ips.ips)}
        re_requests(url, proxies=proxies)


class detail_spider():
    def __init__(self):
        self.db = DbMysql(configs.TEST_DB)

    @property
    def get_urls(self):
        data_all = self.db.find_all('cate',)
        for data in data_all:
            url = data['url']
            yield url

    def parse_time(self, data):
        new_data = data.replace(
            '&#xed93', '0').replace('&#xe83c', '1').replace('&#xe2d4', '2').replace('&#xf302', '3').replace('&#xf882', '4').replace('&#xf0c3', '5').replace('&#xf0f9', '6').replace('&#xf808', '7').replace('&#xf76c', '8').replace('&#xf688', '9')
        return new_data

    def parse_detail(self, url):
        global i
        html = re_requests(url)
        position = re.findall(
            r'<div class="new_job_name" title="(.*?)">', html)[0]
        job_position = re.findall(
            r'<span title="(.*?)" class="job_position">', html)[0]
        salary = self.parse_time(re.findall(
            r'<span class="job_money cutom_font">(.*?)</span>', html)[0])
        edu = re.findall(r'<span class="job_academic">(.*?)</span>', html)[0]
        sx_time = self.parse_time(re.findall(
            r'<span class="job_week cutom_font">(.*?)</span>', html)[0])

        detail = re.findall(r'<div class="job_detail">(.*?)</div>', html)[0].replace(
            '<p>', '').replace('</p>', '').replace('&nbsp;', '').replace('<br>', '').replace('<div>', '').replace('</div>', '')
        p = re.compile(r'<(.*?)span(.*?)>')
        detail = re.sub(p, '', detail)
        end_time = self.parse_time(re.findall(
            r'<div class="job_detail cutom_font">(.*?)</div>', html)[0])
        create_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        data = {'position': position, 'job_position': job_position, 'salary ': salary, 'edu': edu,
                'sx_time': sx_time, 'detail': detail, 'end_time': end_time, 'create_time': create_time}
        with lock:
            i += 1
            print('正在解析:NO.{}'.format(i))
        re_queue.put_nowait(data)

    def save_to_tb(self, db, table, data):
        db.save_one_data(table, data)

    def save_to_db(self, args):
        db = DbMysql(configs.TEST_DB)
        table = 'detail'
        while 1:
            try:
                data = re_queue.get_nowait()
                self.save_to_tb(db, table, data)
            except Exception as e:
                print(e)
                break
        log.info('good body~')

    def run(self):
        urls = self.get_urls
        with Pool(max_workers=100) as pool:
            pool.map(self.parse_detail, urls)

        print(re_queue.qsize())
        with Pool(max_workers=20) as pool:
            pool.map(self.save_to_db, range(20))


if __name__ == '__main__':
    t1 = time.time()
    spider = detail_spider()
    spider.run()
    print('time:{}'.format(time.time() - t1))
    log.info('time:{}'.format(time.time() - t1))
