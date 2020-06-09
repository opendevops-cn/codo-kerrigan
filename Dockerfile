FROM registry.cn-hangzhou.aliyuncs.com/sourcegarden/python:centos7-3.6

RUN mkdir -p /var/www/
ADD ./  /var/www/kerrigan/

RUN pip3 install -i https://pypi.tuna.tsinghua.edu.cn/simple -r /var/www/kerrigan/doc/requirements.txt

#RUN python3 /var/www/kerrigan/db_sync.py

#VOLUME /var/log/

COPY docker/nginx_ops.conf /etc/nginx/conf.d/default.conf
COPY docker/supervisor_ops.conf  /etc/supervisord.conf

EXPOSE 80
CMD ["/usr/bin/supervisord"]
