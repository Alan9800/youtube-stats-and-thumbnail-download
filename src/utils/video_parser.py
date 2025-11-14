thonpython
import re
from datetime import datetime
import logging

def extract_meta_tag(html, property_name):
    pattern = f'<meta property="{property_name}" content="(.*?)"'
    m = re.search(pattern, html)
    return m.group(1) if m else None

def parse_video_page(html: str, original_url: str):
    # Extract thumbnail from og:image
    thumbnail = extract_meta_tag(html, "og:image")

    # Extract title (not required but good)
    title = extract_meta_tag(html, "og:title")

    # Extract upload date (ISO)
    upload_date = extract_meta_tag(html, "video:release_date")

    # Extract duration (ISO 8601 in meta tag)
    raw_duration = extract_meta_tag(html, "video:duration")
    duration_seconds = int(raw_duration) if raw_duration and raw_duration.isdigit() else 0

    # Extract channel name from meta tag
    channel = extract_meta_tag(html, "og:site_name")

    # Try regex for view count from JSON inside HTML
    view_regex = r'"viewCount":"(\d+)"'
    view_match = re.search(view_regex, html)
    view_count = int(view_match.group(1)) if view_match else 0

    # Likes
    like_regex = r'"label":"([\d,]+) likes"'
    like_match = re.search(like_regex, html)
    video_likes = int(like_match.group(1).replace(",", "")) if like_match else 0

    # Profile image
    profile_regex = r'"avatar":{"thumbnails":\[{"url":"(.*?)"'
    prof_match = re.search(profile_regex, html)
    profile_image = prof_match.group(1) if prof_match else None

    # Subscriber count
    subs_regex = r'"subscriberCountText":\{"simpleText":"([\d,]+)"'
    subs_match = re.search(subs_regex, html)
    subs = subs_match.group(1).replace(",", "") if subs_match else 0

    # Upload date conversions
    if upload_date:
        dt = datetime.fromisoformat(upload_date.replace("Z", "+00:00"))
        upload_epoch = int(dt.timestamp())
        formatted = dt.strftime("%Y-%m-%d %H:%M:%S")
    else:
        dt = None
        upload_epoch = 0
        formatted = None

    return {
        "video_id": extract_video_id_from_html(html),
        "thumbnail_url": thumbnail,
        "view_count": view_count,
        "description": extract_meta_tag(html, "og:description"),
        "upload_date": upload_date,
        "upload_date_epoch": upload_epoch,
        "upload_date_formatted": formatted,
        "duration": str(duration_seconds),
        "video_url": original_url,
        "profile_name": channel,
        "profile_image_url": profile_image,
        "channel_subscribers": int(subs),
        "channel_handle": extract_channel_handle(html),
        "video_likes": video_likes
    }

def extract_video_id_from_html(html: str):
    m = re.search(r'"videoId":"(.*?)"', html)
    return m.group(1) if m else None

def extract_channel_handle(html: str):
    m = re.search(r'"canonicalBaseUrl":"(.*?)"', html)
    return m.group(1) if m else None