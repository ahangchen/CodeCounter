import http.client

__author__ = 'cwh'


def get(url):
    http_client = None
    try:
        http_client = http.client.HTTPConnection(url, 80, timeout=30)
        http_client.request('GET', '/')

        # response是HTTPResponse对象
        response = http_client.getresponse()
        print(response.status)
        print(response.reason)
        print(response.read())
    except IOError:
        print('error')
    finally:
        if http_client:
            http_client.close()


get('www.baidu.com')
