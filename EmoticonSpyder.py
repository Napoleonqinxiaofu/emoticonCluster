#_*_coding:utf-8_*_
import requests
from bs4 import BeautifulSoup as BS
import re

def analyse(url):
	try:
		response = requests.get(url, timeout=5)
		doc = BS(response.content, 'html.parser')
		allMoreElement = doc.find_all(class_='fColor')
		for more in allMoreElement:
			a = more.find_all('a')
			if len(a) == 2:
				print(a[1]['href'])
	except Exception as e:
		print(e)

if __name__ == '__main__':
	analyse('http://md.itlun.cn/')