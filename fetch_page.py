import requests
import json
from bs4 import BeautifulSoup

url = "https://www.xiaoyuzhoufm.com/episode/69828c85a712301410e31643"
headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

response = requests.get(url, headers=headers)
print(f"Status code: {response.status_code}")

soup = BeautifulSoup(response.text, 'html.parser')
# 找到__NEXT_DATA__脚本标签
next_data_script = soup.find('script', id='__NEXT_DATA__')

if next_data_script:
    # 提取并解析JSON数据
    next_data = json.loads(next_data_script.string)
    print("\nFound __NEXT_DATA__")
    
    # 遍历数据结构查找音频相关信息
    def find_audio_info(data, path=""):
        if isinstance(data, dict):
            for key, value in data.items():
                new_path = f"{path}.{key}" if path else key
                # 查找可能的音频URL
                if key in ['audio', 'audioUrl', 'url', 'src'] and isinstance(value, str) and ('.mp3' in value or '.m4a' in value or '.audio' in value):
                    print(f"Found audio URL at {new_path}: {value}")
                # 递归查找
                find_audio_info(value, new_path)
        elif isinstance(data, list):
            for i, item in enumerate(data):
                new_path = f"{path}[{i}]"
                find_audio_info(item, new_path)
    
    find_audio_info(next_data)
else:
    print("\n__NEXT_DATA__ not found")