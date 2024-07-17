import re

def remove_emojis(text):
    emoji_pattern = re.compile(
        "["
        u"\U0001F600-\U0001F64F"  # emoticons
        u"\U0001F300-\U0001F5FF"  # symbols & pictographs
        u"\U0001F680-\U0001F6FF"  # transport & map symbols
        u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
        u"\U00002702-\U000027B0"
        u"\U000024C2-\U0001F251"
        "]+", flags=re.UNICODE)
    return emoji_pattern.sub(r'', text)

def convert_views(view_str):
    if 'K' in view_str:
        return int(float(view_str.replace('K', '')) * 1000)
    elif 'M' in view_str:
        return int(float(view_str.replace('M', '')) * 1000000)
    else:
        return int(view_str)