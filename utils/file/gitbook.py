import os

from utils.file.file_utils import get_blank, read2mem, append2file, travel_dir


def gen_name(line):
    return line.strip().replace('- ', '').replace(' ', '_').replace('/', '_') \
        .replace(':', '').replace(',', '').replace('(', '_').replace(')', '_')


def gen_dir_name(names):
    dir_name = ''
    for name in names:
        dir_name += '/' + name
    return dir_name


def build_by_summary(summary_path):
    file = open(summary_path)
    dst_file = open(summary_path.replace('SUMMARY.md', 'summary.md'), 'a+')
    while 1:
        try:
            lines = file.readlines(10000)  # 相当于一个缓冲区
        except UnicodeDecodeError:
            file.close()
            # 有的是用GBK的，也是够呛，年轻不懂事
            file = open(summary_path, 'r', -1, 'gbk')
            try:
                lines = file.readlines(10000)
            except UnicodeDecodeError:
                print("such a fucking file: %s" % summary_path)
                continue
        if not lines:
            break
        root_dir = summary_path.replace("/SUMMARY.md", "")
        tmp_lines = []
        for line in lines:
            if '-' in line:
                tmp_lines.append(line)

        lines = tmp_lines
        dir_depth = -1

        sub_dir = ''

        for index in range(len(lines)):
            # 要求子项缩进为两个空格
            cur_depth = get_blank(lines[index]) / 2
            if cur_depth <= dir_depth:
                remove_count = dir_depth - cur_depth + 1
                names = sub_dir.split('/')
                tmp_names = []
                for index2 in range(len(names)):
                    if index2 < len(names) - remove_count:
                        tmp_names.append(names[index2])

                names = tmp_names
                sub_dir = gen_dir_name(names[1:])

            sub_dir += '/' + gen_name(lines[index])
            dir_depth = cur_depth
            if index < len(lines) - 1 and cur_depth < get_blank(lines[index + 1]) / 2:
                os.mkdir(root_dir + sub_dir)
                os.mknod(root_dir + sub_dir + '/README.md')
                dst_file.write(
                    lines[index].replace('- ', '- [').replace('\n', '') + '](%s/README.md)\n' % sub_dir[1:])
            else:
                os.mknod(root_dir + sub_dir + '.md')
                dst_file.write(lines[index].replace('- ', '- [').replace('\n', '') + '](%s.md)\n' % sub_dir[1:])
    file.close()
    dst_file.close()


def md_link(path):
    if path.endswith('README.md'):
        return "- [%s](%s)" % (path2name(path.replace('/README.md', '')), path)
    else:
        return "- [%s](%s)" % (path2name(path.replace('.md', '')), path)


def path2name(path):
    pieces = path.split('/')
    return pieces[len(pieces) - 1]


def summary_path(dir_path):
    return dir_path + '/SUMMARY.md'


def dir_readme(dir_path):
    return dir_path + '/README.md'


def build_summary(root_path):
    if os.path.exists(summary_path(root_path)):
        os.remove(summary_path(root_path))
    summary = open(summary_path(root_path), 'a+')
    build_summary_helper(root_path, 0, summary)
    summary.close()
    content = read2mem(summary_path(root_path))
    content = content.replace(root_path + '/', '')
    os.remove(summary_path(root_path))
    append2file(summary_path(root_path), content)


def is_sum_file(file_path):
    return file_path.endswith('.md')


def build_summary_helper(root_path, blank_cnt, summary):
    children = os.listdir(root_path)  # 列出目录下的所有文件和目录
    for child in children:
        file_path = os.path.join(root_path, child)
        if os.path.isdir(file_path):  # 如果file_path是目录，则再列出该目录下的所有文件
            if child == '.git':
                continue
            for i in range(blank_cnt):
                summary.write(' ')
            summary.write(md_link(dir_readme(file_path)) + '\n')
            build_summary_helper(file_path, blank_cnt + 2, summary)
        elif os.path:  # 如果file_path是文件，直接列出文件名
            if is_sum_file(file_path):
                for i in range(blank_cnt):
                    summary.write(' ')
                summary.write(md_link(file_path) + '\n')


def index2readme(dir_path):
    def on_dir(file_path):
        pass

    def on_file(file_path):
        if file_path.endswith('index.md'):
            os.rename(file_path, file_path.replace('index.md', 'README.md'))
    travel_dir(dir_path, on_dir, on_file)

if __name__ == '__main__':
    index2readme('/home/cwh/docs/g3doc')
    build_summary('/home/cwh/docs/g3doc')