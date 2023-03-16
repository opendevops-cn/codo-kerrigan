FROM centos:7
# 设置编码
ENV LANG en_US.UTF-8
# 同步时间
ENV TZ=Asia/Shanghai
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

RUN yum install -y bind-utils python3 git
# 3. 安装pip依赖
RUN pip3 install --upgrade pip
RUN pip3 install -U git+https://github.com/ss1917/ops_sdk.git

#### 以上python3.6通用
ARG SERVICE_NAME
ENV SERVICE_NAME=${SERVICE_NAME}

WORKDIR /data
COPY . .

RUN pip3 install -r docs/requirements.txt &> /dev/null && \
    chmod -R a+x /data/run-py.sh

EXPOSE 8000
CMD /data/run-py.sh ${SERVICE_NAME}

### docker build --build-arg SERVICE_NAME=kerrigan . -t kerrigan_image