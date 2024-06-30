import requests

def check_url(url):
    try:
        response = requests.get(url, timeout=10)
        return response.status_code == 200
    except requests.RequestException:
        return False

def process_iptv_file(input_file, output_file):
    with open(input_file, 'r', encoding='utf-8') as infile, open(output_file, 'w', encoding='utf-8') as outfile:
        for line in infile:
            if "://" in line:
                parts = line.split(',')
                if len(parts) == 2:
                    channel_name, url = parts
                    url = url.strip()
                    if check_url(url):
                        outfile.write(line)

input_file = 'iptv.txt'
output_file = 'live.txt'

process_iptv_file(input_file, output_file)
