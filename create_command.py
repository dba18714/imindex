import os
import sys


# 本脚本用于快捷创建Django命令行，使用方法：python create_command.py myapp mycommand

def create_django_command(app_name, command_name):
    # 构建路径
    command_dir = os.path.join(app_name, 'management/commands')
    command_file = os.path.join(command_dir, f'{command_name}.py')
    init_file = os.path.join(command_dir, '__init__.py')

    # 检查 app 目录是否存在
    if not os.path.isdir(app_name):
        print(f"应用 '{app_name}' 不存在。")
        sys.exit(1)

    # 创建目录
    os.makedirs(command_dir, exist_ok=True)

    # 创建 __init__.py 文件
    if not os.path.exists(init_file):
        with open(init_file, 'w') as f:
            pass  # 创建一个空文件

    # 创建命令文件
    if not os.path.exists(command_file):
        with open(command_file, 'w') as f:
            f.write("from django.core.management.base import BaseCommand, CommandError\n\n\n")
            f.write("class Command(BaseCommand):\n")
            f.write("    help = '描述你的命令做什么'\n\n")
            f.write("    def add_arguments(self, parser):\n")
            f.write("        # 添加命令行参数\n")
            f.write("        pass\n\n")
            f.write("    def handle(self, *args, **kwargs):\n")
            f.write("        # 命令的主要逻辑写在这里\n")
            f.write("        pass\n")
        print(f"命令 '{command_name}' 已在 '{app_name}' 应用中创建。")
    else:
        print(f"命令 '{command_name}' 已经存在。")


if __name__ == '__main__':
    if len(sys.argv) < 3:
        print("使用方法: python create_command.py [app_name] [command_name]")
        sys.exit(1)

    app_name = sys.argv[1]
    command_name = sys.argv[2]

    create_django_command(app_name, command_name)
