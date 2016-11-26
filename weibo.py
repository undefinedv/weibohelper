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
#import requests  
#from bs4 import BeautifulSoup  
  
#新浪微博的模拟登陆  
class weiboLogin:  
    def enableCookies(self):  
            #获取一个保存cookies的对象  
            cj = cookielib.CookieJar()  
            #将一个保存cookies对象和一个HTTP的cookie的处理器绑定  
            cookie_support = urllib2.HTTPCookieProcessor(cj)  
            #创建一个opener,设置一个handler用于处理http的url打开  
            opener = urllib2.build_opener(cookie_support, urllib2.HTTPHandler)  
            #安装opener，此后调用urlopen()时会使用安装过的opener对象  
            urllib2.install_opener(opener)  
  
    #预登陆获得 servertime, nonce, pubkey, rsakv  
    def getServerData(self):  
            url = 'http://login.sina.com.cn/sso/prelogin.php?entry=weibo&callback=sinaSSOController.preloginCallBack&su=ZW5nbGFuZHNldSU0MDE2My5jb20%3D&rsakt=mod&checkpin=1&client=ssologin.js(v1.4.18)&_=1442991685270'  
            data = urllib2.urlopen(url).read()  
            p=re.compile('\((.*)\)')
            try:
                    json_data = p.search(data).group(1)
                    data = json.loads(json_data)
                    servertime = str(data['servertime'])
                    nonce = data['nonce']
                    pubkey = data['pubkey']
                    rsakv = data['rsakv']
                    return servertime, nonce, pubkey, rsakv  
            except:
                    print 'Get severtime error!'
                    return None
                  
  
    #获取加密的密码  
    def getPassword(self, password, servertime, nonce, pubkey):  
            rsaPublickey = int(pubkey, 16)  
            key = rsa.PublicKey(rsaPublickey, 65537) #创建公钥  
            message = str(servertime) + '\t' + str(nonce) + '\n' + str(password) #拼接明文js加密文件中得到  
            passwd = rsa.encrypt(message, key) #加密  
            passwd = binascii.b2a_hex(passwd) #将加密信息转换为16进制。  
            return passwd  
  
    #获取加密的用户名  
    def getUsername(self, username):  
            username_ = urllib.quote(username)  
            username = base64.encodestring(username_)[:-1]  
            return username  
  
     #获取需要提交的表单数据     
    def getFormData(self,userName,password,servertime,nonce,pubkey,rsakv):  
        userName = self.getUsername(userName)  
        psw = self.getPassword(password,servertime,nonce,pubkey)  
          
        form_data = {  
            'entry':'weibo',  
            'gateway':'1',  
            'from':'',  
            'savestate':'7',  
            'useticket':'1',  
            'pagerefer':'http://weibo.com/p/1005052679342531/home?from=page_100505&mod=TAB&pids=plc_main',  
            'vsnf':'1',  
            'su':userName,  
            'service':'miniblog',  
            'servertime':servertime,  
            'nonce':nonce,  
            'pwencode':'rsa2',  
            'rsakv':rsakv,  
            'sp':psw,  
            'sr':'1366*768',  
            'encoding':'UTF-8',  
            'prelt':'115',  
            'url':'http://weibo.com/ajaxlogin.php?framelogin=1&callback=parent.sinaSSOController.feedBackUrlCallBack',  
            'returntype':'META'  
            }  
        formData = urllib.urlencode(form_data)  
        return formData  
  
    #登陆函数  
    def login(self,username,psw):  
            self.enableCookies()  
            url = 'http://login.sina.com.cn/sso/login.php?client=ssologin.js(v1.4.18)'  
            servertime,nonce,pubkey,rsakv = self.getServerData()  
            formData = self.getFormData(username,psw,servertime,nonce,pubkey,rsakv)  
            headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.3; WOW64; rv:41.0) Gecko/20100101 Firefox/41.0'}  
            req  = urllib2.Request(  
                    url = url,  
                    data = formData,  
                    headers = headers  
            )  
            result = urllib2.urlopen(req)  
            text = result.read()  
            print text  
            #还没完！！！这边有一个重定位网址，包含在脚本中，获取到之后才能真正地登陆  
            p=re.compile('location\.replace\(\'(.*)\'\)')
            try:  
                    login_url = p.search(text).group(1)
                    print login_url  
                    #由于之前的绑定，cookies信息会直接写入  
                    urllib2.urlopen(login_url)  
                    print "Login success!"  
            except:  
                    print 'Login error!'  
                    return 0  
  
            #访问主页，把主页写入到文件中  
            url = 'http://weibo.com/u/2679342531/home?topnav=1&wvr=6'  
            request = urllib2.Request(url)  
            response = urllib2.urlopen(request)  
            text = response.read()
            fp_raw = open("config/cookies.database","w+")  
            fp_raw.write(text)  
            fp_raw.close()  
            #print text  
            
reload(sys)
sys.setdefaultencoding( "utf-8" )
wblogin = weiboLogin()
print '新浪微博模拟登陆:'
username = raw_input(u'用户名:')
password = raw_input(u'密码:')
wblogin.login(username,password)
