#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Contact : 191715030@qq.com
Author  : shenshuo
Date    : 2019/1/21
Desc    : 配置管理 API
"""

import logging
import re
import json
import difflib
from libs.etcd import Etcd3Client
from models.kerrigan import KerriganProject, KerriganConfig, KerriganHistory, KerriganPublish, KerriganPermissions
from sqlalchemy import or_
from websdk2.model_utils import CommonOptView, model_to_dict
from websdk2.db_context import DBContextV2 as DBContext


# opt_proj_obj = CommonOptView(KerriganProject)


def check_contain_chinese(check_str):
    pattern = re.compile(r'[\u4e00-\u9fff]')
    return bool(pattern.search(check_str))


def check_permissions(nickname):
    the_project_list = []
    the_pro_env_list = []
    the_pro_per_dict = {}
    is_admin = False

    with DBContext('r') as session:
        projects = session.query(KerriganPermissions).filter(KerriganPermissions.nickname == nickname).all()

    for msg in projects:
        data_dict = model_to_dict(msg)
        the_project_list.append(data_dict['project_code'])
        the_pro_env_list.append("{}/{}".format(data_dict['project_code'], data_dict['environment']))
        is_admin = data_dict['is_admin'] if data_dict['is_admin'] else is_admin
        the_pro_per_dict[data_dict['project_code']] = data_dict['is_admin']
    return the_pro_env_list, the_pro_per_dict  # 环境权限    项目权限


def is_allowed_access(data_dict, the_project_list, fullname, superuser):
    if superuser:
        return True
    return data_dict['project_code'] in the_project_list or fullname == data_dict['create_user']


def process_etcd_conf(data_dict):
    etcd_conf = data_dict.get('etcd_conf')
    if etcd_conf:
        try:
            etcd_conf = json.loads(etcd_conf)
            etcd_conf['ETCD_PASSWORD'] = "*******"
            data_dict['etcd_conf'] = etcd_conf
        except:
            pass


def _get_project_value(value: str = None):
    if not value:
        return True
    return or_(KerriganProject.project_name.like(f'%{value}%'),
               KerriganProject.project_code.like(f'%{value}%'))


def get_project_list_for_api(key, limit, is_archive, nickname, superuser) -> list:
    project_list = []
    with DBContext('r') as session:
        projects = session.query(KerriganProject).filter(KerriganProject.is_archive == is_archive).filter(
            _get_project_value(key)).limit(int(limit)).all()

    the_pro_env_list, the_pro_per_dict = check_permissions(nickname)
    the_project_list = [p.split('/')[0] for p in the_pro_env_list]

    for msg in projects:
        data_dict = model_to_dict(msg)
        process_etcd_conf(data_dict)
        if is_allowed_access(data_dict, the_project_list, nickname, superuser):
            project_list.append(data_dict)

    return project_list


def add_project_for_api(data: dict) -> dict:
    project_name = data.get('project_name')
    project_code = data.get('project_code')
    nickname = data.get('create_user')

    if not project_code or not project_name:
        return {"code": -1, "msg": '项目代号和名称不能为空'}

    if check_contain_chinese(project_code) or '/' in project_name:
        return {"code": -2, "msg": '项目代号不能包含汉字，项目名称不能包含 /'}

    try:
        with DBContext('w', None, True) as session:
            # 检查项目代号是否重复
            is_exist = session.query(KerriganProject.project_id).filter(
                KerriganProject.project_code == project_code).first()
            if is_exist:
                return {"code": -3, "msg": '项目代号重复'}

            # 添加项目和权限
            session.add(KerriganProject(**data))
            session.add(KerriganPermissions(project_code=project_code, environment='all_env',
                                            nickname=nickname, is_admin=True))

        return {"code": 0, "msg": "创建成功"}
    except Exception as e:
        print(f"添加项目出错：{e}")
        return {"code": -4, "msg": "添加项目失败"}


def put_project_for_api(data: dict) -> dict:
    project_code = data.get('project_code')
    if not project_code:
        return {"code": -1, "msg": "项目代号不能为空"}

    try:
        with DBContext('w', None, True) as session:
            # 检查项目是否存在
            project = session.query(KerriganProject).filter(KerriganProject.project_code == project_code).first()
            if not project:
                return {"code": -2, "msg": "项目不存在"}

            # 更新项目状态为归档
            project.is_archive = True
            session.commit()

        return {"code": 0, "msg": "归档成功"}
    except Exception as e:
        print(f"归档项目出错：{e}")
        return {"code": -3, "msg": "归档项目失败"}


def edit_project_etcd_for_api(data: dict) -> dict:
    try:
        project_code = data.get('project_code')
        etcd_conf = data.get('etcd_conf')
        fullname = data.get('fullname')

        # 参数验证
        if not project_code:
            return dict(code=-1, msg='项目代号不能为空')

        _, the_pro_per_dict = check_permissions(fullname)
        if not the_pro_per_dict.get(project_code):
            return {"code": -2, "msg": "没有权限"}

        # 解析并验证 etcd_conf
        try:
            etcd_conf = json.loads(etcd_conf)
        except Exception as err:
            return {"code": -3, "msg": "格式不符合要求，必须可以格式化为字典的 JSON 字符串"}

        # 更新数据库
        with DBContext('w', None, True) as session:
            project = session.query(KerriganProject).filter(KerriganProject.project_code == project_code).first()
            if not project:
                return {"code": -4, "msg": "项目不存在"}

            if etcd_conf.get('ETCD_PASSWORD') == "*******":
                try:
                    old_etcd_conf = json.loads(project.etcd_conf)
                    etcd_conf['ETCD_PASSWORD'] = old_etcd_conf.get('ETCD_PASSWORD')
                except Exception as err:
                    pass

            project.etcd_conf = json.dumps(etcd_conf)
            session.commit()

        return {"code": 0, "msg": "关联ETCD配置成功"}
    except Exception as e:
        logging.error(f"修改 etcd 请求出错：{e}")
        return {"code": -5, "msg": "处理请求出错"}


def put_etcd(etcd_conf, config_key, content):
    try:
        etcd_conf = json.loads(etcd_conf)
        client = Etcd3Client(hosts=etcd_conf.get('ETCD_HOST_PORT'), user=etcd_conf.get('ETCD_USER'),
                             passwd=etcd_conf.get('ETCD_PASSWORD'))
        prefix = etcd_conf.get('ETCD_PREFIX', '')
        config_key = config_key[1:]
        full_config_key = f'{prefix}{config_key}' if prefix else config_key
        state = client.put(full_config_key, content)
        return state
    except Exception as err:
        logging.error(f"推送数据到 etcd 请求出错：{err}")
        return False
