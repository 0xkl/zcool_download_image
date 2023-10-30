import httpx
from tqdm import tqdm
from pathlib import Path
from typing import Optional, Union
from bs4 import BeautifulSoup

from .settings import BEHANCE_STORAGE_URL

class BehanceDownloader:
    def __init__(
        self,
        storage_path: str = BEHANCE_STORAGE_URL,
        path_to_save: Optional[Union[str, Path]] = None,
    ):
        self.storage_path = storage_path
        self.pictures: list = []
        self.path_to_save = path_to_save

    def check_path_to_save_exist(self):
        if self.path_to_save:
            if not Path(self.path_to_save).is_dir():
                Path(self.path_to_save).mkdir(parents=True, exist_ok=True)

    @staticmethod
    def _requests(url: str):
        response = httpx.get(url)
        response.raise_for_status()
        return response.text
    
    def extract_span_content(self, link: str, class_name: str):
        raw_html = self._requests(link)
        tree = BeautifulSoup(raw_html, "html.parser")

        span_tag = tree.find("span", class_=class_name)
        span_content = span_tag.get_text()

        return span_content
        
        '''
        if span_tag:
            span_content = span_tag.get_text()
            print(f"Content of <span> tag with class {class_name}: {span_content}")
        else:
            print(f"No <span> tag with class {class_name} found on the page.")
        '''
    def get_pictures_list(self, link: str) -> list:
        self.pictures = []
        raw_html = self._requests(link)
        tree = BeautifulSoup(raw_html, "html.parser")

        for _item in tree.find_all("img"):
            try:
                src_set = _item.get("srcset").split(",")
                for _image in src_set:
                    image = _image.strip()
                    if image[: len(self.storage_path)] == self.storage_path:
                        self.pictures.append(image.split()[0])
            except AttributeError:
                pass
        print(f"url {link} has {len(self.pictures)} pictures")
        return self.pictures

    def get_data(self) -> list:
        return self.pictures

    def _download(self, link: str):
        response = httpx.get(link, stream=True)

        if response.status_code == 200:
            total_size = int(response.headers.get('content-length', 0))
            file_name = link.split("/")[-1]
            path_to_save = Path(self.path_to_save) / file_name if self.path_to_save else file_name

            with open(path_to_save, "wb") as image_file:
                with tqdm(total=total_size, unit='B', unit_scale=True, unit_divisor=1024) as progress_bar:
                    for data in response.iter_content(chunk_size=1024):
                        image_file.write(data)
                        progress_bar.update(len(data))
            
            print(f"image {file_name} saved to {path_to_save}")
        else:
            print(f"Failed to download image from url: {link}")

    def download_pictures(self):
        print("Start download pictures")
        self.check_path_to_save_exist()
        if not self.pictures:
            print("pictures list is empty, please use get_pictures_list(example behance url) method")
        else:
            total_images = len(self.pictures)
            total_size = 0
            with tqdm(total=total_images, unit='image', unit_scale=True) as progress_bar:
                for image_url in self.pictures:
                    file_name = image_url.split("/")[-1]
                    path_to_save = Path(self.path_to_save) / file_name if self.path_to_save else file_name
                    
                    with httpx.stream("GET", image_url) as response:
                        total_size += int(response.headers.get('content-length', 0))
                        with open(path_to_save, "wb") as image_file:
                            for chunk in response.iter_bytes(chunk_size=1024):
                                if chunk:
                                    image_file.write(chunk)
                        progress_bar.update(1)
                print(f"Downloaded {total_images} images, total size: {total_size} bytes")