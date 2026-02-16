import requests
import json
from bs4 import BeautifulSoup
import os
import argparse
from urllib.parse import urlparse
import sys

class PodcastDownloader:
    def __init__(self):
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        }
    
    def print_success(self, message):
        """打印成功信息"""
        print(f"[✓] {message}")
    
    def print_info(self, message):
        """打印信息"""
        print(f"[i] {message}")
    
    def print_warning(self, message):
        """打印警告信息"""
        print(f"[!] {message}")
    
    def print_error(self, message):
        """打印错误信息"""
        print(f"[✗] {message}")
    
    def extract_audio_url(self, url):
        """从播客链接中提取音频文件URL"""
        try:
            self.print_info(f"正在请求页面: {url}")
            response = requests.get(url, headers=self.headers, timeout=30)
            response.raise_for_status()
            
            self.print_info("解析页面内容...")
            soup = BeautifulSoup(response.text, 'html.parser')
            next_data_script = soup.find('script', id='__NEXT_DATA__')
            
            if not next_data_script:
                raise Exception("未找到音频信息")
            
            self.print_info("提取音频信息...")
            next_data = json.loads(next_data_script.string)
            
            # 查找音频URL
            episode_data = next_data.get('props', {}).get('pageProps', {}).get('episode', {})
            
            # 尝试从不同路径获取音频URL
            audio_url = None
            if episode_data.get('enclosure', {}).get('url'):
                audio_url = episode_data['enclosure']['url']
            elif episode_data.get('media', {}).get('source', {}).get('url'):
                audio_url = episode_data['media']['source']['url']
            
            if not audio_url:
                raise Exception("未找到音频文件URL")
            
            self.print_success(f"找到音频文件URL: {audio_url}")
            return audio_url
            
        except requests.RequestException as e:
            raise Exception(f"网络请求失败: {str(e)}")
        except json.JSONDecodeError as e:
            raise Exception(f"解析JSON数据失败: {str(e)}")
        except Exception as e:
            raise Exception(f"提取音频URL失败: {str(e)}")
    
    def download_audio(self, audio_url, output_dir='.', output_filename=None):
        """下载音频文件"""
        try:
            # 确保输出目录存在
            os.makedirs(output_dir, exist_ok=True)
            
            # 如果没有指定文件名，从URL中提取
            if not output_filename:
                parsed_url = urlparse(audio_url)
                output_filename = os.path.basename(parsed_url.path)
            
            output_path = os.path.join(output_dir, output_filename)
            
            self.print_info(f"正在下载音频文件: {output_filename}")
            self.print_info(f"保存路径: {output_path}")
            
            # 下载文件
            response = requests.get(audio_url, headers=self.headers, stream=True, timeout=60)
            response.raise_for_status()
            
            total_size = int(response.headers.get('content-length', 0))
            downloaded_size = 0
            
            with open(output_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
                        downloaded_size += len(chunk)
                        
                        # 显示下载进度
                        if total_size > 0:
                            progress = (downloaded_size / total_size) * 100
                            # 使用进度条
                            bar_length = 50
                            filled_length = int(bar_length * downloaded_size / total_size)
                            bar = '=' * filled_length + '-' * (bar_length - filled_length)
                            sys.stdout.write(f'\r[{bar}] {progress:.2f}%')
                            sys.stdout.flush()
            
            print()
            self.print_success(f"下载完成! 音频文件已保存到: {output_path}")
            return output_path
            
        except requests.RequestException as e:
            raise Exception(f"下载失败: {str(e)}")
        except Exception as e:
            raise Exception(f"下载音频失败: {str(e)}")
    
    def download_from_url(self, podcast_url, output_dir='.', output_filename=None):
        """从播客链接下载音频"""
        try:
            self.print_info(f"处理播客链接: {podcast_url}")
            
            # 提取音频URL
            audio_url = self.extract_audio_url(podcast_url)
            
            # 下载音频
            output_path = self.download_audio(audio_url, output_dir, output_filename)
            
            return output_path
            
        except Exception as e:
            self.print_error(f"错误: {str(e)}")
            return None

def main():
    parser = argparse.ArgumentParser(description='播客音频提取工具')
    parser.add_argument('url', help='播客链接')
    parser.add_argument('-o', '--output', help='输出文件名', default=None)
    parser.add_argument('-d', '--dir', help='输出目录', default='.')
    
    args = parser.parse_args()
    
    # 打印欢迎信息
    print("播客音频提取工具")
    print("===================")
    
    downloader = PodcastDownloader()
    result = downloader.download_from_url(args.url, args.dir, args.output)
    
    if result:
        print("\n任务完成!")
    else:
        print("\n任务失败!")
        sys.exit(1)

if __name__ == '__main__':
    main()