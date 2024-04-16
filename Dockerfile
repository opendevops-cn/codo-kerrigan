FROM rockylinux:9.1

MAINTAINER "shenshuo<191715030@qq.com>"
# 设置编码
ENV LANG C.UTF-8

# 同步时间
ENV TZ=Asia/Shanghai

RUN yum install -y python3 python3-pip git && \
    yum clean all

# 3. 安装pip依赖
RUN pip3 install --upgrade pip
RUN pip3 install -U git+https://github.com/ss1917/codo_sdk.git

#### 以上python3.9通用
ARG SERVICE_NAME
ENV SERVICE_NAME=${SERVICE_NAME}

WORKDIR /data
COPY . .

RUN pip3 install -r docs/requirements.txt &> /dev/null && \
    chmod -R a+x /data/run-py.sh

EXPOSE 8000
CMD /data/run-py.sh ${SERVICE_NAME}

### docker build --no-cache --build-arg SERVICE_NAME=kerrigan . -t codo-kerrigan-image
### docker build --build-arg SERVICE_NAME=kerrigan . -t codo-kerrigan-image
