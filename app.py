from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import os
import sys

# 添加当前目录到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# 确保templates目录存在
if not os.path.exists('templates'):
    os.makedirs('templates')

# 将index.html复制到templates目录
if os.path.exists('index.html'):
    import shutil
    shutil.copy('index.html', 'templates/')

from podcast_downloader import PodcastDownloader

app = Flask(__name__)
CORS(app)  # 启用CORS，允许前端跨域请求

downloader = PodcastDownloader()

@app.route('/')
def index():
    """提供前端页面"""
    return render_template('index.html')

@app.route('/extract', methods=['POST'])
def extract_audio():
    """提取音频URL"""
    try:
        data = request.json
        podcast_url = data.get('url')
        
        if not podcast_url:
            return jsonify({'error': '请提供播客链接'}), 400
        
        # 提取音频URL
        audio_url = downloader.extract_audio_url(podcast_url)
        
        # 从URL中提取文件名
        from urllib.parse import urlparse
        parsed_url = urlparse(audio_url)
        file_name = os.path.basename(parsed_url.path)
        
        return jsonify({
            'success': True,
            'audio_url': audio_url,
            'file_name': file_name
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    # 确保templates目录存在
    if not os.path.exists('templates'):
        os.makedirs('templates')
    
    # 将index.html复制到templates目录
    if os.path.exists('index.html'):
        import shutil
        shutil.copy('index.html', 'templates/')
    
    app.run(debug=True, host='0.0.0.0', port=5001)