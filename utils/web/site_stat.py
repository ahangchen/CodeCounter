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
    url_stat(urls[1] % sid, "2")
    url_stat(urls[3] % (2016, 5, 1, 12, 0, 0, 2016, 5, 1, 12, 0, 15, 3, 125, 216, 231, 164, 37777, sid), "2")
    url_stat(urls[2] % sid, "2")


def real_play_stat():
    data = json.loads(url_stat(urls[0], "1"))
    sid = data['sid']
    url_stat(urls[4] % (125, 216, 231, 164, 35556, 1, 125, 216, 231, 164, 37777, sid), "1")
    url_stat(urls[2] % sid, "1")


def real_cache_stat():
    data = json.loads(url_stat(urls[0], "2"))
    sid = data['sid']
    url_stat(urls[4] % (125, 216, 231, 164, 35556, 1, 125, 216, 231, 164, 37777, sid), "1")
    url_stat(urls[1] % sid, "2")
    url_stat(urls[4] % (125, 216, 231, 164, 35556, 1, 125, 216, 231, 164, 37777, sid), "2")
    url_stat(urls[2] % sid, "2")


def long_play_stat():
    data = json.loads(url_stat(urls[0], "1"))
    sid = data['sid']
    url_stat(urls[5] % (2016, 5, 1, 12, 0, 0, 3, 125, 216, 231, 164, 37777, sid), "1")
    url_stat(urls[2] % sid, "1")


def long_cache_stat():
    data = json.loads(url_stat(urls[0], "2"))
    sid = data['sid']
    url_stat(urls[5] % (2016, 5, 1, 12, 0, 0, 3, 125, 216, 231, 164, 37777, sid), "1")
    url_stat(urls[1] % sid, "2")
    url_stat(urls[5] % (2016, 5, 1, 12, 0, 0, 3, 125, 216, 231, 164, 37777, sid), "2")
    url_stat(urls[2] % sid, "2")


def random_play_back(starts, ends, sid, test_type):
    for k in range(random_size):
        # starts.append(datetime.datetime.now() - datetime.timedelta(seconds=random.randint(0, 345600)))
        starts.append(datetime.datetime(2016, 5, 5) + datetime.timedelta(seconds=random.randint(0, 43200)))
        ends.append(starts[k] + datetime.timedelta(seconds=15))
    for k in range(random_size):
        run_in_background(url_stat, urls[3] % (starts[k].year, starts[k].month, starts[k].day,
                                               starts[k].hour, starts[k].minute, starts[k].second,
                                               ends[k].year, ends[k].month, ends[k].day,
                                               ends[k].hour, ends[k].minute, ends[k].second, random.randint(2, 4),
                                               125, 216, 231, 164, 37777, sid), test_type)
        time.sleep(0.05)


def sample_stat(test_type):
    # 登录
    data = json.loads(url_stat(urls[0], test_type))
    sid = data['sid']

    # 直播
    url_stat(urls[4] % (125, 216, 231, 164, 35556, 1, 125, 216, 231, 164, 37777, sid), test_type)
    # 点播抓取多个随机视频
    starts = []
    ends = []
    random_play_back(starts, ends, sid, test_type)
    time.sleep(15)
    url_stat(urls[1] % sid, test_type)
    # 随机挑一个来回播
    url_stat(urls[5] % (
        starts[random.randint(0, random_size - 1)].year, starts[random.randint(0, random_size - 1)].month,
        starts[random.randint(0, random_size - 1)].day,
        starts[random.randint(0, random_size - 1)].hour, starts[random.randint(0, random_size - 1)].minute,
        starts[random.randint(0, random_size - 1)].second,
        random.randint(2, 4), 125, 216, 231, 164, 37777, sid), test_type)
    # 点播抓取多个随机视频
    random_play_back(starts, ends, sid, test_type)
    time.sleep(15)
    url_stat(urls[2] % sid, test_type)


if __name__ == '__main__':
    prepare()

    # for i in range(30):
    #     # 会话相关测试
    #     session_stat()
    #     # 点播
    #     play_back_stat()
    #
    #     # 直播
    #     real_play_stat()
    #
    #     # 回播
    #     long_play_stat()
    #
    #     # 点播缓存测试
    #     back_cache_stat()
    #
    #     # 直播缓存测试
    #     real_cache_stat()
    #
    #     # 回播缓存测试
    #     long_cache_stat()
    #
    #     print_data_set(query_stat_all())
    #
    # # 模拟正常流程测试
    # sample_stat("3")
    #
    # # 模拟单客户端多次测试
    # for i in range(30):
    #     sample_stat("3")
    #     print_data_set(query_stat_all())
    #     print('range : ' + str(i))
    #
    # 模拟多客户端测试
    for i in range(4):
        run_in_background(sample_stat, "4")
    sample_stat("4")
    input('请按回车退出')
    print_data_set(query_stat_all())

    # 测试删
    # sqlite.execute('url_stat.db', 'delete from single WHERE id > 2099')
    # 测试改
    # sqlite.execute('url_stat.db', 'update single set type = 3 WHERE type = 1')
