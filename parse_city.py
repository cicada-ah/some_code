import requests,re
from pprint import pprint
def main():
	url = 'https://kyfw.12306.cn/otn/resources/js/framework/station_name.js?station_version=1.9030'
	resp = requests.get(url,verify=False)
	pattern = u'([\u4e00-\u9fa5]+)\|([A-Z]+)'
	result = dict(re.findall(pattern, resp.text))
	print(result.keys())
	print(result.values())
if __name__ == '__main__':
	main()