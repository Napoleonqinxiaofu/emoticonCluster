#_*_coding:utf-8_*_
# author : xiaofu.qin
# description : 使用requests来请求百度云上网络图片文字识别的demo，这样就可以省钱了
import requests
import shutil
import base64
import os
import re
import random
import time

import util

import sys
reload(sys)
sys.setdefaultencoding('utf8')


# 浏览器useragent大全
userAgent = [
	"Mozilla/5.0 (Windows NT 5.2) AppleWebKit/534.30 (KHTML, like Gecko) Chrome/12.0.742.122 Safari/534.30",
	"Mozilla/5.0 (Windows NT 5.1; rv:5.0) Gecko/20100101 Firefox/5.0",
	"Opera/9.80 (Windows NT 5.1; U; zh-cn) Presto/2.9.168 Version/11.50",
	"Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1)",
	"Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0; .NET CLR 2.0.50727; .NET CLR 3.0.04506.648; .NET CLR 3.5.21022; .NET4.0E; .NET CLR 3.0.4506.2152; .NET CLR 3.5.30729; .NET4.0C)",
	"Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN) AppleWebKit/533.21.1 (KHTML, like Gecko) Version/5.0.5 Safari/533.21.1",
	"Mozilla/5.0 (Windows; U; Windows NT 5.1; ) AppleWebKit/534.12 (KHTML, like Gecko) Maxthon/3.0 Safari/534.12",
	"Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; .NET CLR 2.0.50727; TheWorld)",
	"Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"
]

def readImage(path):
	"""
	读取一张图片并将其转化成base64格式
	:param path:  图片路径
	:return: base64ImageData
	"""
	if not os.path.isfile(path):
		return None
	with open(path, 'rb') as fs:
		return "data:image/jpeg;base64," + base64.b64encode(fs.read())

def requestBaidu(imageBase64Data):
	"""
	请求百度云网络图片文字识别的Demo页面
	:param imageBase64Data: base64格式图片
	:return: 请求成功返回请求的json，否则返回None
	"""
	global userAgent
	url = "https://cloud.baidu.com/aidemo"
	formData = {
		"type" : "webimage",
		"image_url" : "",
		"image" : imageBase64Data
	}
	# 伪造IP，看看百度有没有识别出来
	IPs = util.readLine('ip.txt')
	fadeIPs = [IPs.next() for i in range(100)]
	try:
		proxies = {
			"http": random.choice(fadeIPs)
		}
		header = {
			'User-Agent': random.choice(userAgent)
		}
		r = requests.post(url, proxies=proxies, headers=header, data=formData, timeout=5)

		response = r.json()
		# print(response.get('msg').encode('gbk'))
	except Exception as e:
		response = None
		print(e, "Error in request function")

	return response

def getResult(response):
	"""
	从requests请求结果中提取识别到的文字（不一定能识别出来）
	:param response: requests请求结果，如果请求不成功，则为None
	:return: 返回一个数组，每一个元素都是识别出来的文字结果,没有识别到文字，但是正确请求了的范湖空数组；出了错就返回相应错误码
	"""
	result = []
	# 传递进来的是None的话就直接走吧
	if response is None:
		return result
	error = response.get('errno', 1)
	# 出现这个错误说明请求次数太多，等会儿
	if error == 102:
		print("Please wait for 30 minutes.")
		time.sleep(30 * 60)
	# 如果出现了错误直接返回
	if error > 0:
		print(response.get('msg'))
		return error

	# 获取结果,得放在try中，毕竟错误极有可能发生
	try:
		words = response.get('data', {}).get('words_result')
		for w in words:
			result.append(w.get('words', 'no words'))
	except Exception as e:
		print(e, 'Error in getResult function')
		pass

	return result

# 提取结果集中的有用的信息，顺便把信息存储这些信息到某一个文件下
def saveResult(result, originImagePath, logFile):
	"""
	将提取到的结果集中保存到某一个日志文件中，因为没有数据库，只能这样了。
	:param result: 保存识别结果的数组
	:param originImagePath:  待识别图片的路径，用于与识别结果一一对应
	:param logFile:  日志文件路径
	:return: None
	"""
	try:
		result = '-'.join(result)
	except Exception as e:
		print(e)
		result = ''
	result = originImagePath + "==>" + result + "\r\n"
	util.write(logFile, result)


# 将filePath移动到targetFolder目录下，顺便把原来的filePath删除了
def moveFile(filePath, targetFolder):
	"""
	某一张图片识别出结果之后将该图片移动至某一个文件夹下，并将原来的图像删除掉
	:param filePath:  图片路径
	:param targetFolder:  需要移动到的文件夹名称
	:return:  None
	"""
	# 移动文件
	util.movoToDir(filePath, targetFolder)

	# 删除原文件
	util.deleteFile(filePath)

def main(folder):
	"""
	主函数，负责全局调用上述的所有函数
	:param folder:  文件夹的路径，需要识别该文件夹下的所有图片。
	:return: None
	"""
	paths = [os.path.join(folder, item) for item in os.listdir(folder)]
	paths = [fileName for fileName in paths if util.isSuitableImageType(fileName)]
	# 设置接收已经识别的图片的文件夹
	targetFolder = os.path.join(folder, 'final')
	# 先前没有过这个文件夹则创建之，在该函数内部已经有了判断文件夹是否存在的逻辑
	util.mkDir(targetFolder)
	# 根据folder文件夹的名称生成一个日志文件名称
	logFile = util.generateLogName(folder)

	# 如果有先前的文件，那就换一个名称
	if os.path.isfile(logFile):
		logFile = logFile.replace('.txt', 'Log.txt')

	for image in paths:
		imageData = readImage(image)
		response = requestBaidu(imageData)
		# 请求有误，跳过当前循环
		if response is None:
			continue
		
		result = getResult(response)
		# 如果获取不到结果，返回的是一个error(大于0的值)，则continue
		if isinstance(result, int) and result > 0:
			print(result)
			print("Too many requests, Please try later.")
			continue
	
		saveResult(result, image, logFile)
		moveFile(image, targetFolder)

		try:
			print("-".join(result))
		except Exception as e:
			print(e)


if __name__ == "__main__":
	parentFolder = r"F:/emoticonData"

	folders = [
				os.path.join(parentFolder, item) \
				for item in os.listdir(parentFolder) \
				if os.path.isdir(os.path.join(parentFolder, item))
			]
	
	for folder in folders:
		print(folder)
		main(folder)