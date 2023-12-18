import subprocess
import os


def main():
    # 启动 Tailwind CSS 监视进程
    subprocess.Popen(["npm", "run", "tailwind-watch"], cwd="jstoolchain")
    subprocess.Popen(["celery", "-A", "mysite", "worker", "-l", "info"])
    # subprocess.Popen("celery -A mysite worker -l info")
    os.system("python manage.py runserver")


if __name__ == "__main__":
    main()
