#_*_coding:utf-8_*_
# author : xiaofu.qin
# description : Download image from baidu Image website.
import cv2
import numpy
import requests
import urllib
import re
import os
import sys
import time

# 引入file.py文件
import util

# 下面两个变量是百度对图片的原网址进行编码的解码方式
str_table = {
    '_z2C$q': ':',
    '_z&e3B': '.',
    'AzdH3F': '/'
}
char_table = {
    'w': 'a',
    'k': 'b',
    'v': 'c',
    '1': 'd',
    'j': 'e',
    'u': 'f',
    '2': 'g',
    'i': 'h',
    't': 'i',
    '3': 'j',
    'h': 'k',
    's': 'l',
    '4': 'm',
    'g': 'n',
    '5': 'o',
    'r': 'p',
    'q': 'q',
    '6': 'r',
    'f': 's',
    'p': 't',
    '7': 'u',
    'e': 'v',
    'o': 'w',
    '8': '1',
    'd': '2',
    'n': '3',
    '9': '4',
    'c': '5',
    'm': '6',
    '0': '7',
    'b': '8',
    'l': '9',
    'a': '0'
}

char_table = {ord(key):ord(value) for key, value in char_table.items()}


def decodeUrl(url):
	"""
	对百度图片中的objURL地址进行解码
	:param url:  原来的objUrl，这是解密过的
	:return:
	"""
	for key, value in str_table.items():
		url = url.replace(key, value)

	# 替换字符
	return url.translate(char_table)


def buildUrls(words, maxRequestTime=10):
	"""
	构建百度图片ajax请求地址。
	:param words:  请求关键词
	:param maxRequestTime:需要构建ajax请求的数量
	:return:
	"""
	words = urllib.quote(words)
	url = r"http://image.baidu.com/search/acjson?tn=resultjson_com&ipn=rj&ct=201326592&fp=result&queryWord={word}&cl=2&lm=-1&ie=utf-8&oe=utf-8&st=-1&ic=0&word={word}&face=0&istype=2nc=1&pn={pn}&rn=60"
	urls = [url.format(word=words, pn=x*60) for x in range(0, maxRequestTime)]
	return urls

def requestAjax(url):
	"""
	请求百度图片的ajax，获得其返回的json数据
	:param url:  ajax请求地址
	:return: 一个保存所有图片源地址的列表
	"""
	objUrls = []
	try:
		response = requests.get(url, timeout=5)
		response.encoding = 'utf-8'
		if response.status_code == 200:
			# 请求成功
			jsonData = response.json()['data']
			# 有的时候最后一个是一个空的dict，所以需要注意一下
			objUrls = [decodeUrl(s['objURL']) for s in jsonData if s and re.search(r'jpg|png$', s['middleURL'], re.I)]
	except Exception as e:
		print('Fail to get origin url of image.')
		print(e)

	return objUrls

def saveToImage(path, response):
	"""
	将requests的请求响应中提取信息并将其保存为path的图片
	:param path: 保存到本地的图片路径
	:param response: 响应包
	:return:
	"""
	with open(path, 'wb') as f:
		for chunk in response.iter_content(chunk_size=128):
			f.write(chunk)
	
def downloadImage(url, path):
	"""
	下载图片，并将其保存到path路径下
	:param url:  图片URL
	:param path:  本地图片地址
	:return: 成功1，失败None
	"""
	try:
		# 设置相应的最长时间为5s，超过该时间限制则会抛出错误，但是在try语句中则不会中值程序的运行
		response = requests.get(url, stream=True, timeout=5)
		response.encoding = 'utf-8'
		if response.status_code != 200:
			print('Fail to download ')
			return None
		saveToImage(path, response)
		print('Successful download')

		result = 1

	except Exception as e:
		print(e)
		print('Fail to download' )
		result = None
	
	return result

def main(word, folder):
	"""
	整合上述所有函数进行对百度图片的爬取。
	:param word:  需要爬取的图片的关键词
	:param folder: 将关键词下的图片保存到folder文件夹下
	:return:
	"""
	# 构建ajax请求地址
	ajaxUrls = buildUrls(word)
	
	# 创建文件夹
	util.mkDir(folder)
	
	# 遍历所有的ajaxUrls元素，真正请求这个ajax地址，然后获取图片的源地址
	for i, ajax in enumerate(ajaxUrls):
		objUrls = requestAjax(ajax)
		
		for index, url in enumerate(objUrls):
			current = index + i * 60 + 1
			imageName = str(current) + '.jpg'
			imageName = os.path.join(folder, imageName)
			
			# 文件名已经存在，则加上一个时间戳
			if util.fileExist(imageName):
				imageName = os.path.join(folder, str(int(time.time())) + str(current) + '.jpg')
			
			downloadImage(url, imageName)

if __name__ == '__main__':
	import cluster

	# texts = util.readLine('keywords_brief_extend.txt')
	#
	# folder = r'F:/emoticonData/ANewData'
	# # folder = r'H:/emoticon/jinguanzhang'
	# count = 0
	# for text in texts:
	# 	count += 1
	# 	# 将中文转化成拼音
	# 	folderName = util.translateToPinYin(text)
	#
	# 	# 如果文件夹已经存在，那么说明已经下载过了，不要再次进行下载
	# 	if util.dirExist(os.path.join(folder, folderName)):
	# 		print("%s is exists" % (os.path.join(folder, folderName)))
	# 		continue
	# 	# 调用主函数进行下载
	# 	main(text, os.path.join(folder, folderName))
	#
	# # 最后的时候调用cluster.py的分类函数
	# cluster.classification()
	
	# main(r'表情包', os.path.join(r"H:/emoticon", 'biaoqingbao'))
	cluster.classification(folder=r"H:/emoticon/biaoqingbao")