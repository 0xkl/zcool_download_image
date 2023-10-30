'''
download_main()
说明：所有平台下载代码的封装库，只包含一个参数就是目标链接，目前只封装了两个平台（小红书和站酷）。
使用：只需要将url作为参数，传递给函数就可以进行下载和使用。
'''

import os
import datetime
# 小红书包含库
from .xhs.xhs_download_img import xhs_download_image, xhs_get_image_url, xhs_get_title

# 站酷包含库
from .zcool.zcool_download_img import zcool_download_image, zcool_get_image_url

# behance 包含库
from .behance.downloader import BehanceDownloader

# 解决文中非法字符
from .process_file import clean_folder_name
from .process_file import clean_titel_emoji

# 请求头
headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36 Edg/87.0.664.75'
    }
# 保存地址
ZCOOL_FOLDER_PATH = fr'\\Airdisk_q3x_cd0/数据-a/2023/脚本/downloaded_files/'
XHS_FOLDER_PATH = fr'\\Airdisk_q3x_cd0/数据-a/2023/脚本/downloaded_files/'
BEHANCE_FOLDER_PATH = fr'\\Airdisk_q3x_cd0/数据-a/2023/脚本/downloaded_files/'

'''
download_log() - 下载日志函数
参数1：日志保存地址
参数2：下载作品标题
参数3：下载作品链接

返回值：返回日志保存地址
'''
def download_log(log_path, title, url):
    # 时间板块，获取年、月、日、小时、分钟
    current_datetime = datetime.datetime.now()
    
    current_year = current_datetime.year
    current_month = current_datetime.month
    current_day = current_datetime.day
    current_hour = current_datetime.hour
    current_minute = current_datetime.minute

    current_all = f'{current_year}-{current_month}-{current_day}-{current_hour}:{current_minute}'

    # 目录板块
    #log_dir = os.path.dirname(log_path)  # 获取 log_path 的目录路径
    parent_dir = os.path.dirname(log_path) # 获取 log_dir 的上一级目录路径
    log_file = os.path.join(parent_dir, 'download_log.txt')  # 创建 download_log.txt 的完整路径

    log_info = f'标题: {clean_titel_emoji(title)}\n链接: {url}\n\n'
    # print(f'logo_path:{log_path}\n')
    # print(f'parent_dir:{parent_dir}\n')

    with open(log_file, 'a') as download_log:
        download_log.write(log_info)
        print(f'下载日志保存到：{log_file}')
    
    return log_file

# 站酷
def zcool_main(zcool_url, name, headers):
    img_urls, title = zcool_get_image_url(zcool_url, headers)
    
    if not img_urls:
            print(f'链接 {zcool_url} 没有找到图片地址，或该网站有反爬虫机制，爬取失败。')

    if title:
        print(f'标题：{title}正在下载...:')
        folder_path =  f'{ZCOOL_FOLDER_PATH}{name}/站酷/{clean_folder_name(title)}' # 使用H1标签内容作为文件夹名称
        # folder_path =  f'{ZCOOL_FOLDER_PATH}{name}\站酷\{clean_folder_name(title)}' # 使用H1标签内容作为文件夹名称
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
            # 下载图片
            zcool_download_image(zcool_url, headers, folder_path, title)

            # 计入下载日志
            '''
            log_path = folder_path.replace(title, 'download_log.txt')
            with open(f'{log_path}', 'a') as download_log:
                download_log.write(f'标题:{clean_titel_emoji(title)}\n链接:{zcool_url}\n\n')
                print(f'下载日志保存到：{log_path}')
            '''
            download_log(folder_path, title, zcool_url)

        else:
            print(f'链接 {zcool_url} 未找到H1标签')
    
    print('所有图片下载完成！')
    return title, folder_path

# 小红书
def xhs_main(xhs_url,name):
    # 获取标题
    title = xhs_get_title(xhs_url)
    if title is None:
        print("无法获取标题，退出程序")
        exit()
    print("标题:", title)

    # 处理标题作为文件夹名称
    folder_name = f'{XHS_FOLDER_PATH}{name}/小红书/{clean_folder_name(title)}'      #  使用H1标签内容作为文件夹名称
    folder_path = os.path.join(folder_name)

    # 如果不存在这个文件夹，就创建一个文件夹
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    # 获取图片链接并下载到文件夹
    image_urls = xhs_get_image_url(xhs_url)
    for image_url in image_urls:
        # 下载图片
        xhs_download_image(image_url, folder_path)

    download_log(folder_path, title, xhs_url)
    print('所有图片下载完成！')
    return title, folder_name

'''
# Behance
# behance_url： behance作品链接
# name: 谁在使用
# class_name: 提取span标签类型里面的内容作为标题
'''
def behance_main(behance_url, name, class_name):
    # 初始化
    behance = BehanceDownloader()
    
    # 标题
    title_name = behance.extract_span_content(behance_url, class_name)
    # 路径
    folder_path = f'{BEHANCE_FOLDER_PATH}{name}/Behance/{clean_folder_name(title_name)}'
    behance.path_to_save = folder_path

    data = behance.get_pictures_list(behance_url)
    print(f'标题:{title_name}')

    behance.download_pictures()

    # 日志
    download_log(folder_path, title_name, behance_url)

    return title_name, folder_path