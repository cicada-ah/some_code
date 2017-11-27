from DBmodel.DBMysql import DbMysql
from configs import configs
from pyecharts import Geo, Pie
db = DbMysql(configs.TEST_DB)
all_data = db.find_all('detail')
c = p = js = j = 0
data_positions1 = []
attr1 = []
value1 = []

# 及其随意的for循环
for data in all_data:
    if 'python' in (data['detail'].lower() or data['position'].lower()) and len(data['job_position']) <= 2 and data['job_position'] != '全国':
        data_positions1.append(data['job_position'])
        p += 1
    if 'java' in (data['detail'].lower() or data['position'].lower()) and len(data['job_position']) <= 2 and data['job_position'] != '全国':
        data_positions1.append(data['job_position'])
        j += 1
    if 'javascript' in (data['detail'].lower() or data['position'].lower()) and len(data['job_position']) <= 2 and data['job_position'] != '全国':
        data_positions1.append(data['job_position'])
        js += 1
    if 'c++' in (data['detail'].lower() or data['position'].lower()) and len(data['job_position']) <= 2 and data['job_position'] != '全国':
        data_positions1.append(data['job_position'])
        c += 1

myset1 = set(data_positions1)
for item in myset1:
    attr1.append(item)
    value1.append(data_positions1.count(item))


geo = Geo("Python各地实习招聘数", "data from sxc", title_color="#fff", title_pos="center",
          width=1200, height=600, background_color='#404a59')
geo.add("", attr1, value1, visual_range=[min(value1), max(value1)], visual_text_color="#fff",
        symbol_size=15, is_visualmap=True, is_piecewise=True, visual_split_number=3)
geo.render('chart_Python.html')

attr_all = ['c++', 'Javascript', 'Python', 'Java']
v = [c, js, p, j]
pie = Pie('各语言占4门需求总和')
pie.add('', attr_all, v, is_label_show=True, is_random=True, radius=[
        30, 75], rosetype='radius')
pie.render('chart_pie.html')
