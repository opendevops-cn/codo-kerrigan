#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Contact : 191715030@qq.com
Author  : shenshuo
Date    : 2019/1/21
Desc    : 启动文件
"""

import fire
from tornado.options import define
from websdk2.program import MainProgram
from settings import settings as app_settings
from biz.applications import Application as config_api

define("service", default='api', help="start service flag", type=str)


class MyProgram(MainProgram):
    def __init__(self, progress_id='config'):
        self.__app = None
        settings = app_settings
        self.__app = config_api(**settings)
        super(MyProgram, self).__init__(progress_id)
        self.__app.start_server()


if __name__ == '__main__':
    fire.Fire(MyProgram)