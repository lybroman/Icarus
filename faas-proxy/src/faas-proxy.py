from celery import Celery
import requests
icarus = Celery('icarus.app', backend='db+postgresql://postgres:postgres@postgres:5432/postgres', broker='pyamqp://guest@rabbitmq//')


@icarus.task(name='icarus.app.func_handler')
def func_handler(url, *args):
    response = requests.post('http://gateway:8080/function/icarus_{}'.format(url), data=args[0])
    return response.text

