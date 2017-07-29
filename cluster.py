#_*_coding:utf-8_*_
# author : xiaofu.qin
# description : 使用opencv的聚类算法将图片进行聚类
import cv2
import numpy
from matplotlib import pyplot as plt
import os
import re
import shutil

# 引入自己写的文件
import filterImage as FI
import util

def thumbnailCollect(imgs, name='fig1'):
	"""
		显示多张缩略图的集合
	"""
	plt.figure(name)
	column = 10
	row = len(imgs) // column + 1
	for index, image in enumerate(imgs):
		plt.subplot(row, column, index+1)
		plt.imshow(image)
		plt.xticks([])
		plt.yticks([])
	plt.show()

def showImage(img):
	cv2.imshow('img', img)
	cv2.waitKey(400) & 0XFF

def createDirs(folder):
	# 在目标文件夹下创建四个子文件夹classAA、classAB、classBA，classBB
	[util.mkDir(os.path.join(folder, dirName)) for dirName in ['classAA', 'classAB', 'classBA', 'classBB']]

class cluster(object):
	"""
		聚类分类
	"""
	def __init__(self, maxIter=20, isDebug=False):
		"""
		初始化函数
		:param maxIter: 最高迭代次数
		:param isDebug:  是否在运行中向控制台打印一些运行信息，默认为False，不打印
		"""
		#随时labels命名，但是其中保存的是每一个图片的绝对地址
		self.labls = None
		# 存储需要聚类的数据用的
		self.data = None
		# 最高的迭代次数
		self.maxIter = maxIter
		# opencv聚类函数的其中一个参数
		self.criteria = (cv2.TERM_CRITERIA_EPS+cv2.TERM_CRITERIA_MAX_ITER, self.maxIter, 1.0)
		# 初始化簇中心点的方式——随机
		self.initCenterType = cv2.KMEANS_RANDOM_CENTERS

		# 是否在程序运行的时候打印一些信息,默认不打印
		self.isDebug = isDebug

	def train(self, folderOrPaths, K=2):
		self.data = []
		self.label = []
		self.log('Starting read images from disk..............')
		# 这一步获取图片数据和它们的标签
		self._getTrainData(folderOrPaths)
		self.log('Training..............')
		# ret为每一个点与各自的簇中心的距离，result为聚类的结果，center为簇中心点坐标（向量）
		try:
			ret, result, center = cv2.kmeans(self.data, K, self.criteria, 10, self.initCenterType)
			result = result.ravel()
			classA = self.label[result==0]
			classB = self.label[result==1]

			return (classA, classB)
		except Exception as e:
			print(e)
			return None

	def _getTrainData(self, folderOrPaths):
		# 如果传递的字符串，则表示传递的目录名称，否则传递的是包含所有图片的地址的列表
		if isinstance(folderOrPaths, str):
			labels = self._getTrainLabels(folderOrPaths)
			flag = 0
		else:
			labels = folderOrPaths
			flag = 1
		for path in labels:
			try:
				img = cv2.imread(path, 0)
				mask = FI.feature.mask(img, ratio=0.06)
				# 如果flag为0的话，则获取归一化之后非概率的向量，这也是默认的值
				if flag == 0:
					hist = FI.feature.normalizeWithRange(img, mask)
				else:
					hist = FI.feature.normalizeWithPro(img, mask)

				self.data.append(hist)
				self.label.append(path)
			except Exception as e:
				print(e)
		self.data = numpy.float32(self.data)
		self.label = numpy.array(self.label)

	def _getTrainLabels(self, folder):
		return [os.path.join(folder, s) for s in os.listdir(folder) if s.endswith('jpg')]

	def log(self, string):
		if self.isDebug:
			print(string)

def classification(folder):
	clusterIns = cluster(isDebug=True)
	if util.dirExist(os.path.join(folder, 'classAA')):
		return
	# 在目标文件夹下创建四个文件夹——classAA、classAB、classBA、classBB
	# createDirs(folder)

	resultLevelOne = None
	# 第一次聚类
	# try:
	# 	resultLevelOne = clusterIns.train(folder)
	# 	print(resultLevelOne)
	# except Exception as e:
	# 	print(e)
	
	resultLevelOne = clusterIns.train(folder)
	
	if resultLevelOne is not None:
		# 对第一次聚类的第一个结果再次进行聚类
		result = clusterIns.train(resultLevelOne[0])
		if result is not None:
			util.moveToDir(result[0], os.path.join(folder, 'classAA'))
			util.moveToDir(result[1], os.path.join(folder, 'classAB'))
		# 对第一次聚类的结果的第二个结果再次进行聚类
		result = clusterIns.train(resultLevelOne[1])
		if result is not None:
			util.moveToDir(result[0], os.path.join(folder, 'classBA'))
			util.moveToDir(result[1], os.path.join(folder, 'classBB'))

if __name__ == '__main__':
	classification(folder=r"F:/emoticonData/ANewData")