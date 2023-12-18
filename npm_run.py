import subprocess
import os


def main():
    # 启动 Tailwind CSS 监视进程
    os.system("cd jstoolchain && npm run tailwind-watch")


if __name__ == "__main__":
    main()
