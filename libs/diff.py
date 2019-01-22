import difflib
from commons.models import Setting
from kerrigan.models import Publish
from kerrigan.backends.etcd_api import EtcdApi


def diffApp(config, diff_value):
    try:
        enable_etcd = Setting.objects.get(key='enable_etcd').value
    except Setting.DoesNotExist:
        enable_etcd = 0

    if enable_etcd == 0:
        try:
            _p = Publish.objects.get(config=config)
            src_value = _p.content.splitlines()
        except Publish.DoesNotExist:
            return {"state": 0, "message": "此项目可能还未正式发布过，无法获取到配置"}

    if enable_etcd == 1:
        key = '/conf/%s/%s/%s/%s' % (
            config.project.project_code,
            config.environment,
            config.service,
            config.filename
        )

        _r = EtcdApi().read(key)
        if _r.get('state'):
            src_value = _r.get('value').splitlines()
        else:
            return {"state": 0, "message": "获取etcd value失败：%s" % (_r.get('message'))}

    try:
        diff_value = diff_value.splitlines()
        html = difflib.HtmlDiff().make_file(src_value, diff_value, context=True, numlines=3)

        return {"state": 1, "message": html}
    except Exception as e:
        return {"state": 0, "message": str(e)}
