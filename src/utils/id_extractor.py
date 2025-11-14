thonpython
import re

def extract_video_id(url: str) -> str:
    """
    Supports:
    - https://www.youtube.com/watch?v=ID
    - https://youtu.be/ID
    - https://youtube.com/shorts/ID
    """
    patterns = [
        r"v=([a-zA-Z0-9_-]{11})",
        r"youtu\.be/([a-zA-Z0-9_-]{11})",
        r"shorts/([a-zA-Z0-9_-]{11})"
    ]

    for p in patterns:
        m = re.search(p, url)
        if m:
            return m.group(1)

    raise ValueError(f"Could not extract video ID from URL: {url}")