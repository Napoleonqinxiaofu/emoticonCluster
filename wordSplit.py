#_*_coding:utf-8_*_
# author :xiaofu.qin
# description : 使用百度的自然语言处理API来处理一下词语分类，以后好做图片分类

# 引入NLP SDK
from aip import AipNlp

# 定义常量
APP_ID = '9893591'
API_KEY = 'LiyY0LgBT1PGtw00QQoLStii'
SECRET_KEY = 'V64DVYBDzQWhTCAOOHILRV1yHTXLjFEA'

# 初始化AipNlp对象
aipNlp = AipNlp(APP_ID, API_KEY, SECRET_KEY)

import requests  # 导入requests模块用于访问测试自己的ip
import random
import util

IPs = util.readLine('ip.txt')
available = []
for ip in IPs:
	proxies = {
	  "http": ip
	}
	
	#  你的请求头信息
	header = {
	    'User-Agent':
		    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) ' +
		    'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
	}
	url = 'http://httpbin.org/ip'  # 你用于测试自己ip的网站
	try:
		request = requests.get(url, proxies=proxies, headers=header, timeout=5)  # 让问这个网页  随机生成一个ip
		util.write("availabelIP.txt", ip + "\n")
		request.encoding = request.apparent_encoding
		# 设置编码 encoding 返回的是请求头编码  apparent_encoding 是从内容网页中分析出的响应内容编码方式
		print(request.text)
	except Exception as e:
		print(e)