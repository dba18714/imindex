import re


# 从字符串中提取URL
def extract_url_of_str(text):
    url_pattern = r'https?://[^\s]+'
    match = re.search(url_pattern, text)
    if match:
        return match.group(0)
    return None
