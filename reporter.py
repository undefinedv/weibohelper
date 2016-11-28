#encoding:utf-8
import requests
headers = {"Content-type":"application/x-www-form-urlencoded", "Referer":"", "X-Requested-With":"XMLHttpRequest", "User-Agent":"Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:49.0) Gecko/20100101 Firefox/49.0"}
headers['Cookie'] = "PHPSESSID=o1iac73pbugrrj1481bqnf9cf0"
url1 = "http://changelog.hctf.io/register.php"
url2 = "http://changelog.hctf.io/login.php"
url3 = "http://changelog.hctf.io/index.php"
data = {
	"username":"undefined0",
	"password":"123456",
	"gogogo":"苟!"
}
response1 = requests.post(url1,headers = headers,data = data)
print "step1:"
print response1.text
response2 = requests.post(url2,headers = headers,data = data)
print "step2:"
print response2.text
response3 = requests.get(url3,headers = headers)
print "step3:"
print response3.text