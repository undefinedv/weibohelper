# -*- coding: utf-8 -*-  
########################  
#author:Undefined
#date:2016/11/18
#login weibo  
########################
import sys  
import urllib  
import urllib2  
import cookielib  
import base64  
import re  
import json  
import rsa  
import binascii
import threading
from Queue import Queue
import weibo
import function
def loginAll():
	print u'新浪微博模拟登陆:'
	tasks = {}
	accounts = function.getAccounts()
	fp = open("config/cookies.database","a")
	for account in accounts:
		t = account.split(",")
		username = t[0]
		password = t[1]
		tasks[username] = weibo.weiboLogin(fp,username,password)
	for task in tasks:
		tasks[task].start()
	for task in tasks:
		tasks[task].join()
	fp.close()
	return "OK"
if __name__=='__main__':
	reload(sys)
	sys.setdefaultencoding("utf-8")
	#username = raw_input(u'用户名:')
	#password = raw_input(u'密码:')
	loginAll()
	function.getCookies()