import web
import controler
urls=('/.*','index')
app=web.application(urls,globals())
class index():
	def GET(self):
		res = ''
		i = web.input(action = 'show',text='', url = '',num=-1)
		text = i.text.split("$")
		if i.action == 'login':
			res = controler.loginAll()
		elif i.action == 'resend':
			res = controler.resendAll(i.url,text,i.num)
		return "result :" + res
		#return render.index(i.name,i.age)
# class flush():
# 	def GET(self):
# 		return "This is flush action"
if __name__ == "__main__":
	app.run()


# 0.0.0.0:8080/?action=login login
#0.0.0.0:8080/?action=resend&text=hello$hahahh&url=http%3A//weibo.com/tv/v/Ejw5BFNgE%3Ffrom%3Dvhot