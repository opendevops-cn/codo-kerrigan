#!/usr/bin/env python
# -*-coding:utf-8-*-
"""
Contact : 191715030@qq.com
Author  : shenshuo
Date    : 2019/1/29
Desc    : 获取配置文件内容，
          要确保有全局权限 /kerrigan/v1/conf/publish/
          要确保有当前项目配置获取权限
"""

import os
import requests
import json


class ConfApi:
    def __init__(self):
        self.user = 'publish'
        self.pwd = 'shenshuo'
        self.login_api = 'http://gw.shinezone.net.cn/api/accounts/login/'
        self.conf_path ='/tmp'
        self.conf_config_api = "http://gw.shinezone.net.cn/api/kerrigan/v1/conf/publish/config/"
        self.conf_service_api = "http://gw.shinezone.net.cn/api/kerrigan/v1/conf/publish/service/"


    def login(self):
        try:
            headers = {"Content-Type": "application/json"}
            params = {"username": self.user, "password": self.pwd}
            result = requests.post(self.login_api, data=json.dumps(params), headers=headers)

            ret = json.loads(result.text)
            if ret['code'] == 0:
                return ret['auth_key']
            else:
                print(ret)
                exit(-1)
        except Exception as e:
            print('[Error:] 用户:{} 接口登陆失败，错误信息：{}'.format(self.user, e))
            exit(-2)


    def get_config_details(self, project_code, environment, service, filename):
        # 获取配置文件内容
        __token = self.login()
        try:
            _params = {'project_code': project_code, 'environment': environment,'service':service,'filename':filename}
            res = requests.get(self.conf_config_api, params=_params, cookies=dict(auth_key=__token))
            ret = json.loads(res.content)
            if ret['code'] == 0: return ret['data']
        except Exception as e:
            print('[Error:] 发布配置接口连接失败，错误信息：{}'.format(e))
            exit(-2)


    def get_service_details(self, project_code, environment, service):
        # 获取服务所有配置内容
        __token = self.login()
        try:
            _params = {'project_code': project_code, 'environment': environment,'service':service}
            res = requests.get(self.conf_service_api, params=_params, cookies=dict(auth_key=__token))
            ret = json.loads(res.content)
            if ret['code'] == 0: return ret['data']
        except Exception as e:
            print('[Error:] 发布配置接口连接失败，错误信息：{}'.format(e))
            exit(-2)


    def create_config_file(self, project_code, environment, service, filename):
        # 生成配置文件
        config_data = self.get_config_details(project_code, environment, service, filename)
        for k,v in config_data.items():
            config_file = self.conf_path + k
            dir_name, _ = os.path.split(config_file)
            if not os.path.exists(dir_name):
                os.makedirs(dir_name)
            with open(config_file ,'a+') as f:
                f.write(v)
            print('config file path is {}'.format(config_file))
        print('success')

    def create_config_key(self, config_key):
        ### 根据配置KEY 生成配置文件
        config_list = os.path.split(config_key)
        config_dir, filename = config_list[0],config_list[1]
        _, project_code, environment, service = config_dir.split('/')

        config_data = self.get_config_details(project_code, environment, service, filename)
        for k,v in config_data.items():
            config_file = self.conf_path + k
            dir_name, _ = os.path.split(config_file)
            if not os.path.exists(dir_name):
                os.makedirs(dir_name)
            with open(config_file ,'a+') as f:
                f.write(v)
            print('config file path is {}'.format(config_file))
        print('success')

    def create_service_config_file(self, project_code, environment, service):
        # 生成服务所有配置文件
        config_data = self.get_service_details(project_code, environment, service)
        for k,v in config_data.items():
            config_file = self.conf_path + k
            dir_name, _ = os.path.split(config_file)
            if not os.path.exists(dir_name):
                os.makedirs(dir_name)
            with open(config_file ,'a+') as f:
                f.write(v)
            print('config file path is {}'.format(config_file))
        print('success')

if __name__ == '__main__':
    obj = ConfApi()
    # print(obj.get_config_details('ss', 'dev', 'nginx', 'nginx.conf'))
    # print(obj.get_service_details('ss', 'dev', 'nginx'))
    obj.create_config_file('ss','dev','nginx','nginx.conf')
    # obj.create_config_key('/kerrigan/dev/kubernetes/deployment.yaml')
    # obj.create_service_config_file('ss', 'dev', 'nginx')
