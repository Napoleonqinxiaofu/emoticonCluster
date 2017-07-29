#_*_coding:utf-8_*_
# author : xiaofu.qin
# description: 读取图片数据，

import cv2
import numpy
import os
import re
from pinyin import PinYin

# 为了解决unicode和ascii不兼容的情况
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

class File:
	def __init__():
		pass


def filterImage(folder):
	"""
		将某一个文件夹内的文件非图片过滤掉
	"""
	# 如果当前的文件名字是以数字开头的话，重命名的时候为了避免名字重复，以prevName为开头
	prevName = 'chars'
	nameLists = os.listdir(folder)
	for index, imageName in enumerate(nameLists):
		#if not imageName.endswith('jpg') :#and not imageName.endswith('png') and not imageName.endswith('bmp'):
		if re.search(r'(jpg|png|bmp)$', imageName, re.I) is None:
			# 删除文件
			os.remove(os.path.join(folder, imageName))
			continue
		fix = re.match(r'\.(jpg|png|bmp)$', imageName, re.I) 

		# 告诉Python当前的文件的目录在哪儿
		# os.chdir(os.path.dirname(os.path.join(folder,imageName)))

		if imageName.startswith('char'):
			# 对图片重命名
			newName = str(index + 1) + fix
			newName = os.path.join(folder, newName)
		else:
			newName = prevName + str(index + 1) + fix
			newName = os.path.join(folder, newName)
		oldName = os.path.join(folder, imageName)
		os.rename(oldName, newName)


class fileOperate(object):
	def __init__(self):
		pass

	@classmethod
	def read(cls, fileName, mode='r'):
		# 读取文件
		with open(fileName, mode) as f:
			for line in f:
				yield line.rstrip()
		
	@classmethod
	def write(cls, fileName, string, mode='a'):
		# 写入文件
		with open(fileName, mode) as f:
			f.write(string)


class util(object):
	# 工具类
	def __init__(self):
		pass

	@classmethod
	def mkDir(cls, dirName):
		# 创建文件夹
		if not os.path.exists(dirName):
			os.mkdir(dirName)

	@classmethod
	def translateToPinYin(cls, string):
		# 将中文转换成拼音
		test = PinYin()
		test.load_word()
		return ''.join(test.hanzi2pinyin(string=string))

	@classmethod
	def rename(cls, oldName, newName):
		os.rename(oldName, newName)

class console(object):
	"""
		打印信息类
	"""
	def __init__(self):
		pass

	@classmethod
	def log(cls, fileName, string):
		print("Writing.......")
		# 将字符串写入文件
		fileOperate.write(fileName, string + "\n")
		print('Writing done.')

if __name__ == '__main__':
	from pinyin import PinYin

	test = PinYin()
	test.load_word()
	print ''.join(test.hanzi2pinyin(string=r'脱衣服吧！好吗？'))

	print util.translateToPinYin('你好吗')