import os
import re
import requests
from datetime import datetime

url = 'https://s.weibo.com/top/summary'
headers = {'Cookie': 'SINAGLOBAL=9984350838163.459.1639458131480; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WWO7Xc2TqZUpUycnXX6JX6G5JpX5KMhUgL.Foqfe0271hBRe0B2dJLoI05LxK.L1KnLB.qLxKnLBK-LB.qLxK-L1K5LBKMLxKqL12zL1h.LxKqL12zL1hLaUJYt; UOR=github.com,s.weibo.com,login.sina.com.cn; SCF=AhYJZS5_n-2dh-fzeiiEVulWxpdZqWntw9i3SlVXNoxUaxg-Oo_kT_PbozJdKQ7Q1o4KkG7nUh_2Wa7onE2jC5s.; SUB=_2A25Jgq6ADeRhGeBL6FMR-CrEyDiIHXVq-YdIrDV8PUNbmtAGLU7ZkW9NRzPQ6G8vppG-s0zMazMMk6ltcs99gSKZ; ALF=1689152463; SSOLoginState=1686560464; _s_tentry=-; Apache=8094265020018.747.1686568888327; ULV=1686568888336:62:3:3:8094265020018.747.1686568888327:1686530733790', 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'}
response = requests.get(url, headers=headers, timeout=3).text
href = re.findall(
  r'<a href="(/weibo\?q=.*&Refer=top)" target="_blank">(.*?)</a>[\s]*<span> (.*?)</span>',
  response)
# 时间格式，用于命名
date = datetime.now().strftime("%Y-%m-%d")
# 储存原始数据
for item in href:
  baseurl, title, index = item
  url = 'https://s.weibo.com/' + baseurl
  with open('./weibo_data/' + date + '-origin.md', 'a') as f:
    f.write('[' + title + ']' + '(' + url + ')' + ' ' + index + "\r\n")
# 从本地读取原始数据并去掉空元素
with open('./weibo_data/' + date + '-origin.md', 'r') as f:
  datalist = f.read().split('\n')
if '' in datalist:
  while '' in datalist:
    datalist.remove('')
# 新建字典暂存
counts = {}
for k in range(len(datalist)):
  t = datalist[k].split(']')[0].split('[')[1]  # 标题
  d = datalist[k].split(' ')[-1]  # 热度
  u = datalist[k].split('](')[1].split(')')[0]  # 链接
  # 以热度为键
  counts[int(d)] = u + ', ' + t
# 热度降序
items = list(counts.items())
items.sort(key=lambda x: int(x[0]), reverse=True)
# 获取相同标题的键
repeatindex = []
for i in range(len(items)):
  for k in range(i + 1, len(items)):
    if items[i][1].split(', ')[-1] == items[k][1].split(', ')[-1]:
      repeatindex.append(items[k][0])
# 去重
for i in set(repeatindex):
  counts.pop(i)
# 储存整理好的数据，按热度降序
if os.path.exists('./spider/result/' + date + '.md'):
  os.remove('./spider/result/' + date + '.md')
index = 0
for i in sorted(counts, reverse=True):
  index += 1
  with open('./spider/result/' + date + '.md', 'a') as f:
    f.write(
      str(index) + '. ' + '[' + counts[i].split(', ')[1] + ']' + '(' +
      counts[i].split(', ')[0] + ')' + ' ' + str(i) + "\r\n")

print("Completed")
print(date)
