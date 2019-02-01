## 配置中心

###  部署文档

#### 创建数据库
```sql
create database `codo-kerrigan` default character set utf8mb4 collate utf8mb4_unicode_ci;
```
- 初始化表结构
```bash
python3 /var/www/kerrigan/db_sync.py
```
#### 修改配置
- 对settings 里面的配置文件进行修改
- 修改 doc/nginx_ops.conf 的server_name  例如 改为 kerrigan.opendevops.cn ,当然你也可以直接用IP
- 修改 doc/supervisor_ops.conf 内容来控制进程数量

#### 编译镜像
```bash
docker build . -t kerrigan_image
```
#### docker 启动
> 默认映射出了8030端口
```bash
docker-compose up -d
```
#### 启动后访问地址为 kerrigan.opendevops.cn:8030
#### 测试
```bash
curl -I -X GET -m  10 -o /dev/null -s -w %{http_code}  http://kerrigan.opendevops.cn:8030/are_you_ok/
### 返回200 就代表成功了
```
### 注册网关 用户登录 URI鉴权是通过网关来处理的。
> 参考[api网关](https://github.com/ss1917/api-gateway/blob/master/README.md)

### 调用示例
- 已经封装成类， 并写了获取配置的示例，和生成配置文件示例,具体参考脚本内容
- libs/get_config.py

## License

Everything is [GPL v3.0](https://www.gnu.org/licenses/gpl-3.0.html).
