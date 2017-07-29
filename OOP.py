#_*_coding:utf-8_*_
# author : xiaofu.qin
# description: Learning the OOP for Python

#New style of defining the Python class
class Programmer(object):
	
	# define a static property
	description = "My name is xiaofu.qin, I come from China"
	def __init__(self, name, age):
		"""
		This is my first Python new style class.
		"""
		self.name = name
		# protect property
		self._age = age

	@property
	def getAge(self):
		return self._age

	@classmethod
	def Hi(cl, you):
		return "%s, this is parameter %s" % (cl.description, you)

	@staticmethod
	def hello():
		return Programmer.description

class FrontEndProgrammer(Programmer):
	def __init__(self, name, age, language):
		super(FrontEndProgrammer, self).__init__(name, age)
		self.language = language


if __name__ == '__main__':
	pro = FrontEndProgrammer('NapoleonAndXiaofuQin', 55, 'Javascript')
	help(Programmer)
	print(pro.getAge)