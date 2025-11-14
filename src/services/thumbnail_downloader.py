thonpython
import requests
import logging

class ThumbnailDownloader:
    def download(self, url: str, filename: str):
        try:
            logging.info(f"Downloading thumbnail: {url}")
            data = requests.get(url, timeout=10).content
            with open(filename, "wb") as f:
                f.write(data)
        except Exception as e:
            logging.error(f"Failed to download thumbnail: {e}")