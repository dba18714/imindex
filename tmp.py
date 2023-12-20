import re

str = '0 members, 24 online'

# 使用正则表达式匹配 'members' 前的数字
match = re.search(r'(\d[\d\s,]*)members', str)

# 检查是否找到匹配项
if match:
    number_str = match.group(1)  # 提取数字字符串
    number_str = re.sub(r'\D', '', number_str)

    # 转换为整数
    number = int(number_str)
    print(number)
else:
    number = None  # 如果没有找到相应的数字
