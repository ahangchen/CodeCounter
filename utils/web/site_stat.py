import datetime
import json
import random
import time
from urllib.error import HTTPError
from urllib.request import urlopen

from utils.concurent.thread_utils import run_in_background
from utils.db import sqlite

urls = ["http://222.201.145.237:8888/VideoSvr/Login",
        "http://222.201.145.237:8888/VideoSvr/Touch?sid=%s",
        "http://222.201.145.237:8888/VideoSvr/SessionClean?sid=%s",
        "http://222.201.145.237:8888/VideoSvr/Playback?start=%d-%d-%d-%d-%d-%d&end=%d-%d-%d-%d-%d-%d&channel=%d&ip=%d.%d.%d.%d&port=%d&sid=%s",
        "http://222.201.145.237:8888/VideoSvr/RealPlay?ip=%d.%d.%d.%d&port=%d&channel=%d&nip=%d.%d.%d.%d&nport=%d&sid=%s",
        "http://222.201.145.237:8888/VideoSvr/LongTime?start=%d-%d-%d-%d-%d-%d&channel=%d&ip=%d.%d.%d.%d&port=%d&sid=%s",
        ]

random_size = 20


def url_stat(url, test_type):
    start = time.time()  # 单位秒
    resp_code = 0
    has_err = False
    resp_msg = ""
    try:
        resp = urlopen(url)
    except HTTPError as e:
        has_err = True
        resp_code = str(e.code)
        resp_msg = e.msg

    end = time.time()
    if not has_err:
        resp_msg = resp.read().decode()
        resp_code = str(resp.code)
    resp_time = str(end - start)

    sqlite.execute('url_stat.db', "insert into single (url, code, time, msg, type) values ('" +
                   url + "', '" + resp_code + "', '" + resp_time + "', '" + resp_msg + "', '" + test_type + "')")
    return resp_msg


def prepare():
    sqlite.new_table('url_stat.db', "single",
                     "id INTEGER PRIMARY KEY AUTOINCREMENT, url varchar(200), code varchar(4), time real, msg varchar(200), type integer")


def query_stat_all():
    return sqlite.query("url_stat.db", "select * from single")


def print_data_set(data_set):
    for i in range(len(data_set)):
        print(data_set[i])


def session_stat():
    data = json.loads(url_stat(urls[0], "1"))
    sid = data['sid']
    url_stat(urls[1] % sid, "1")
    url_stat(urls[2] % sid, "1")


def play_back_stat():
    data = json.loads(url_stat(urls[0], "1"))
    sid = data['sid']
    url_stat(urls[3] % (2016, 5, 1, 12, 0, 0, 2016, 5, 1, 12, 0, 15, 3, 125, 216, 231, 164, 37777, sid), "1")
    url_stat(urls[2] % sid, "1")


def back_cache_stat():
    data = json.loads(url_stat(urls[0], "2"))
    sid = data['sid']
    url_stat(urls[3] % (2016, 5, 1, 12, 0, 0, 2016, 5, 1, 12, 0, 15, 3, 125, 216, 231, 164, 37777, sid), "1")
    url_stat(urls[3] % (2016, 5, 1, 12, 0, 0, 2016, 5, 1, 12, 0, 15, 3, 125, 216, 231, 164, 37777, sid), "1")
    url_stat(urls[2] % sid, "1")


def real_play_stat():
    data = json.loads(url_stat(urls[0], "1"))
    sid = data['sid']
    url_stat(urls[4] % (125, 216, 231, 164, 35556, 1, 125, 216, 231, 164, 37777, sid), "1")
    url_stat(urls[2] % sid, "1")


def real_cache_stat():
    data = json.loads(url_stat(urls[0], "2"))
    sid = data['sid']
    url_stat(urls[4] % (125, 216, 231, 164, 35556, 1, 125, 216, 231, 164, 37777, sid), "1")
    url_stat(urls[4] % (125, 216, 231, 164, 35556, 1, 125, 216, 231, 164, 37777, sid), "1")
    url_stat(urls[2] % sid, "1")


def long_play_stat():
    data = json.loads(url_stat(urls[0], "1"))
    sid = data['sid']
    url_stat(urls[5] % (2016, 5, 1, 12, 0, 0, 3, 125, 216, 231, 164, 37777, sid), "1")
    url_stat(urls[2] % sid, "1")


def long_cache_stat():
    data = json.loads(url_stat(urls[0], "2"))
    sid = data['sid']
    url_stat(urls[5] % (2016, 5, 1, 12, 0, 0, 3, 125, 216, 231, 164, 37777, sid), "1")
    url_stat(urls[5] % (2016, 5, 1, 12, 0, 0, 3, 125, 216, 231, 164, 37777, sid), "1")
    url_stat(urls[2] % sid, "1")


def random_play_back(starts, ends, sid):
    for i in range(random_size):
        # starts.append(datetime.datetime.now() - datetime.timedelta(seconds=random.randint(0, 345600)))
        starts.append(datetime.datetime(2016, 5, 1) + datetime.timedelta(seconds=random.randint(0, 86400)))
        ends.append(starts[i] + datetime.timedelta(seconds=15))
    for i in range(random_size):
        run_in_background(url_stat, urls[3] % (starts[i].year, starts[i].month, starts[i].day,
                                               starts[i].hour, starts[i].minute, starts[i].second,
                                               ends[i].year, ends[i].month, ends[i].day,
                                               ends[i].hour, ends[i].minute, ends[i].second, random.randint(2, 4),
                                               125, 216, 231, 164, 37777, sid), "3")
        time.sleep(0.05)


def sample_stat():
    # 登录
    data = json.loads(url_stat(urls[0], "3"))
    sid = data['sid']

    # 直播
    url_stat(urls[4] % (125, 216, 231, 164, 35556, 1, 125, 216, 231, 164, 37777, sid), "3")
    # 点播抓取多个随机视频
    starts = []
    ends = []
    random_play_back(starts, ends, sid)
    time.sleep(15)

    # 随机挑一个来回播
    url_stat(urls[5] % (
        starts[random.randint(0, random_size - 1)].year, starts[random.randint(0, random_size - 1)].month,
        starts[random.randint(0, random_size - 1)].day,
        starts[random.randint(0, random_size - 1)].hour, starts[random.randint(0, random_size - 1)].minute,
        starts[random.randint(0, random_size - 1)].second,
        random.randint(2, 4), 125, 216, 231, 164, 37777, sid), "3")
    # 点播抓取多个随机视频
    random_play_back(starts, ends, sid)
    time.sleep(15)
    url_stat(urls[2] % sid, "1")


if __name__ == '__main__':
    prepare()
    # 顺序请求测试平均时间
    # i = 10
    # while i > 0:
    #     i -= 1
    #     session_stat()

    # 点播
    # play_back_stat()

    # 直播
    # real_play_stat()

    # 回播
    # long_play_stat()

    # 点播缓存测试
    # back_cache_stat()

    # 直播缓存测试
    # real_cache_stat()

    # 回播缓存测试
    # long_cache_stat()

    # 模拟正常流程测试
    # sample_stat()

    # 模拟多客户端测试
    # for i in range(1):
    #     run_in_background(sample_stat)
    # input('请按回车退出')
    # print_data_set(query_stat_all())

    # 模拟单客户端多次测试
    for i in range(30):
        sample_stat()
        print('range : ' + str(i))
        print_data_set(query_stat_all())
