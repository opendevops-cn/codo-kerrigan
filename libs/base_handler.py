#!/usr/bin/env python
# -*-coding:utf-8-*-

from websdk2.base_handler import BaseHandler as SDKBaseHandler


class BaseHandler(SDKBaseHandler):
    def __init__(self, *args, **kwargs):
        super(BaseHandler, self).__init__(*args, **kwargs)

    def prepare(self):
        self.xsrf_token
        self.codo_login()