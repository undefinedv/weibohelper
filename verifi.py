import requests
import urllib2
import urllib
import md5
import re
def verifi():
	url = "http://login.sina.com.cn/cgi/pin.php"
	filename = "png/test.png"
	urllib.urlretrieve(url,filename)
	headers = {
	"Content-type":"multipart/form-data; boundary=-------------RK",
	"Accept-Encoding":"gzip, deflate", 
	"Accept-Language":"zh-cn", 
	"Accept":"*/*", 
	"User-Agent":"Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:49.0) Gecko/20100101 Firefox/49.0"
	}
	fp = open(filename,"r")
	filedata = fp.read()
	boundary = "---------------RK"
	data = []
	data.append(boundary)
	data.append('Content-Disposition: form-data; name="username"\r\n')
	data.append('undefined')
	data.append(boundary)
	data.append('Content-Disposition: form-data; name="password"\r\n')
	data.append('hduisa111')
	data.append(boundary)
	data.append('Content-Disposition: form-data; name="typeid"\r\n')
	data.append('5000')
	data.append(boundary)
	data.append('Content-Disposition: form-data; name="timeout"\r\n')
	data.append('90')
	data.append(boundary)
	data.append('Content-Disposition: form-data; name="softid"\r\n')
	data.append('71614')
	data.append(boundary)
	data.append('Content-Disposition: form-data; name="softkey"\r\n')
	data.append('30be95da6c574797bc11ddbdf6a79793')
	data.append(boundary)
	data.append('Content-Disposition: form-data; name="image"; filename="1.png"')
	data.append('Content-Type: application/octet-stream\r\n')
	data.append(filedata)
	data.append(boundary+"--")
	# data.append('Content-Disposition: form-data; name="Submit"\r\n')
	# data.append('submit')
	# data.append(boundary)
	httpBody = '\r\n'.join(data)
	postDataUrl = 'http://api.ruokuai.com/create.json'
	response = urllib2.Request(postDataUrl,data=httpBody, headers=headers)
	response = urllib2.urlopen(response)
	response = response.read()
	p = re.compile('Result\":\"(.*)\",')
	code = p.search(response).group(1)
	return code