#_*_coding:utf-8_*_
import re
from bs4 import BeautifulSoup as BS
import requests
import urllib


class extractKeywords(object):
	def __init__(self):
		"""
			提取百度图片的相关关键词
		"""
		pass

	def _buildBaiduImageRequest(self, words):
		# 构建初始的时候的请求页面，然后才能获取该搜索的关键词相关的其他的关键词
		URL = r"http://image.baidu.com/search/index?tn=baiduimage&ipn=r&ct=201326592&cl=2&lm=-1&st=-1&sf=1&fmq=&pv=&ic=0&nc=1&z=&se=1&showtab=0&fb=0&width=&height=&face=0&istype=2&ie=utf-8&fm=index&pos=history&word={word}"
		return URL.format(word=urllib.quote(words))

	def extract(self, words):
		URL = self._buildBaiduImageRequest(words)
		relateWords = None
		try:
			response = requests.get(URL, timeout=5)
			response.encoding = 'utf-8'
			soup = BS(response.text, 'html.parser')
			# 这是每一个页面的相关链接
			relateWords = soup.find_all("a", class_='pull-rs')
			relateWords = [s.text.encode('utf-8') for s in relateWords]
		except Exception as e:
			print('>>>>>>>>>>>Error Message:')
			print('Fail to extract the relative key words.')
			print(e)

		return relateWords


if __name__ == '__main__':
	import file
	extract = extractKeywords()

	# initKeyWords = [r'表情包', r'斗图', r'张学友表情包', r'金馆长', r'熊猫表情包', r'斗图表情包', r'熊猫斗图', r'当然是原谅她', r'小仙女表情包', r'表情包简笔画', r'程序员斗图']
	initKeyWords = [r'污表情包', r'撩妹表情包']

	# 获取初始关键词的所有相关关键词
	firstLevelWords = []
	for i in xrange(len(initKeyWords)):
		print("First level process %d" % (i))
		firstLevelWords.extend(extract.extract(initKeyWords[i]))

	# 获取第二层相关的关键词
	# secondLevelWords = []
	# for i in xrange(len(firstLevelWords)):
	# 	print("Second level process %d" % (i))
	# 	secondLevelWords.extend(extract.extract(firstLevelWords[i]))

	# 将所有的关键词保存到文件中
	initKeyWords.extend(firstLevelWords)
	# initKeyWords.extend(secondLevelWords)

	for i in xrange(len(initKeyWords)):
		file.console.log('keywords_brief_extend.txt', initKeyWords[i])