"""
pybehance package
"""
import logging

from .downloader import BehanceDownloader as Behance  # noqa

__version__ = "0.2.5"

'''
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s %(funcName)s - %(message)s",
)
'''


