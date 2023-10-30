import os 
import re
import uuid
import time
import requests
from tqdm import tqdm
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By

# 解析页面的标题
def xhs_get_title(url):
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    driver = webdriver.Chrome(options=options)
    driver.get(url)
    time.sleep(2)

    soup = BeautifulSoup(driver.page_source, "html.parser")
    title_tag = soup.find('title')

    if title_tag:
        title = title_tag.text.strip()
        driver.quit()
        return title
    else:
        print("未找到 <title> 标签")
        driver.quit()
        return None

# 解析链接
def xhs_get_title(url):
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    driver = webdriver.Chrome(options=options)
    driver.get(url)
    time.sleep(2)

    soup = BeautifulSoup(driver.page_source, "html.parser")
    title_tag = soup.find('title')

    if title_tag:
        title = title_tag.text.strip()
        driver.quit()
        return title
    else:
        print("未找到 <title> 标签")
        driver.quit()
        return None

# 解析图片链接
def xhs_get_image_url(url):
    img_urls = []
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    driver = webdriver.Chrome(options=options)
    driver.get(url)
    time.sleep(5)

    soup = BeautifulSoup(driver.page_source, "html.parser")
    image_list = driver.find_elements(By.CLASS_NAME, 'swiper-slide')

    for image in image_list:
        tmp = image.get_attribute("style")
        tmp = re.findall('url\(\"(.*?)\"\)', tmp)
        img_urls.append(tmp[0])

    driver.quit()
    return list(set(img_urls))

# 下载图片
def xhs_download_image(url, save_path):
    r = requests.get(url, stream=True)
    with open(os.path.join(save_path, str(uuid.uuid4()) + ".jpg"), "wb") as f:
        for chunk in r.iter_content(chunk_size=512):
            f.write(chunk)
    return True

