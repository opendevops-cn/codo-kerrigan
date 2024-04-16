#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Contact : 191715030@qq.com
Author  : shenshuo
Date    : 2018/12/24
Desc    : 生成表结构
"""

from sqlalchemy import create_engine
from websdk2.consts import const
from models.kerrigan import Base
from settings import settings as app_settings

# ORM创建表结构

default_configs = app_settings[const.DB_CONFIG_ITEM][const.DEFAULT_DB_KEY]
engine = create_engine(
    f'mysql+pymysql://{default_configs.get(const.DBUSER_KEY)}:'
    f'{default_configs.get(const.DBPWD_KEY)}@{default_configs.get(const.DBHOST_KEY)}:'
    f'{default_configs.get(const.DBPORT_KEY)}/{default_configs.get(const.DBNAME_KEY)}'
    f'?charset=utf8mb4',
    echo=True
)


def create():
    Base.metadata.create_all(engine)
    print('[Success] 表结构创建成功!')


def drop():
    Base.metadata.drop_all(engine)


if __name__ == '__main__':
    create()
