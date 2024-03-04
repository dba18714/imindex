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

RUN apt-get update && apt-get install -y \
    nano \
    postgresql-client \
    cron \
    gettext \
    && rm -rf /var/lib/apt/lists/*

# 复制和设置 wait-for-db.sh 脚本
COPY _for_deploy/wait-for-db.sh /code/_for_deploy/wait-for-db.sh
RUN chmod +x /code/_for_deploy/wait-for-db.sh

COPY _for_deploy/start.sh /code/_for_deploy/start.sh
RUN chmod +x /code/_for_deploy/start.sh

# 复制 cron 任务文件并设置权限
COPY _for_deploy/django_cron_job /etc/cron.d/django_cron_job
RUN chmod 0644 /etc/cron.d/django_cron_job
RUN crontab /etc/cron.d/django_cron_job
