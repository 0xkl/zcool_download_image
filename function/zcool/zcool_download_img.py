import re
import os
import requests
from tqdm import tqdm
from bs4 import BeautifulSoup
from function.process_file import avoid_duplicate_file_names



# 站酷解析
def zcool_get_image_url(url, headers):
    try:
        web_text = requests.get(url, headers=headers).text
    except requests.exceptions.RequestException as e:
        print(f'请求网页失败：{str(e)}')
        return [], None

    img_pattern = r'<img.*?src="(.*?)".*?>'
    img_list = re.findall(img_pattern, web_text)

    # 使用Beautiful Soup解析页面内容
    soup = BeautifulSoup(web_text, 'html.parser')
    h1_tag = soup.find('h1')

    h1_text = h1_tag.text.strip() if h1_tag else None

    return img_list, h1_text

# 站酷下载
def zcool_download_image(url, headers, folder_path, h1_text):
    try:
        img_urls = zcool_get_image_url(url, headers)[0]  # 获取图片链接
        img_urls_to_download = img_urls[2:-2]  # 跳过前两张和最后两张图片

        for img_url in tqdm(img_urls_to_download, desc='下载进度'):
            try:
                r = requests.get(img_url, stream=True)
                if r.status_code == 200:
                    file_name = os.path.basename(img_url)
                    file_name = f"{file_name}.png"  # 添加 .png 后缀
                    file_name = avoid_duplicate_file_names(folder_path, file_name)  # 处理重名问题
                    file_path = os.path.join(folder_path, file_name)
                    with open(file_path, 'wb') as f:
                        for chunk in r.iter_content(chunk_size=1024):
                            f.write(chunk)
                else:
                    print(f'下载失败: {os.path.basename(img_url)}')
            except Exception as e:
                print(f'下载失败: {os.path.basename(img_url)} - {str(e)}')
    except Exception as e:
        print(f'下载失败: {str(e)}')