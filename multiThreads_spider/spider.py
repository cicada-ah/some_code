
import requests
from lxml import etree
from threading import Thread,RLock
import os,time
import re
import ips,random


headers={
	'User-Agent':'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36',
}
class myThread (Thread):
	def __init__(self, url, pages, class_posts, newdir, CrawledURLs):
		Thread.__init__(self)
		self.url = url
		self.newdir = newdir
		self.class_posts = class_posts
		self.CrawledURLs = CrawledURLs
		self.pages = pages
		self.lock = RLock()
	def run(self):
		details_spider(self.url, self.pages, self.class_posts, self.newdir, self.CrawledURLs, self.lock)

def isexit(newurl, CrawledURLs):
	return newurl in CrawledURLs


def get_requests(url, proxies=None):
	try:
		response = requests.get(url, headers=headers, proxies=proxies, timeout=1)
		if response.status_code == requests.codes.ok:
			time.sleep(random.random()+0.5)
			response.encoding = 'gb2312'
			return response.text
		raise 'error'
	except:
		print('Connection refused by the server...')
		proxies = {'http':random.choice(ips.ips)}
		return get_requests(url, proxies=proxies)
# else:
	# 	return 'error'


def details_spider(url, pages, class_posts, newdir, CrawledURLs, lock):
	print('Parsing classification: {}{}...'.format(class_posts,str(pages)))
	page = get_requests(url)
	# if page == 'error':
	# 	print('Parsing classification: {}{}out time...'.format(class_posts,str(pages)))
	# 	return
	CrawledURLs.append(url)
	tree = etree.HTML(page)
	posts_url = tree.xpath('//div[@class="listitem"]/ul/li/a/@href')
	detail_spider(posts_url, newdir, CrawledURLs, lock)
	pattern = re.compile(r"<a href='(.*?)'>下一页</a>")
	reslut = re.findall(pattern,page)
	print('Analytic classification: {}{} finished.'.format(class_posts,str(pages)))
	if reslut:
		newurl = 'http://www.meiwenting.com'+reslut[0]
		if not isexit(newurl,CrawledURLs):
			pages += 1
			return details_spider(newurl, pages, class_posts, newdir, CrawledURLs, lock)
	print('Analytic classification: {} finished.'.format(class_posts))

def detail_spider(posts_url, newdir, CrawledURLs, lock):
	for post_url in posts_url:
		if not isexit(posts_url,CrawledURLs):
			page = get_requests(post_url)
			CrawledURLs.append(post_url)
			# if page == 'error':
			# 	print('{} parse fail ...'.format(post_url))
			# 	continue
			tree = etree.HTML(page)
			title = tree.xpath('//div[@class="title"]/h1/text()')[0].replace("/"," ")\
																.replace("\\"," ")\
																.replace(":"," ")\
																.replace("*"," ")\
																.replace("?"," ")\
																.replace("\""," ")\
																.replace("<", " ") \
																.replace(">", " ")\
																.replace("|", " ")
			body = ''.join(tree.xpath('//div[@id="content"]/p/text()'))
			lock.acquire()
			filedir = newdir+'\\'+title+'.txt'
			with open(filedir, 'w', encoding='utf-8') as fd:
				print(filedir)
				fd.write(title+'\n'+body)
			lock.release()
		else:
			continue


def create_dir(classes_posts):
	if  not os.path.exists('beautiful posts'):
		os.mkdir('beautiful posts')
	os.chdir('beautiful posts')
	[os.mkdir(class_posts) for class_posts in classes_posts]
	print('文件夹创建完毕！')
	return os.getcwd()

def pig_run_faster():
	first_url = 'http://www.meiwenting.com'
	page = get_requests(first_url)
	# if page == 'error':
	# 	print('首页失效咯,换网站吧~QAQ')
	tree = etree.HTML(page)
	classes_posts = tree.xpath('//div[@class="subnav"]/ul/li/a/text()')
	print(classes_posts)
	class_urls = tree.xpath('//div[@class="subnav"]/ul/li/a/@href')
	file_dir = create_dir(classes_posts)
	half_len = int(1/2*len(class_urls))
	thread1 = []
	thread2 = []
	CrawledURLs = []
	print('collect the half ...')
	page = 0
	for i in range(half_len):
		newdir = file_dir+'\\'+classes_posts[i]
		t = myThread(class_urls[i], page, classes_posts[i], newdir, CrawledURLs)
		thread1.append(t)
		t.setDaemon(True)
		t.start()
	for t in thread1:
		t.join()
	print('already collect half of all ...')
	time.sleep(5)
	pages = 0
	for k in range(half_len,len(class_urls)):
		newdir = file_dir+'\\'+classes_posts[k]
		t = myThread(class_urls[k], pages, classes_posts[k], newdir, CrawledURLs)
		thread2.append(t)
		t.setDaemon(True)
		t.start()
	for t in thread2:
		t.join()
	print('already collect all.')

if __name__ == '__main__':
	pig_run_faster()




