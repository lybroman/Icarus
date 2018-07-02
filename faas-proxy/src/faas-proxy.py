from celery import Celery
import requests
import traceback
icarus = Celery('icarus.app', backend='db+postgresql://postgres:postgres@postgres:5432/postgres', broker='pyamqp://guest@rabbitmq//')


@icarus.task(name='icarus.app.func_handler')
def func_handler(url, content, **kwargs):
	response = requests.post('http://gateway:8080/function/icarus_{}'.format(url), data=content)
	if 'callback_url' in kwargs:
		try:
			print response.text
			rr = requests.post(kwargs['callback_url'], data=response.text)
			return rr.text
		except:
			return traceback.format_exc()
	return response.text

