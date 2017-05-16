#encoding:utf-8
from controler import *
from sys import argv
from random import random
if __name__ == "__main__":
	if len(argv) < 2:
		print "usage:python index.py urladdress example:python index.py http://weibo.com/p/10151501_61744481 [is_proxy]"
		exit()
	print "ok,the software is running! website is:"+argv[1]
	turl = argv[1]
	is_proxy = -1
	if len(argv)>2:
		is_proxy = argv[2]
	text = "我正在 #音乐人先锋榜# 为 @汪苏泷 "+turl+"打榜！好音乐需要用行动来支持，你也来为喜欢的音乐人加油吧！"
	num = -1
	resendAll(turl,text,num)
		


# 0.0.0.0:8080/?action=login login
#0.0.0.0:8080/?action=resend&text=hello$hahahh&url=http%3A//weibo.com/tv/v/Ejw5BFNgE%3Ffrom%3Dvhot
