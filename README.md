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
- 修改 doc/nginx_ops.conf 的server_name  例如 改为 kerrigan.opendevops.cn
- 修改 doc/supervisor_ops.conf 内容来控制进程数量
#### 编译镜像
```bash
docker build . -t kerrigan_image
```
#### docker 启动
> 此处要保证 变量正确
```bash
docker-compose up -d
```
#### 启动后访问地址为 kerrigan.opendevops.cn:8030 在API网关上注册，注册示例参考API网关
### 注册网关
> 参考[api网关](https://github.com/ss1917/api-gateway/blob/master/README.md)
## License

Everything is [GPL v3.0](https://www.gnu.org/licenses/gpl-3.0.html).
