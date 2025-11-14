thonpython
import requests
import logging

class YoutubeClient:
    BASE_URL = "https://www.youtube.com/watch?v="

    def fetch_html(self, video_id: str) -> str:
        url = self.BASE_URL + video_id
        logging.info(f"Fetching {url}")
        resp = requests.get(url, timeout=10)
        resp.raise_for_status()
        return resp.text