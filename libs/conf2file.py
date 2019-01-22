import requests


class ConfApi:
    def __init__(self):
        self.domain = 'http://172.16.0.223:8001'

    def get_project_id(self, key):
        # 获取项目ID
        _uri = '/api/project?project_code=%s' % key
        print(_uri)
        _r = requests.get(self.domain + _uri).json()

        return _r.id

    def get_project_details(self, id):
        # 获取配置文件内容并生成本地配置文件
        _uri = '/api/config/%d/true' %(id)
        _r = requests.get(self.domain + _uri).json()

        filename = _r.get('filename')
        content = _r.get('content')

        with open('/tmp/' + filename) as f:
            f.write(content)

        print('success')

if __name__ == '__main__':
    obj = ConfApi()
    obj.get_project_id('/conf/shenshuo/dev/nginx/demo.conf')