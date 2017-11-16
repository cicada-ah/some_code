#coding: utf-8

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


"""

from docopt import docopt
import citys
import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
from prettytable import PrettyTable
from colorama import Fore
import colorama
from datetime import datetime
#在windows中导入Init 来处理colorama跨平台ANSI转义序列，在linux中不用
colorama.init()
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
#禁用警告,可以试试不带的效果
def cli():
	arguments = docopt(__doc__, version='Tickets 1.0')
	options = ''.join([key for key, value in arguments.items() if value is True])
	
	try:
		date = arguments.get('<date>')
		if datetime.strptime(date,'%Y-%m-%d') < datetime.now():
			print('日期有误，请重新输入！')
			raise ValueError
		from_station = citys.get_code(arguments.get('<from>'))
		to_station  = citys.get_code(arguments.get('<to>'))
	except ValueError:
		print('查询有误，请重新输入！')
		exit()

	url = ('https://kyfw.12306.cn/otn/leftTicket/query?leftTicketDTO.train_date={}&leftTicketDTO.from_station={}&leftTicketDTO.to_station={}&purpose_codes=ADULT'.format(date,from_station,to_station))
	r = requests.get(url, verify = False)
	trains_masg = r.json()['data']['result']

	pt = PrettyTable()
	pt.field_names = '车次 车站 时间 历时 一等座 二等座 软卧 硬卧 硬座 无座'.split()
	for train_masg in trains_masg:
		data_list = train_masg.split('|')
		station_train_code = data_list[3]
		intitial = station_train_code[0].lower()
		if not options or intitial in options:
			from_station_telecode = data_list[6]
			to_station_telecode = data_list[7]
			start_time = data_list[8]
			arrive_time = data_list[9]
			take_time = data_list[10]
			soft_sleep_num = data_list[23] or "--"
			hard_sleep_num = data_list[28] or "--"
			hard_seat_num = data_list[29] or "--"
			second_seat_num = data_list[30] or "--"
			first_seat_num = data_list[31] or "--"
			no_seat_num = data_list[33] or "--"
			pt.add_row([
				station_train_code,
				'\n'.join([Fore.GREEN + citys.get_name(from_station_telecode) + Fore.RESET,Fore.CYAN + citys.get_name(to_station_telecode) + Fore.RESET]),
				'\n'.join([Fore.GREEN + start_time + Fore.RESET, Fore.CYAN + arrive_time + Fore.RESET]),
				take_time,
				first_seat_num,
				second_seat_num,
				soft_sleep_num,
				hard_sleep_num,
				hard_seat_num,
				no_seat_num
				])
	print(pt)
if __name__ == '__main__':
	cli()