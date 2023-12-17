# 开发环境 macOS Docker

### 构建镜像
```shell
docker-compose -f docker-compose-dev.yml build
```
### 启动服务
```shell
docker-compose -f docker-compose-dev.yml up
```
### 停止服务
```shell
docker-compose -f docker-compose-dev.yml down
```
启动后即可访问：http://127.0.0.1:8000/

### 构建并推送到 Docker Hub
```shell
docker build -t dba18714/imindex:latest . \
&& docker push dba18714/imindex:latest
```

# 生产环境
部署在 Ubuntu 20.04 64 Bit 的 Docker 上

### 启动服务
```shell
docker-compose -f docker-compose-prod.yml up --build
```
### 停止服务
```shell
docker-compose -f docker-compose-prod.yml down
```




# Docker 环境调试

运行 Django 测试
```shell
python manage.py test
```
列出所有运行中的容器
```shell
docker ps
```
列出所有容器（包括未运行的）
```shell
docker ps -a
```
查看所有服务的状态 docker-compose
```shell
docker-compose -f docker-compose-prod.yml ps
```
查看日志 docker-compose
```shell
docker-compose -f docker-compose-prod.yml logs web
```
```shell
docker-compose -f docker-compose-prod.yml logs db
```
```shell
docker-compose -f docker-compose-prod.yml logs redis
```
查看日志 docker
```shell
docker logs imindex-web-1
```
```shell
docker logs imindex-db-1
```
```shell
docker logs imindex-redis-1
```

进入 web, db, redis 容器命令行
```shell
docker exec -it imindex-web-1 /bin/bash
```
```shell
docker exec -it imindex-db-1 /bin/bash
```
```shell
docker exec -it imindex-redis-1 /bin/bash
```
安装 redis-cli
```shell
apt-get update && apt-get install redis-tools
```





### Install flyctl
```shell
brew install flyctl
```
OR
```shell
curl -L https://fly.io/install.sh | sh
```
### Sign In
```shell
fly auth login
```
### 创建 PostgreSQL 数据库
```shell
flyctl postgres create
```
执行完毕后将会得到类似:
> Username:    postgres  
  Password:    XXX  
  Hostname:    tmp01.internal  
  Flycast:     fdaa:3:d8f9:0:1::4  
  Proxy port:  5432  
  Postgres port:  5433  
  Connection string: postgres://postgres:XXX@tmp01.flycast:5432

注意：默认数据库名字是`postgres`，将`Connection string`的值复制到 .env 文件里的`DATABASE_URL`上，并在后面加上 `/postgres`，即：postgres://postgres:XXX@tmp01.flycast:5432/postgres

### Launch a New App
```shell
fly launch
```
### Deploy
```shell
fly deploy
```
✅完成部署

### 其他 Fly 常用命令
```shell
fly logs
```
```shell
fly status
```
```shell
fly ssh console
```
如果部署时提示机器配额超限，则执行此命令将机器缩放为1台后再执行部署即可：
```shell
flyctl scale count 1
```

### 其他 Django 常用命令
```shell
python manage.py makemigrations
```
```shell
python manage.py migrate
```

### 自定义的脚本
一键创建Django命令行
```shell
python create_command.py <myapp> <mycommand>
```

后台地址：域名/admin  
默认管理员：
> 账号：admin  
> 密码：Admin123
