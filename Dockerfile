FROM python:3.11.4
ENV PYTHONUNBUFFERED 1

# 创建工作目录
RUN mkdir /code
WORKDIR /code

# 安装依赖
COPY requirements.txt /code/
RUN pip install -r requirements.txt

# 拷贝您的代码到工作目录
COPY . /code/

# 安装 postgresql-client
RUN apt-get update && apt-get install -y postgresql-client

# 复制和设置 wait-for-db.sh 脚本
COPY wait-for-db.sh /wait-for-db.sh
RUN chmod +x /wait-for-db.sh
