#codingor utf-8

"""命令行火车票查看器

Usage:
	tickets [-gdtkz] <from> <to> <date>

Options:
	-h,--help   显示帮助菜单
	-g          高铁
	-d          动车
	-t          特快
	-k          快速
	-z          直达
Ex:
	-gtd 西安 乌鲁木齐 2017-11-12

"""

from docopt import docopt
import citys
import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
from prettytable import PrettyTable
from colorama import Fore
import colorama
from datetime import datetime,timedelta
colorama.init()
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

class spider_tickets(object):
	url_template =('https://kyfw.12306.cn/otn/leftTicket/query?leftTicketDTO.train_date={}'
	'&leftTicketDTO.from_station={}'
	'&leftTicketDTO.to_station={}'
	'&purpose_codes=ADULT'
	)

	def __init__(self):
		self.arguments = docopt(__doc__, version='Tickets 1.0')
		self.options = ''.join([key for key, value in self.arguments.items() if value is True])
		try:
			self.from_station = citys.get_code(self.arguments.get('<from>'))
			self.to_station  = citys.get_code(self.arguments.get('<to>'))
			self.date = self.arguments.get('<date>')
		except ValueError:
			print('输入查询条件有误，请重新输入！')
			exit()

	@property
	def del_url(self):
		url = self.url_template.format(self.date,self.from_station,self.to_station)
		return url
	
	def run(self):
		r = requests.get(self.del_url, verify = False)
		try:
			trains_masg = r.json()['data']['result']
		except:
			print('日期有误，请重新输入！')
			exit()
		TrainMasg(trains_masg,self.options).pretty_print()

class TrainMasg(object):
	def __init__(self,trains_masg,options):
		self.trains_masg = trains_masg
		self.options = options


	def get_from_to_name(self,data_list):
		from_station_telecode = data_list[6]
		to_station_telecode = data_list[7]
		return  '\n'.join([Fore.GREEN + citys.get_name(from_station_telecode) + Fore.RESET,Fore.CYAN + citys.get_name(to_station_telecode) + Fore.RESET])
	
	def get_start_arrive_time(self,data_list):
		start_time = data_list[8]
		arrive_time = data_list[9]	
		return '\n'.join([Fore.GREEN + start_time + Fore.RESET, Fore.CYAN + arrive_time + Fore.RESET])
	
	def parse_data(self,data_list):
			return{
			'station_train_code' : data_list[3],
			'from_to_station' : self.get_from_to_name(data_list),
			'start_arrive_time' :  self.get_start_arrive_time(data_list),
			'take_time' : data_list[10],
			'soft_sleep_num' : data_list[23] or "--",
			'hard_sleep_num' : data_list[28] or "--",
			'hard_seat_num' : data_list[29] or "--",
			'second_seat_num' : data_list[30] or "--",
			'first_seat_num' : data_list[31] or "--",
			'no_seat_num' : data_list[33] or "--",
			}
	@property
	def masg_del(self):
		for train_masg in self.trains_masg:
			data_list = train_masg.split('|')
			station_train_code = data_list[3]
			intitial = station_train_code[0].lower()
			if not self.options or intitial in self.options:
				yield self.parse_data(data_list).values()

	def pretty_print(self):
		pt = PrettyTable()
		pt.field_names = '车次 车站 时间 历时 一等座 二等座 软卧 硬卧 硬座 无座'.split()
		for train in self.masg_del:
			pt.add_row(train)
		print(pt)
if __name__ == '__main__':
	spider_tickets().run()