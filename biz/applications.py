#!/usr/bin/env python
# -*-coding:utf-8-*-
"""
Author : shenshuo
date   : 2017-10-11
role   : Application
"""

from websdk2.application import Application as myApplication
from biz.handlers.config_handler import config_urls


class Application(myApplication):
    def __init__(self, **settings):
        urls = []
        urls.extend(config_urls)
        super(Application, self).__init__(urls, **settings)


if __name__ == '__main__':
    pass
