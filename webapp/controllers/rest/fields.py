# -*- coding: utf-8 -*-
# @Author: liuli
# @Date:   2017-04-05 17:41:54
# @Last Modified by:   XUEQUN
# @Last Modified time: 2017-08-08 21:40:30
#UnicodeEncodeError: 'ascii' codec can't encode characters in position 64-66: ordinal not in range(128)
#将html格式转化成json格式

import sys
reload(sys)
sys.setdefaultencoding( "utf-8" )

from HTMLParser import HTMLParser
from flask_restful import fields


class HTMLStripper(HTMLParser):
    def __init__(self):
        self.reset()
        self.fed = []

    def handle_data(self, d):
        self.fed.append(d)

    def get_data(self):
        return ''.join(self.fed)


def strip_tags(html):
    s = HTMLStripper()
    s.feed(html)

    return s.get_data()


class HTMLField(fields.Raw):
    def format(self, value):
        return strip_tags(str(value))
