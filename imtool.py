#_*_coding:utf-8_*_
"""
author:NapoleonQin
email:qxfnapoleon@163.com
weChat:whatever
description : 图像平移、旋转、改变尺寸的小函数
"""
import cv2
import numpy

#
# 平移图像
#
def translate( img, tx, ty ):
    matrix = numpy.array([
        [1, 0, tx],
        [0, 1, ty]
    ], dtype=numpy.float32)
    targetImage = cv2.warpAffine(img, matrix, (img.shape[1], img.shape[0]))

    return targetImage

#
# 旋转图像
#
def rotate( img, centerPoint, angle, scale=1.0 ):
    matrix = cv2.getRotationMatrix2D(centerPoint, angle, scale)
    w = img.shape[1]
    h = img.shape[0]
    rotationImage = cv2.warpAffine(img, matrix, (w, h))

    return rotationImage

#
# 改变图像的尺寸
#
def resize( img, width=None, height=None, interpolation=cv2.INTER_AREA):
    ratio = None
    size = None

    if width is None and height is None:
        size = (img.shape[1], img.shape[0])
    #当值传递width的时候表示我们想要获得的图片有固定的宽度
    elif width is not None:
        ratio = width / float(img.shape[1])
        height = int(img.shape[0] * ratio)
        size = (width, height)
    elif height is not None:
        ratio = height / float(img.shape[0])
        width = int(img.shape[1] * ratio)
        size = (width, height)

    resizeImage = cv2.resize(img, size, interpolation=interpolation)

    return resizeImage