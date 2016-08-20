import os
from html.parser import HTMLParser

from utils.file import file_utils


class LinkParser(HTMLParser):
    def error(self, message):
        pass

    is_a = False
    is_h3 = False
    links = []
    cur_tag_key = ''
    cur_tag_value = ''

    def __init__(self):
        HTMLParser.__init__(self)

    def handle_starttag(self, tag, attrs):
        # print "Encountered the beginning of a %s tag" % tag
        if tag == 'a':
            self.is_a = True
            if len(attrs) == 0:
                pass
            else:
                for (variable, value) in attrs:
                    if variable == "href":
                        self.cur_tag_value = value
        else:
            self.is_h3 = True

    def handle_data(self, data):
        if self.is_a:
            self.cur_tag_key = data
        elif self.is_h3:
            self.cur_tag_key = data
            self.cur_tag_value = 'h3'

    def handle_endtag(self, tag):
        if tag == 'a' or tag == 'h3':
            self.is_a = False
            self.is_h3 = False
            if self.cur_tag_key == '' and self.cur_tag_value == '':
                pass
            else:
                self.links.append([self.cur_tag_key, self.cur_tag_value])
                self.cur_tag_key = ''
                self.cur_tag_value = ''


def get_links():
    html_code = file_utils.read2mem('/home/cwh/Mission/bookmarks_16_3_23.html')
    hp = LinkParser()
    hp.feed(html_code)
    hp.close()
    try:
        os.remove('star.md')
    except FileNotFoundError:
        pass
    file_utils.append2file('star.md', '#我的收藏\n>他山之石，可以攻玉\n\n开发过程中收藏在Chrome书签栏里的技术文章，与自己的文章分开\n\n主要涉及python，android，ubuntu等内容，我自己常常在这里面找回忘了的知识。')
    for word in hp.links:
        if word[1] == 'h3':
            file_utils.append2file('star.md', '##' + word[0] + '\n\n')
            print(word[0] + '\n')
        else:
            file_utils.append2file('star.md', '- [' + word[0] + '](' + word[1] + ')\n\n')
            print('- [' + word[0] + '](' + word[1] + ')\n')


# get_links()

class TdParser(HTMLParser):
    def error(self, message):
        pass

    is_td = False
    tds = []
    cur_tag_key = ''
    cur_tag_value = ''

    def __init__(self):
        HTMLParser.__init__(self)

    def handle_starttag(self, tag, attrs):
        # print "Encountered the beginning of a %s tag" % tag
        if tag == 'td':
            self.is_td = True
            if len(attrs) == 0:
                pass
            else:
                for (variable, value) in attrs:
                    if variable == "href":
                        self.cur_tag_value = value

    def handle_data(self, data):
        if self.is_td:
            self.cur_tag_key = data

    def handle_endtag(self, tag):
        if tag == 'td':
            self.is_td = False
            if self.cur_tag_key == '' and self.cur_tag_value == '':
                pass
            else:
                self.tds.append([self.cur_tag_key, self.cur_tag_value])
                self.cur_tag_key = ''
                self.cur_tag_value = ''


def get_tds(src):
    hp = TdParser()
    hp.feed(src)
    hp.close()
    for word in hp.tds:
        if '姓名' in word[1] or ' 房间号：' in word[1]:
            file_utils.append2file('tds.txt', '\n')
            print(word[1] + '\n')


def test_get_tds():
    html_code = file_utils.read2mem('stu_dom.html')
    get_tds(html_code)

test_get_tds()