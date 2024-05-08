#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Contact : 191715030@qq.com
Author  : shenshuo
Date    : 2019/1/21
Desc    : 数据库ORM
"""

from datetime import datetime
from sqlalchemy import Column, String, Integer, DateTime, Text, Boolean
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class KerriganProject(Base):
    __tablename__ = 'kerrigan_project'

    # 项目表
    project_id = Column('project_id', Integer, primary_key=True, autoincrement=True)

    project_code = Column('project_code', String(50), unique=True, nullable=False)
    project_name = Column('project_name', String(150), index=True)
    etcd_conf = Column('etcd_conf', String(255), default='')  # 关联ETCD配置

    is_archive = Column('is_archive', Boolean(), default=False, index=True)  # 归档
    create_user = Column('create_user', String(150))
    create_time = Column('create_time', DateTime(), default=datetime.now, onupdate=datetime.now)


class KerriganConfig(Base):
    __tablename__ = 'kerrigan_config'

    # 配置表
    id = Column('id', Integer, primary_key=True, autoincrement=True)

    project_code = Column('project_code', String(50), index=True)
    environment = Column('environment', String(25), index=True)
    service = Column('service', String(50))
    filename = Column('filename', String(50))
    content = Column('content', Text())

    is_published = Column('is_published', Boolean(), default=False, index=True)
    is_deleted = Column('is_deleted', Boolean(), default=False, index=True)

    create_user = Column('create_user', String(100))
    create_time = Column('create_time', DateTime(), default=datetime.now, onupdate=datetime.now)


class KerriganHistory(Base):
    __tablename__ = 'kerrigan_history'

    # 历史版本
    id = Column('id', Integer, primary_key=True, autoincrement=True)
    config = Column('config', String(500), nullable=False, index=True)  ### 关联配置
    content = Column('content', Text(), nullable=False)
    create_user = Column('create_user', String(150))
    create_time = Column('create_time', DateTime(), default=datetime.now, onupdate=datetime.now)


class KerriganPublish(Base):
    __tablename__ = 'kerrigan_publish'

    id = Column('id', Integer, primary_key=True, autoincrement=True)
    config = Column('config', String(500), nullable=False, index=True)  # 关联配置
    content = Column('content', Text(), nullable=False)
    create_user = Column('create_user', String(150))
    create_time = Column('create_time', DateTime(), default=datetime.now, onupdate=datetime.now)


class KerriganPermissions(Base):
    __tablename__ = 'kerrigan_permissions'
    # 数据权限表
    id = Column('id', Integer, primary_key=True, autoincrement=True)
    project_code = Column('project_code', String(50), nullable=False)
    environment = Column('environment', String(25), nullable=False)
    nickname = Column('nickname', String(150))
    is_admin = Column('is_admin', Boolean(), default=False)
    create_time = Column('create_time', DateTime(), default=datetime.now, onupdate=datetime.now)
