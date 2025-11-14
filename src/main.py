thonpython
import json
import logging
from pathlib import Path
from utils.id_extractor import extract_video_id
from utils.video_parser import parse_video_page
from utils.duration_converter import convert_duration
from services.youtube_client import YoutubeClient
from services.thumbnail_downloader import ThumbnailDownloader

logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(message)s')

def load_input(file_path: str):
    with open(file_path, "r") as f:
        return json.load(f)

def save_output(data, file_path: str):
    with open(file_path, "w") as f:
        json.dump(data, f, indent=4)

def main():
    input_path = Path("data/sample_input.json")
    output_path = Path("data/sample_output.json")

    urls = load_input(input_path)
    client = YoutubeClient()
    downloader = ThumbnailDownloader()

    results = []
    for url in urls:
        try:
            video_id = extract_video_id(url)
            logging.info(f"Processing video ID: {video_id}")

            raw_html = client.fetch_html(video_id)
            parsed = parse_video_page(raw_html, url)

            # duration conversions
            formatted_duration, duration_seconds = convert_duration(parsed["duration"])

            parsed["duration"] = formatted_duration
            parsed["duration_seconds"] = duration_seconds

            # download thumbnail
            if parsed.get("thumbnail_url"):
                downloader.download(parsed["thumbnail_url"], f"thumbnail_{video_id}.jpg")

            results.append(parsed)

        except Exception as e:
            logging.error(f"Error processing {url}: {e}")

    save_output(results, output_path)
    logging.info("Finished processing.")

if __name__ == "__main__":
    main()