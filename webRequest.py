#_*_coding:utf-8_*_
# author : xiaofu.qin
# description : 使用requests库来请求百度云网络图片识图webDemo页面，看看能不能行得通
# 还可以使用达观数据的webDemo来请求分词，这个有点儿省钱了。

import base64
import requests
import cv2
import numpy

import file

# 请求达观数据的分词
response = requests.post('http://fileload.datagrand.com:8080/pos', data = {
	"text" : "床前明月光，疑是地上霜。好一个睹物思乡的诗人。"
})
response = response.json()
for r in response:
	print(r[0])
	
