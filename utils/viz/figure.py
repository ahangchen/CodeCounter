import numpy as np
import matplotlib.pyplot as plt


def draw_rect():
    n_groups = 6
    test1 = (20, 35, 30, 35, 27, 32)
    test2 = (25, 32, 34, 20, 25, 11)
    test3 = (28, 32, 31, 26, 22, 17)

    plt.subplots()
    index = np.arange(n_groups)
    bar_width = 0.2
    opacity = 0.4
    plt.bar(index, test1, bar_width, alpha=opacity, color='b', label='Test1')
    plt.bar(index + bar_width, test2, bar_width, alpha=opacity, color='r', label='Test2')
    plt.bar(index + 2 * bar_width, test3, bar_width, alpha=opacity, color='g', label='Test3')
    plt.xlabel('Request')
    plt.ylabel('Time')
    plt.title('Response Time in Three Situations')
    plt.xticks(index + 1.5 * bar_width, ('Login', 'Touch', 'SessionClean', 'Playback', 'RealPlay', 'LongTime'))
    plt.ylim(0, 40)
    plt.legend()
    plt.tight_layout()
    plt.show()


if __name__ == '__main__':
    draw_rect()
