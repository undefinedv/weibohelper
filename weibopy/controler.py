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
import random
def resendAll(url,texts=['hello!'],num=-1):
	cookies = function.getCookies()
	text = random.choice(texts)
	proxy = {"http":"127.0.0.1:8087"}
	#proxy = 0# set 0 to stop the proxy
	tasks = []
	if num == -1:
		for cookie in cookies:
			tasks.append(weibo.weiboResend(cookie,url,text,proxy))
	else:
		flag = 0
		for cookie in cookies:
			if flag >= num:
				break
			else:
				tasks.append(weibo.weiboResend(cookie,url,text,proxy))
				flag += 1
	for task in tasks:
		task.start()
	for task in tasks:
		task.join()
	return "resend OK"

def loginAll():
	print u'新浪微博模拟登陆:'
	tasks = {}
	accounts = function.getAccounts()
	proxy = {"http":"127.0.0.1:8087"}
	#proxy = 0
	fp = open("config/cookies.database","a")
	for account in accounts:
		t = account.split(",")
		username = t[0]
		password = t[1]
		tasks[username] = weibo.weiboLogin(fp,username,password,proxy)
	for task in tasks:
		tasks[task].start()
	for task in tasks:
		tasks[task].join()
	fp.close()
	return "OK"

# if __name__=='__main__':
# 	reload(sys)
# 	sys.setdefaultencoding("utf-8")
# 	url = "http://weibo.com/1642591402/EjwlZ13Pn?type=comment#_rnd1480314907965"
# 	texts = ['hahhh!']
# 	resendAll(url,texts)