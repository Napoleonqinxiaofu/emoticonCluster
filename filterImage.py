#_*_coding:utf-8_*_
# author : xiaofu.qin
# description : 过滤图片，只留下大部分的简笔画——HOG, histogram(mask)
import os
import sys
import cv2
import numpy
from matplotlib import pyplot as plt


class feature(object):
	"""
		提取图片的特征
	"""
	def __init__(self):
		pass

	@classmethod
	def mask(cls, img, ratio=0.05):
		# 对图像进行掩膜--四周的5%
		h, w = img.shape[:2]
		mask = numpy.ones(img.shape[:2], numpy.uint8) * 255
		paddingW = int(w * ratio)
		paddingH = int(h * ratio)
		mask[paddingH:h-paddingH, paddingW:w-paddingW] = 0
		return mask

	@classmethod
	def normalizeWithPro(cls, img, mask=None):
		"""
			对图像提取直方图数据并归一化，归一化之后向量的每一个值代表的是概率，总和为1——normalize with probability
		"""
		hist = cv2.calcHist([img], [0], mask, [30], [0, 256]).ravel()
		total = hist.sum()
		return hist / total

	@classmethod
	def normalizeWithRange(cls, img, mask=None):
		"""
			对图像提取直方图数据并归一化，归一化之后向量中的每一个值仅仅是0到1之间的值。
		"""
		hist = cv2.calcHist([img], [0], mask, [30], [0, 256]).ravel()
		minV = hist.min()
		maxV = hist.max()
		return (hist - minV) / (maxV - minV)


def maskedImage(img, ratio=0.05):
	# 对图像进行掩膜--四周的5%
	h, w = img.shape[:2]
	mask = numpy.ones(img.shape[:2], numpy.uint8) * 255
	paddingW = int(w * ratio)
	paddingH = int(h * ratio)
	mask[paddingH:h-paddingH, paddingW:w-paddingW] = 0
	# return cv2.bitwise_and(img, img, mask = mask)
	return mask



def showHistogram(img, mask=None):
	hist = cv2.calcHist([img], [0], mask, [256], [0, 256])
	plt.subplot(121)
	plt.imshow(img, 'gray')
	plt.subplot(122)
	plt.plot(hist)
	plt.xlim(0, 255)
	plt.ylim(0, 1000)
	plt.show()

def normalize(img, mask=None):
	hist = cv2.calcHist([img], [0], mask, [30], [0, 256]).ravel()
	# total = hist.sum()
	# return hist / total
	minV = hist.min()
	maxV = hist.max()
	return (hist - minV) / (maxV - minV)

def getAllImagePath(folder):
	path = [os.path.join(folder, s) for s in ['cluster-nag', 'cluster-pos']]
	pathPos = os.listdir(path[1])
	pathPos = [os.path.join(path[1], s) for s in pathPos]

	pathNag = os.listdir(path[0])
	pathNag = [os.path.join(path[0], s) for s in pathNag]
	pathNag.extend(pathPos)
	return pathNag

def getPaths(folder):
	pathNag = os.listdir(folder)
	pathNag = [os.path.join(folder, s) for s in pathNag]
	return pathNag

if __name__ =='__main__':
	pass