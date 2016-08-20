# coding=utf-8
import http.client
import logging
import urllib3

__author__ = 'cwh'


def get(url):
    """"
    :param url 比如，110.65.10.209/uploadfile，要有host和后半部分
    如果请求的确实只有host，就传host就好 110.65.10.209
    :return 返回response对象
    """
    strings = url.split('/')
    host = strings[0].split(':')[0]
    port = strings[0].split(':')[1]
    child = url.replace(strings[0] + '/', '')
    http_client = None
    try:
        http_client = http.client.HTTPConnection(host, port, timeout=30)
        http_client.request('GET', child)

        ret = http_client.getresponse()
        return ret
    except IOError as e:
        print(url)
        logging.exception(e)
    finally:
        if http_client:
            http_client.close()


def post(url):
    """"
    :param url 比如，110.65.10.209/uploadfile，要有host和后半部分
    如果请求的确实只有host，就传host就好 110.65.10.209
    :return 返回response对象
    """
    strings = url.split('/')
    host = strings[0]
    child = url.replace(host, '')
    http_client = None
    try:
        http_client = http.client.HTTPConnection(host, timeout=30)
        http_client.request('GET', child)

        ret = http_client.getresponse()
        return ret
    except IOError as e:
        print(url)
        logging.exception(e)
    finally:
        if http_client:
            http_client.close()


def query_file():
    # 201230601030
    for i in range(28265, 100000):
        response = get('110.65.10.209/uploadfile/201230601030%06d.pdf' % i)
        if response is not None and response.status != 404:
            print('success: 110.65.10.209/uploadfile/201230601030%06d.pdf' % i)


# query_file()
