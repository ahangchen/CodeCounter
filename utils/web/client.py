import http.client
import logging
from urllib.request import urlopen

import time

__author__ = 'cwh'


def get(url):
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


def url_response_time(url):
    start = time.time()  # 单位秒
    resp = urlopen(url)
    if resp.code == 200:
        print(resp.read())
    else:
        print(resp.code)
    end = time.time()
    return end - start

time_cnt = url_response_time("http://222.201.145.237:8888/VideoSvr/Login")
print(time_cnt)
