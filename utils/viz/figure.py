import matplotlib.pyplot as plt
import numpy as np

from utils.db import sqlite


def read_db():
    pass


def draw_rect(ys_in_labels, y_low_bound, y_up_bound, xs, x_type_cnt, label_colors, label_names, x_label, y_label,
              title):
    label_cnt = len(ys_in_labels)

    plt.subplots()
    index = np.arange(x_type_cnt)
    bar_width = 1 / (label_cnt + 1)
    opacity = 0.4
    for j in range(label_cnt):
        plt.bar(index + j * bar_width, ys_in_labels[j], bar_width, alpha=opacity, color=label_colors[j],
                label=label_names[j])
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.title(title)
    plt.xticks(index + label_cnt / 2 * bar_width, xs)
    plt.ylim(y_low_bound, y_up_bound)
    plt.legend()
    plt.tight_layout()
    plt.show()


def sample_draw_rect():
    url_type = 6
    resp_time_of_url_in_types = [(20, 35, 30, 35, 27, 32),
                                 (25, 32, 34, 20, 25, 11),
                                 (28, 32, 31, 26, 22, 17)]
    min_resp_time = 0
    max_resp_time = 40
    url_types = ('Login', 'Touch', 'SessionClean', 'Playback', 'RealPlay', 'LongTime')
    label_colors = ['r', 'g', 'b']
    label_names = ['single', 'cache', 'sample']
    x_label_name = '请求分类'
    y_label_name = '响应时间'
    figure_name = '不同请求在不同测试环境下的平均响应时间'
    draw_rect(resp_time_of_url_in_types, min_resp_time, max_resp_time, url_types, url_type, label_colors, label_names,
              x_label_name, y_label_name, figure_name)


def site_avg_rect(p_login_s, p_touch_s, p_clean_s, p_play_back_s, p_real_play_s, p_long_time_s):
    url_type = 6
    resp_time_of_url_in_types = \
        [(p_login_s[0], p_touch_s[0], p_clean_s[0], p_play_back_s[0], p_real_play_s[0], p_long_time_s[0]),
         (p_login_s[1], p_touch_s[1], p_clean_s[1], p_play_back_s[1], p_real_play_s[1], p_long_time_s[1]),
         (p_login_s[2], p_touch_s[2], p_clean_s[2], p_play_back_s[2], p_real_play_s[2], p_long_time_s[2])]
    min_resp_time = 0
    max_resp_time = 7
    url_types = ('Login', 'Touch', 'SessionClean', 'Playback', 'RealPlay', 'LongTime')
    label_colors = ['r', 'g', 'b']
    label_names = ['single', 'cache', 'sample']
    x_label_name = 'Request Type'
    y_label_name = 'Response Time'
    figure_name = 'Average Response Time of Requests in Three Test Environment'
    draw_rect(resp_time_of_url_in_types, min_resp_time, max_resp_time, url_types, url_type, label_colors, label_names,
              x_label_name, y_label_name, figure_name)


if __name__ == '__main__':
    login_s = sqlite.query('../web/url_stat.db', "select * from single where url like '%Login'")
    touch_s = sqlite.query('../web/url_stat.db', "select * from single where url like '%Touch%'")
    clean_s = sqlite.query('../web/url_stat.db', "select * from single where url like '%SessionClean%'")
    play_back_s = sqlite.query('../web/url_stat.db', "select * from single where url like '%Playback%'")
    real_play_s = sqlite.query('../web/url_stat.db', "select * from single where url like '%RealPlay%'")
    long_time_s = sqlite.query('../web/url_stat.db', "select * from single where url like '%LongTime%'")

    result_s = [login_s, touch_s, clean_s, play_back_s, real_play_s, long_time_s]

    login_avg_s = [0.0, 0.0, 0.0]
    touch_avg_s = [0.0, 0.0, 0.0]
    clean_avg_s = [0.0, 0.0, 0.0]
    play_back_avg_s = [0.0, 0.0, 0.0]
    real_play_avg_s = [0.0, 0.0, 0.0]
    long_time_avg_s = [0.0, 0.0, 0.0]

    avg_s = [login_avg_s, touch_avg_s, clean_avg_s, play_back_avg_s, real_play_avg_s, long_time_avg_s]

    for j in range(len(result_s)):
        data_size = len(result_s[j])
        for i in range(data_size):
            avg_s[j][result_s[j][i][5] - 1] += result_s[j][i][3]
        for i in range(len(avg_s[j])):
            if data_size != 0:
                avg_s[j][i] /= data_size
    for i in range(len(avg_s)):
        for j in range(len(avg_s[i])):
            print(avg_s[i][j])
        print()
    site_avg_rect(login_avg_s, touch_avg_s, clean_avg_s, play_back_avg_s, real_play_avg_s, long_time_avg_s)
