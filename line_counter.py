import utils.concurent.thread_utils
import time

__author__ = 'cwh'


def on_dir(dir_path):
    print(dir_path)


def on_file(file_path):
    print(file_path)


class Test(object):
    pass


if __name__ == '__main__':

    def sleep_print():
        time.sleep(1)
        print(1)
        time.sleep(1)
        print(2)

    utils.concurent.thread_utils.new_thread(sleep_print, 'sleep')
    print('this end')
