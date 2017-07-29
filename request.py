#_*_coding:utf-8_*_
# author : xiaofu.qin
# description : Learning requests library
import requests
from io import BytesIO
from PIL import Image
import cv2
import numpy

URL = 'http://id.fanruan.com/login/login.php'
IMAGE_URL = 'http://id.fanruan.com/template/img/logo_116x40@2x.png?__sprite'
BAIDU_IMAGE = 'http://image.baidu.com/search/down?tn=download&ipn=dwnl&word=download&ie=utf8&fr=result&url=http%3A%2F%2Fimg3.duitang.com%2Fuploads%2Fitem%2F201607%2F26%2F20160726073053_QAHTu.thumb.700_0.jpeg&thumburl=http%3A%2F%2Fimg0.imgtn.bdimg.com%2Fit%2Fu%3D2167144987%2C2085131087%26fm%3D26%26gp%3D0.jpg'
GITHUB_URL = 'https://api.github.com/events'
LOGIN_URL = 'http://id.fanruan.com/login/login_alpha_one.php'

def get_simple_requests(url):
	params = {'key':'value'}
	response = requests.get(url, params=params)
	response.encoding = 'utf-8'
	print response.encoding
	print( ">>>> Response body:" )
	print response.text

def downloadImage(url):
	response = requests.get(url)
	with Image.open(BytesIO(response.content)) as image:
		image = numpy.array(image)
		cv2.imshow('id.fanruan.com', image)
		cv2.waitKey(0) & 0XFF
		cv2.destroyAllWindows()

def json_response(url):
	response = requests.get(url)
	response.encoding = 'utf-8'
	print(response.json())

# 从服务器上获取原始的数据流，并将这些数据流保存在本地文件中，使用数据流的时候最好加上stream=True这个参数，下面的代码可以用来下载任何文件
def download_html_file(url, localFileName='login.html'):
	response = requests.get(url, stream=True)
	with open(localFileName, 'wb') as f:
		for chunk in response.iter_content(chunk_size=128):
			f.write(chunk)

def post_request():
	headers = {'user-agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36'}
	params = {'name':'xiaofu.qin', 'hero' : 'Napoleon'}
	response = requests.post("http://httpbin.org/post", data=params, headers=headers)
	response.encoding = 'utf-8'
	print(response.text)

def getResponseCookie(url):
	response = requests.get(url)
	response.encoding = 'utf-8'
	print('>>> Response headers')
	print(response.headers)
	print('>>> Response cookies')
	print(response.cookies)



if __name__ == '__main__':
	# get_simple_requests(URL)
	# downloadImage(IMAGE_URL)
	# json_response(GITHUB_URL)
	# download_html_file(IMAGE_URL, 'logo.png')
	# post_request()
	# getResponseCookie(URL)
	download_html_file(BAIDU_IMAGE, 'baidu.jpg')