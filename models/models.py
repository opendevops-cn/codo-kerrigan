#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Contact : 191715030@qq.com
Author  : shenshuo
Date    : 2019/1/21
Desc    : 数据库ORM
"""

from sqlalchemy import Column, String, Integer, DateTime, Text, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import class_mapper
from datetime import datetime

Base = declarative_base()


def model_to_dict(model):
    model_dict = {}
    for key, column in class_mapper(model.__class__).c.items():
        model_dict[column.name] = getattr(model, key, None)
    return model_dict


class KerriganProject(Base):
    __tablename__ = 'kerrigan_project'

    ### 项目表
    project_id = Column('project_id', Integer, primary_key=True, autoincrement=True)

    project_code = Column('project_code', String(50) ,unique=True ,nullable=False)
    project_name = Column('project_name', String(150))

    create_user = Column('create_user', String(100))
    create_time = Column('create_time', DateTime(), default=datetime.now, onupdate=datetime.now)


class KerriganConfig(Base):
    __tablename__ = 'kerrigan_config'

    ###
    id = Column('id', Integer, primary_key=True, autoincrement=True)

    project_code = Column('project_code', String(50))
    environment = Column('environment', String(18))
    service = Column('service', String(50))
    filename = Column('filename', String(50))
    content = Column('content', Text())

    is_published = Column('is_published', Boolean(), default=False)
    is_deleted = Column('is_deleted', Boolean(), default=False)

    create_user = Column('create_user', String(100))
    create_time = Column('create_time', DateTime(), default=datetime.now, onupdate=datetime.now)


class KerriganHistory(Base):
    __tablename__ = 'kerrigan_history'

    ### 历史
    id = Column('id', Integer, primary_key=True, autoincrement=True)
    config = Column('config', String(500), nullable=False)  ### 关联配置
    content = Column('content', Text(), nullable=False)
    create_user = Column('create_user', String(100))
    create_time = Column('create_time', DateTime(), default=datetime.now, onupdate=datetime.now)


class KerriganPublish(Base):
    __tablename__ = 'kerrigan_publish'

    id = Column('id', Integer, primary_key=True, autoincrement=True)
    config = Column('config', String(500), nullable=False)  ### 关联配置
    content = Column('content', Text(), nullable=False)
    create_user = Column('create_user', String(100))
    create_time = Column('create_time', DateTime(), default=datetime.now, onupdate=datetime.now)


class KerriganPermissions(Base):
    __tablename__ = 'kerrigan_permissions'

    id = Column('id', Integer, primary_key=True, autoincrement=True)
    project_code = Column('project_code', String(50) ,nullable=False)  ###
    environment = Column('environment', String(18),nullable=False)
    nickname = Column('nickname', String(120))
    create_time = Column('create_time', DateTime(), default=datetime.now, onupdate=datetime.now)
