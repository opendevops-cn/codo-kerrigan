## 配置中心

### 部署文档

#### 创建数据库

```sql
create
database `codo-kerrigan` default character set utf8mb4 collate utf8mb4_unicode_ci;
```

- 初始化表结构 docker部署可以无视

```bash
python3 db_sync.py
```

#### 修改配置

- 根据需要修改 `settings` 中的配置文件。

#### 编译镜像

```bash
docker build --build-arg SERVICE_NAME=kerrigan . -t codo-kerrigan-image
```

#### Docker 启动

> 默认映射出了端口 8030

```bash
docker-compose up -d
```

#### 启动后访问地址为 ` http://0.0.0.0:8030`

#### 测试

```bash
curl -I -X GET -m 10 -o /dev/null -s -w %{http_code} http://0.0.0.0:8030/are_you_ok/
### 返回200 就代表成功了
```

### 注册网关

用户登录 URI 鉴权是通过网关来处理的。详情请参考 [API 网关](https://github.com/ss1917/api-gateway/blob/master/README.md)。

### 调用示例

- 已经封装成类，并提供了获取配置和生成配置文件的示例。具体参考脚本内容：

    - `libs/get_config.py`

## License

本项目采用 [GPL v3.0](https://www.gnu.org/licenses/gpl-3.0.html) 许可。
