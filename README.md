# 开发环境 macOS Docker

### 前端资源处理
```shell
python npm_run.py
```

### 构建镜像
```shell
docker-compose -f docker-compose-dev.yml build
```
### 启动服务
```shell
docker-compose -f docker-compose-dev.yml up --build --remove-orphans
```
### 停止服务
```shell
docker-compose -f docker-compose-dev.yml down --remove-orphans
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
docker-compose -f docker-compose-prod.yml up --build --remove-orphans
```
### 停止服务
```shell
docker-compose -f docker-compose-prod.yml down --remove-orphans
```




# Docker 环境调试

停止所有容器
```shell
docker stop $(docker ps -a -q)
```
删除所有容器
```shell
docker rm $(docker ps -a -q)
```
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
查看所有相关的服务的状态 docker-compose
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


# 测试覆盖率

`coverage.py` 是一个流行的 Python 工具，用于测量代码覆盖率，即您的测试覆盖了代码的哪些部分。以下是如何在 Django 项目中使用 `coverage.py` 的基本步骤：

### 安装 coverage.py

如果您还没有安装 `coverage.py`，可以通过 pip 安装：

```bash
pip install coverage
```

### 运行测试并收集覆盖率数据

在您的 Django 项目目录中，使用 `coverage` 命令运行测试，并收集覆盖率数据。以下是一个基本的例子：

```bash
coverage run --source='.' manage.py test
```

这个命令告诉 `coverage.py` 监控您的整个项目（通过 `--source='.'` 指定）并运行 `manage.py test`。

### 生成覆盖率报告

测试完成后，您可以生成一个覆盖率报告。以下是两种常见的报告格式：

- **命令行报告**:

  ```bash
  coverage report
  ```

  这个命令将在命令行中输出一个简单的覆盖率报告。

- **HTML 报告**:

  ```bash
  coverage html
  ```

  这个命令将生成一个更详细的 HTML 覆盖率报告，存储在 `htmlcov/` 目录中。您可以在浏览器中打开 `htmlcov/index.html` 文件来查看报告。

### 分析报告

无论是命令行报告还是 HTML 报告，您都可以看到每个文件的覆盖率数据，包括覆盖的行数和未覆盖的行数。这有助于您识别需要更多测试的代码区域。

### 集成到开发流程中

您可以将 `coverage.py` 集成到您的开发和测试流程中，作为代码审查和持续集成的一部分。这有助于确保新添加的代码得到适当的测试。

### 注意事项

- **排除不必要的代码**：您可能想要排除一些不需要测试的代码（如第三方库或特定的配置文件）。可以在 `.coveragerc` 文件中配置这些排除规则。
- **持续集成**：如果您使用持续集成服务，如 Travis CI 或 Jenkins，可以配置它们在每次提交时运行覆盖率测试，并报告任何下降的覆盖率。

使用 `coverage.py` 是一种提高代码质量的有效方式，它可以帮助您识别未被测试的代码，从而提升测试的完整性。