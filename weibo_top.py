import os
import re
import requests
from datetime import datetime

url = 'https://s.weibo.com/top/summary'
headers = {
    'Cookie': 'SINAGLOBAL=9984350838163.459.1639458131480; SCF=AhYJZS5_n-2dh-fzeiiEVulWxpdZqWntw9i3SlVXNoxUIwSAX-FUf5SDiBpHtfE-fZIQiT60J8BRFNKo9qXG5VY.; UOR=github.com,s.weibo.com,github.com; _s_tentry=-; Apache=2340719057363.756.1686489602759; ULV=1686489602775:60:1:1:2340719057363.756.1686489602759:1682592070172; SUB=_2A25Jgbp1DeRhGeBL6FMR-CrEyDiIHXVq9qy9rDV8PUNbmtANLVbSkW9NRzPQ6IXxzIoCo2ERDJo3MZKTEEUHcYX6; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WWO7Xc2TqZUpUycnXX6JX6G5JpX5KzhUgL.Foqfe0271hBRe0B2dJLoI05LxK.L1KnLB.qLxKnLBK-LB.qLxK-L1K5LBKMLxKqL12zL1h.LxKqL12zL1hLaUJYt; ALF=1718025636; SSOLoginState=1686489637',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'
}
response = requests.get(url, headers=headers).text
href = re.findall(r'<a href="(/weibo\?q=.*&Refer=top)" target="_blank">(.*?)</a>[\s]*<span> (.*?)</span>', response)
# 时间格式，用于命名
date = datetime.now().strftime("%Y-%m-%d")
time = datetime.now().strftime("%x-%X")
# 储存原始数据
for item in href:
    baseurl, title, index = item
    url = 'https://s.weibo.com/'+baseurl
    with open('../weibo_data/'+date+'-origin.md', 'a')as f:
        f.write('['+title+']'+'('+url+')'+' '+index+"\r\n")
# 从本地读取原始数据并去掉空元素
with open('../weibo_data/'+date+'-origin.md', 'r')as f:
    datalist = f.read().split('\n')
if '' in datalist:
    while '' in datalist:
        datalist.remove('')
# 新建字典暂存
counts = {}
for k in range(len(datalist)):
    t = datalist[k].split(']')[0].split('[')[1]   # 标题
    d = datalist[k].split(' ')[-1]  # 热度
    u = datalist[k].split('](')[1].split(')')[0]  # 链接
    # 以热度为键
    counts[int(d)] = u+', '+t
# 热度降序
items = list(counts.items())
items.sort(key=lambda x: int(x[0]), reverse=True)
# 获取相同标题的键
repeatindex = []
for i in range(len(items)):
    for k in range(i+1, len(items)):
        if items[i][1].split(', ')[-1] == items[k][1].split(', ')[-1]:
            repeatindex.append(items[k][0])
# 去重
for i in set(repeatindex):
    counts.pop(i)
# 储存整理好的数据，按热度降序
if os.path.exists('../weibo_top/result/'+date+'.md'):
    os.remove('../weibo_top/result/'+date+'.md')
index = 0
for i in sorted(counts, reverse=True):
    index += 1
    with open('../weibo_top/result/'+date+'.md', 'a')as f:
        f.write(str(index)+'. '+'['+counts[i].split(', ')[1]+']'+'('+counts[i].split(', ')[0]+')'+' '+str(i)+"\r\n")
item_start = """weibo_top  
---
每十分钟爬取一次微博热搜  

上过热搜的标题和链接都可以记录， 而不仅仅是Top50

正式从2021/12/17开始记录  

*归档[./result](./result/)*

# 今日热门搜索  
"""
item_end = """# 更新日志  
2021/12/16  简化代码,减少生成文件  
2021/12/17  获取话题一天中最高热度  
2022/03/28  在3/27 下午六点—3/28 下午三点期间服务器故障 无法更新期间的微博  
# 声明  
本项目的所有数据来源均来自 [新浪微博热搜榜](https://s.weibo.com/top/summary)  

# LICENSE
该源码使用 Apache License 2.0 发布，具体内容请查看 [LICENSE](./LICENSE)
"""
with open('../weibo_top/result/'+date+'.md', 'r+')as f:
    content = f.read()
if os.path.exists('../weibo_top/README.md'):
    os.remove('../weibo_top/README.md')
with open('../weibo_top/README.md', 'a')as f:
    f.write(item_start+content+item_end)
print("Completed")
print(time)
