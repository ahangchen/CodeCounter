# coding=utf-8
import http.client
import logging
from urllib.error import HTTPError
from urllib.request import urlopen

from utils.file import file_utils

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

def query_info():
    resp_code = 0
    has_err = False
    resp_msg = ""
    # 21033429
    # 20132000
    for i in range(1055, 1500):
        url = '' % i
        try:
            resp = urlopen(url)
        except HTTPError as e:
            has_err = True
            resp_code = str(e.code)
            resp_msg = e.msg

        if not has_err:
            resp_msg = resp.read().decode()
            resp_code = str(resp.code)
        if '没有入住安排信息' in resp_msg:
            print('no msg for num: %d' % i)
        else:
            file_utils.append2file('data.txt', resp_msg)


def filter_html(path):
    content = file_utils.read2mem(path)
    lines = content.split('\n')
    for line in lines:
        if '姓名：' in line or '性别：' in line or '身份证号' in line \
                or '学号：' in line or '所在学院：' in line or '所在专业：' in line  \
                or '学制：' in line or '毕业时间：' in line or '校区：' in line or '宿舍楼：' in line or '房间号：' in line:
            file_utils.append2file('simple.txt', line.replace('&nbsp;', '').replace('<br/>', '').strip() + '\n')


# filter_html('data.txt')


def line2table(path):
    content = file_utils.read2mem(path)
    lines = content.split('\n')
    cur_line_cnt = 0
    for line in lines:
        file_utils.append2file('table.txt', line.split('：')[-1])
        cur_line_cnt += 1
        if cur_line_cnt % 12 == 0:
            file_utils.append2file('table.txt', '\n')
        else:
            file_utils.append2file('table.txt', '\t')


line2table('simple.txt')
