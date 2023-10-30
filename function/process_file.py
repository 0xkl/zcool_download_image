import re
import os
import hashlib

# 处理非法文字，将非法文字替换成下划线
def clean_folder_name(folder_name):
    return re.sub(r'[\/:*?"<>|"]', '_', folder_name)

# 为日志处理 非法emoji表情
def clean_titel_emoji(title):
    return re.sub(r'\W', '', title)

# 随机生成哈希值
def generate_hash():
    return hashlib.sha1(os.urandom(128)).hexdigest()[:5]

# 抽取文中的 url
def find_url(string):
    tmp = string.replace("，", " ")
    return re.search("(?P<url>https?://[^\s]+)", tmp).group("url")

# 处理重名的问题函数
def avoid_duplicate_file_names(folder_path, file_name):
    base_name, extension = os.path.splitext(file_name)
    # index 暂时不知道用来干啥
    # count 用来排序文件名迭代
    index,count = 1, 0
    while os.path.exists(os.path.join(folder_path, file_name)):
        hash_suffix = generate_hash()  # 生成哈希乱码
        new_file_name = f"{base_name}_{count}_{hash_suffix}.png"
        index += 1
        count += 1
        file_name = new_file_name
    return file_name