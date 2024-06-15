import re
import requests
import config
from collections import OrderedDict
from datetime import datetime

def formatChannelName(name):
    """
    Format the channel name with sub and replace and lower
    """
    sub_pattern = (
        r"-|_|\((.*?)\)|\[(.*?)\]| |频道|标清|高清|HD|hd|超清|超高|超高清|地方|卫视|台"
    )
    name = re.sub(sub_pattern, "", name)
    name = name.replace("-卫视", "卫视")
    return name.lower()
    
def parse_template(template_file):
    """
    Parse the template file to extract channel names.
    """
    template_channels = OrderedDict()
    current_category = None

    with open(template_file, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith("#"):
                if "#genre#" in line:
                    current_category = line.split(",")[0].strip()
                    template_channels[current_category] = []
                elif current_category:
                    channel_name = line.split(",")[0].strip()
                    template_channels[current_category].append(channel_name)

    return template_channels

def fetch_channels(url):
    """
    Fetch channel items from a URL.
    """
    channels = OrderedDict()

    try:
        response = requests.get(url)
        response.raise_for_status()
        response.encoding = 'utf-8'
        lines = response.text.split("\n")

        current_category = None

        for line in lines:
            line = line.strip()
            if "#genre#" in line:
                current_category = line.split(",")[0].strip()
                channels[current_category] = []
            elif current_category:
                match = re.match(r"^(.*?),(.*?)$", line)
                if match:
                    channel_name = match.group(1).strip()
                    channel_url = match.group(2).strip()
                    channels[current_category].append((channel_name, channel_url))
                elif line:  # If it's not an empty line and doesn't match comma-separated pattern
                    channels[current_category].append((line, ''))
    except requests.RequestException as e:
        print(f"Failed to fetch channels from the URL: {url}, Error: {e}")

    return channels

def getChannelItems(template_channels, source_urls):
    """
    Get the channel items from the source URLs
    """
    channels = OrderedDict()

    for category in template_channels:
        channels[category] = OrderedDict()

    for url in source_urls:
        if url.endswith(".m3u"):
            converted_url = f"https://fanmingming.com/txt?url={url}"
            response = requests.get(converted_url)
        else:
            response = requests.get(url)

        if response.status_code == 200:
            response.encoding = 'utf-8'
            lines = response.text.split("\n")

            current_category = None

            for line in lines:
                line = line.strip()
                if "#genre#" in line:
                    current_category = line.split(",")[0].strip()
                else:
                    match = re.match(r"^(.*?),(?!#genre#)(.*?)$", line)
                    if match and current_category in channels:
                        channel_name = match.group(1).strip()
                        if channel_name in template_channels[current_category]:
                            channels[current_category].setdefault(channel_name, []).append(match.group(2).strip())
        else:
            print(f"Failed to fetch channel items from the source URL: {url}")

    return channels

def match_channels(template_channels, all_channels):
    """
    Match the channels from all channels with the template channels.
    """
    matched_channels = OrderedDict()

    for category, channel_list in template_channels.items():
        matched_channels[category] = OrderedDict()
        for channel_name in channel_list:
            for online_category, online_channel_list in all_channels.items():
                for online_channel_name, online_channel_url in online_channel_list:
                    if channel_name == online_channel_name:
                        matched_channels[category].setdefault(channel_name, []).append(online_channel_url)

    return matched_channels

def filter_source_urls(template_file):
    """
    Filter source URL.
    """
    template_channels = parse_template(template_file)
    source_urls = config.source_urls

    # Fetch channels from all source URLs
    all_channels = OrderedDict()
    for url in source_urls:
        fetched_channels = fetch_channels(url)
        for category, channel_list in fetched_channels.items():
            if category in all_channels:
                all_channels[category].extend(channel_list)
            else:
                all_channels[category] = channel_list

    # Match the fetched channels with the template
    matched_channels = match_channels(template_channels, all_channels)

    return matched_channels, template_channels

def updateChannelUrlsM3U(channels, template_channels):
    """
    Update the category and channel URLs to the final file in M3U format
    """
    written_urls = set()  # Set to store written URLs

    current_date = datetime.now().strftime("%Y-%m-%d")

    with open("cntv.m3u", "w", encoding="utf-8") as f_m3u:
        f_m3u.write("#EXTM3U\n")

        with open("cntv.txt", "w", encoding="utf-8") as f_txt:
            for category, channel_list in template_channels.items():
                f_txt.write(f"{category},#genre#\n")
                if category in channels:
                    for channel_name in channel_list:
                        if channel_name in channels[category]:
                            for url in channels[category][channel_name]:
                                if url and url not in written_urls and not any(blacklist in url for blacklist in config.url_blacklist):  # Check if网站is not already written and not in blacklist
                                    f_m3u.write(f"#EXTINF:-1 tvg-id=\"\" tvg-name=\"{channel_name}\" tvg-logo=\"https://gitee.com/yuanzl77/TVBox-logo/raw/main/png/{channel_name}.png\" group-title=\"{category}\",{channel_name}\n")
                                    f_m3u.write(url + "\n")
                                    f_txt.write(f"{channel_name},{url}\n")
                                    written_urls.add(url)  # Add URL to written URLs set

            f_txt.write("\n")

if __name__ == "__main__":
    template_file = "demo2.txt"
    channels, template_channels = filter_source_urls(template_file)
    updateChannelUrlsM3U(channels, template_channels)
