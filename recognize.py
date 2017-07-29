#_*_coding:utf-8_*_
# author : xiaofu.qin
# description : 使用百度云的网络图片文字识别来识别表情包的图片
# 引入文字识别OCR SDK
from aip import AipOcr
import os
import file

import util

import sys
reload(sys)
sys.setdefaultencoding('utf8')

def requestBaiduApi(imageData):
	"""
	请求百度云上的网络图片文字识别API
	:param base64Image: 图片数据
	:return:
	"""
	# 定义常量
	APP_ID = '9818457'
	API_KEY = 'kFtGii157YTtbgD6iSdwYQuf'
	SECRET_KEY = 'sRyxSiXiTEcDSehNnY6quiNaPxPxsfjx'
	
	# 初始化ApiOcr对象
	aipOcr = AipOcr(APP_ID, API_KEY, SECRET_KEY)
	try:
		# 开始请求
		result = aipOcr.webImage(imageData)
	except Exception as e:
		print(e)
		result = {"error_code": 282810}
	return result


def getResult(result):
	"""
	从百度API返回的json格式中提取所有的图片文字信息。
	:param result: 一个包含所有文字的数组
	:return:
	"""
	words = []
	error = result.get("error_code", 0)
	if error != 0:
		print(error)
		return words
	
	words_result_num = result.get('words_result_num', 0)
	
	if words_result_num == 0:
		return words
	
	for word in result['words_result']:
		words.append(word['words'])
	
	return words

# 使用百度的AipOcr来请求识别网络图片
# base64Img base64格式的图片
# imagePath 当前请求的图片的路径
# logFileName 获得图片上的文字之后需要保存到本地文件中，这就是文件名称
def recognize(base64Img, imagePath, logFileName):
	# 定义常量
	APP_ID = '9818457'
	API_KEY = 'kFtGii157YTtbgD6iSdwYQuf'
	SECRET_KEY = 'sRyxSiXiTEcDSehNnY6quiNaPxPxsfjx'

	# 初始化ApiOcr对象
	aipOcr = AipOcr(APP_ID, API_KEY, SECRET_KEY)
	try:
		# 开始请求
		result = aipOcr.webImage(base64Img)
	except Exception as e:
		print(e)
		result = {"error_code", 216201}

	error_code = result.get('error_code', None)

	# 请求有误或者参数不对之类的一大堆原因都会得到error的结果
	if error_code is not None:
		return error_code
		
	words_result_num = result.get('words_result_num', 0)
	words = []
	if words_result_num == 0:
		return words

	# 给allWords的前面加上每一张图片的路径信息
	allWords = imagePath + "==>"

	for word in result['words_result']:
		# 获取文字,多行文字使用_*_隔开
		allWords += word['words'] + "_*_"
	allWords += "printn"
	print(allWords.encode('gbk'))

	file.fileOperate.write(logFileName, allWords)

# 读取图片
def readImage(path):
	with open(path, 'rb') as fs:
		return fs.read()

# 获得某一个文件夹下的所有图片的路径
def getImagePath(folder):
	if not util.dirExist(folder):
		return []
	paths = [os.path.join(folder, item) for item in os.listdir(folder)]
	return [fileName for fileName in paths \
	        if not util.isDir(fileName) and util.isSuitableImageType(fileName)]

# 主函数
# folder 需要识别的图片所在的文件夹
def main(folder):
	paths = getImagePath(folder)
	logName = util.generateLogName(folder)
	targetFolder = os.path.join(folder, "final")
	util.mkDir(targetFolder)

	for index, p in enumerate(paths):
		imageData= readImage(p)
		result = requestBaiduApi(imageData)
		words = getResult(result)
		try:
			result = '-'.join(words)
		except Exception as e:
			result = ""
		print(result.encode("utf8"))
		result = p + result + "/n"
		util.write(logName, result)
		
		# 将该文件移入某一个文件夹并删掉当前文件
		util.movoToDir(p, targetFolder)
		util.deleteFile(p)

if __name__ == "__main__":
	folder = r'F:/emoticonData/ANewData/doutu'

	main(folder)