
import requests
from lxml import etree
from threading import Thread
def get_ips(page):
    print(page)
    headers={
        'User-Agent':'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36',
    }
    url = 'http://www.kuaidaili.com/free/inha/{}/'.format(page)
    url_confirm = 'http://blog.csdn.net'
    r = requests.get(url=url, headers=headers)
    tree = etree.HTML(r.text)
    result_ip = tree.xpath("//tbody/tr/td[@data-title='IP']/text()")
    result_port = tree.xpath("//tbody/tr/td[@data-title='PORT']/text()")
    ips = [k+':'+v for k in result_ip for v in result_port]
    for ip in ips:
        try:
            r = requests.get(url=url_confirm, headers=headers, proxies={'http':ip}, timeout=0.5)
            print('"http://{}",'.format(ip))
        except:
            continue


if __name__ == '__main__':
    threads = []

    for i in range(1,5):
        t = Thread(target=get_ips,args=(i,))
        threads.append(t)
        t.start()

    for t in  threads:
        t.join()