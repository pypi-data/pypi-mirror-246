"""
This is where I'm putting all the functions that don't belong anywhere else
"""
import re

def show_message(code):
    error_dict = {
        "search_too_long": "Error: Search text must be less than 40 characters",
        "no_matches_found": "No matches found.\n- Try shortening the search text or use wildcards to match partial words.",
        "channel_not_found": "channel not found.\n- Try using channel id",
        "multiple_channels_found": "Multiple channels found.\n- Try using id",
        "channel_url_not_correct": "The given channel URL is not correct, expected pattern : https://www.youtube.com/@TimDillonShow/videos",
    }

    print(error_dict[code])


def time_to_secs(time_str):
    """
    converts timestamp to seconds youtube urls. Subtracts 3 seconds to give a buffer. 
    """
    time_rex = re.search("^(\d\d):(\d\d):(\d\d)",time_str)
    hours = int(time_rex.group(1)) * 3600 
    mins = int(time_rex.group(2)) * 60
    secs = int(time_rex.group(3)) 
    total_secs =  hours + mins + secs

    return total_secs - 3


def parse_vtt(file_path):
    """
    extracts start time and text from vtt file and return a list of dicts
    """
    result = []

    time_pattern = "^(.*) align:start position:0%"

    with open(file_path, "r") as f:
        lines = f.readlines()

    for count, line in enumerate(lines):
        time_match = re.match(time_pattern, line)

        if time_match:
            start = re.search("^(.*) -->",time_match.group(1))
            start_time = start.group(1)
            sub_titles = lines[count + 1]

            # prevent duplicate entries
            if result and result[-1]['text'] == sub_titles.strip('\n'):
                continue
            else:   
                result.append({
                    'start_time': start_time,
                    'text': sub_titles.strip('\n'),
                })

    return result 


def get_api_key():
    import os
    api_key = os.environ.get("OPENAI_API_KEY")

    if api_key is None:
        return None
    return api_key


def get_time_delta(timestamp1, timestamp2):
    from datetime import datetime
    format_string = "%H:%M:%S.%f"
    dt1 = datetime.strptime(timestamp1, format_string)
    dt2 = datetime.strptime(timestamp2, format_string)
    diff = dt2 - dt1
    # convert to string "HH:MM:SS"
    diff = str(diff).split(".")[0]

    return diff 