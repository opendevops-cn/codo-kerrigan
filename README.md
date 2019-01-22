## 任务系统

###  部署文档

> <font size="4" color="#dd0000">此系统尽量分布式安装</font> 
#### 创建数据库
```sql
create database `codo-kerrigan` default character set utf8mb4 collate utf8mb4_unicode_ci;
```

#### 修改配置
- 对settings 里面的配置文件进行修改
- 修改 doc/nginx_ops.conf 的server_name  例如 改为 task.opendevops.cn
- 修改 doc/supervisor_ops.conf 内容来控制进程数量
#### 编译镜像
```bash
docker build . -t codo-kerrigan_image
```
#### docker 启动
> 此处要保证 变量正确
```bash
docker-compose up -d
```
#### 启动后访问地址为 task.opendevops.cn：8020 在API网关上注册，注册示例参考API网关
### 注册网关
> 参考[api网关](https://github.com/ss1917/api-gateway/blob/master/README.md)
## License

Everything is [GPL v3.0](https://www.gnu.org/licenses/gpl-3.0.html).
