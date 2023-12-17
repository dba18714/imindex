# seeds.py 或任何自定义脚本文件
from django_seed import Seed
from .models import Link


def run_seeding():
    seeder = Seed.seeder()
    seeder.add_entity(Link, 10)  # 为 MyModel 生成 10 个实例
    seeder.execute()

# 运行：
# 启动 Django shell：
# python manage.py shell
# 在 shell 中导入并运行函数：
# from ims.seeds import run_seeding; run_seeding()
