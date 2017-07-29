#_*_coding:utf-8_*_
# author : xiaofu.qin   
# create on {2017/7/22}
# description : 一些项目中常用的函数集合
import os
import shutil
import imghdr
from pinyin import PinYin
import random
import string

#====================================
# 文件相关的函数
#====================================
def readLine(fileName, mode='r'):
	"""
	读取某一个文件，返回一个迭代器，迭代器里面某一个元素则是文件的一行。
	:param fileName: 文件名称
	:param mode: 文件打开的方式，其实就是"只读"模式
	:return: iterator
	"""
	with open(fileName, mode) as f:
		for line in f:
			yield line.rstrip()

def write(fileName, content, mode='a'):
	# 写入文件
	with open(fileName, mode) as f:
		f.write(content)

def fileExist(fileName):
	return os.path.exists(fileName)

def deleteFile(fileName):
	if fileExist(fileName):
		os.remove(fileName)
		
def rename(oldName, newName):
	"""
	对文件重命名。
	:param oldName:
	:param newName:
	:return:
	"""
	os.rename(oldName, newName)
	
def movoToDir(filePaths, targetFolder):
	"""
	将文件复制到某一个文件夹下。
	:param filePaths: 需要复制的文件路径，可以是数组，也可以是字符串。
	:param targetFolder: 接受最终文件的文件夹
	:return:
	"""
	# 如果没有对应的文件夹，则创建之
	mkDir(targetFolder)
	if isinstance(filePaths, list):
		for p in filePaths:
			shutil.copy(p, targetFolder)
	elif isinstance(filePaths, str):
		shutil.copy(filePaths, targetFolder)

def isFile(fileName):
	return os.path.isfile(fileName)
		
#=================================
# 目录操作函数
#=================================
def isDir(dirName):
	return os.path.isdir(dirName)

def dirExist(dirName):
	"""
	判断目录是否存在
	:param dirName:
	:return:
	"""
	return os.path.exists(dirName)

def deleteDir(dirName):
	"""
	删除目录。
	:param dirName:
	:return:
	"""
	if dirExist(dirName):
		shutil.rmtree()

def mkDir(dirName):
	"""
	创建目录。
	:param dirName:
	:return:
	"""
	if not dirExist(dirName):
		os.mkdir(dirName)


#===============================
# 其他的常用的函数
#===============================
def translateToPinYin(content):
	# 将中文转换成拼音
	words = PinYin()
	words.load_word()
	return ''.join(words.hanzi2pinyin(string=content))

def generateLogName(folder):
	"""
	根据文件夹的名字生成一个日志文件名。
	:param folder:
	:return:
	"""
	if dirExist(folder):
		return os.path.join(folder, os.path.basename(folder) + '.txt')
	else:
		print('folder is not a local disk folder name, Please check it out.')
		return None
	
#=================================
# 图片相关函数
#=================================

def _imageType(fileName):
	"""
	获取图片类型
	:param fileName:
	:return:
	"""
	try:
		result = imghdr.what(fileName).lower()
	except Exception as e:
		result = False
	return result

def isSuitableImageType(fileName):
	"""
	判断图片类型是否是jpeg、png、jpg
	:param fileName:  需要判断的文件路径
	:return:  boolean，图片类型jpeg、png、jpg其中之一，返回True，否则返回False
	"""
	imageType = _imageType(fileName)
	suitable = ['jpeg', 'jpg', 'png']
	return imageType in suitable


#===============================
#
#===============================
def randomChars(y):
       return ''.join(random.choice(string.letters) for x in range(y))