import os
import model.common_define

__author__ = 'cwh'


def travel_dir(file_dir, on_dir, on_file):
    children = os.listdir(file_dir)  # 列出目录下的所有文件和目录
    for child in children:
        file_path = os.path.join(file_dir, child)
        if os.path.isdir(file_path):  # 如果file_path是目录，则再列出该目录下的所有文件
            on_dir(file_path)
            travel_dir(file_path, on_dir, on_file)
        elif os.path:  # 如果file_path是文件，直接列出文件名
            on_file(file_path)


def travel_dir_ret(file_dir, on_dir, on_file, ret):
    children = os.listdir(file_dir)  # 列出目录下的所有文件和目录
    for child in children:
        file_path = os.path.join(file_dir, child)
        if os.path.isdir(file_path):  # 如果file_path是目录，则再列出该目录下的所有文件
            on_dir(file_path, ret)
            travel_dir_ret(file_path, on_dir, on_file, ret)
        elif os.path:  # 如果file_path是文件，直接列出文件名
            on_file(file_path, ret)

    return ret


def line_count(file_path):
    print(file_path)
    file = open(file_path)
    count = 0
    while 1:
        try:
            lines = file.readlines(10000)  # 相当于一个缓冲区
        except UnicodeDecodeError:
            file.close()
            # 有的是用GBK的，也是够呛，年轻不懂事
            file = open(file_path, 'r', -1, 'gbk')
            try:
                lines = file.readlines(10000)
            except UnicodeDecodeError:
                print("such a fucking file: %s" % file_path)
                continue
        if not lines:
            break
        count += len(lines)
    file.close()
    print(count)
    # 把大于700行的文件记录下来
    if count > 700:
        special_write(file_path)
        special_write(str(count) + '\n')
    return count


def special_write(log):
    file = open("special", "a+")
    file.write(log + '\n')
    file.close()


def is_code_file(file_name):
    for ext in model.common_define.CODE_FILE_EXT_LIST:
        if file_name.endswith(ext):
            return True
        if file_name.endswith('workspace.xml') or file_name.endswith('R.java') or file_name.endswith('R.txt') \
                or file_name.endswith('values.xml') or file_name.endswith('workbench.xml') \
                or file_name.endswith('merger.xml') or 'intermediates' in file_name or 'generated' in file_name \
                or '.idea' in file_name or '.metadata' in file_name:
            return False
    return False


def code_counter(file_dir):
    # 传mutable对象才能留住更改
    count = [0]

    def on_dir(path, ret):
        pass

    def on_file(file_path, line_cnt):
        if is_code_file(file_path):
            line_cnt[0] += line_count(file_path)
            print(line_cnt)

    travel_dir_ret(file_dir, on_dir, on_file, count)

    return count[0]


def get_blank(line):
    char_count = 0
    for c in line:
        if c != ' ':
            break
        else:
            char_count += 1

    return char_count


def read2mem(path):
    file = open(path)
    content = ''
    while 1:
        try:
            lines = file.readlines(100)  # 相当于一个缓冲区
        except UnicodeDecodeError:
            file.close()
            continue
        if not lines:
            break
        for line in lines:
            content += line
    return content


def append2file(path, content):
    file = open(path, "a+")
    file.write(content)
    file.close()


def concepts():
    raw = read2mem('watermelon.md')
    lines = raw.split('\n')
    cs = list()
    for line in lines:
        words = line.split()
        if len(words) < 2:
            continue
        cs.append({'page': int(words[0]), 'word': words[1]})
    results = sorted(cs, key=lambda x: x['page'])
    for result in results:
        append2file('concept.md', '- Page' + str(result['page']) + ': ' + result['word'] + '\n')


if __name__ == '__main__':
    concepts()
    # print(utils.file.file_utils.code_counter('/media/Software/coding/C++/穿越迷宫/穿越迷宫'))
    # count = code_counter('/media/Software/coding')
    # special_write(str(count))
    # print(count)
    # build_by_summary('/home/cwh/gitrep/chromium/SUMMARY.md')
