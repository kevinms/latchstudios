import threading
import Queue
import sys

class console(threading.Thread):

	def __init__(self,n):
		threading.Thread.__init__(self)
		self.n = n

	def run(self):
		while 1:
			s = sys.stdin.readline()
			self.parse(s.strip())

	def parse(self,s):
		if self.check(s,'say'):
			self.n.chat(s[4:])

	def check(self,s,token):
		return s[:len(token)] == token
