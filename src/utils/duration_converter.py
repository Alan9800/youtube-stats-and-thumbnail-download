thonpython
def convert_duration(seconds_str: str):
    try:
        seconds = int(seconds_str)
    except ValueError:
        return "00:00:00", 0

    hours = seconds // 3600
    minutes = (seconds % 3600) / 60
    minutes = int(minutes)
    secs = seconds - (hours * 3600 + minutes * 60)

    formatted = f"{hours:02}:{minutes:02}:{secs:02}"
    return formatted, seconds