# 播客音频提取工具 - 部署指南

本指南将帮助您将播客音频提取工具部署到Vercel平台，使其可以在任何设备上访问。

## 前提条件

- 一个Vercel账号（[注册地址](https://vercel.com/signup)）
- 一个GitHub账号（用于代码托管）

## 部署步骤

### 1. 将项目上传到GitHub

1. 在GitHub上创建一个新的仓库
2. 将本地项目文件上传到GitHub仓库

```bash
# 初始化git仓库
git init

# 添加文件
git add .

# 提交文件
git commit -m "Initial commit"

# 添加远程仓库
git remote add origin https://github.com/your-username/podcast-downloader.git

# 推送到GitHub
git push -u origin main
```

### 2. 部署到Vercel

1. 登录Vercel控制台
2. 点击"New Project"
3. 选择您刚刚创建的GitHub仓库
4. 配置部署选项：
   - Framework Preset: 选择 "Other"
   - Build Command: 留空
   - Output Directory: 留空
   - Environment Variables: 不需要特殊配置
5. 点击"Deploy"按钮开始部署

### 3. 验证部署

部署完成后，Vercel会提供一个唯一的URL（例如：`https://podcast-downloader.vercel.app`）。

您可以通过以下步骤验证部署是否成功：

1. 打开提供的URL
2. 输入播客链接测试音频提取功能
3. 确认系统能够正常提取和提供下载链接

## 项目结构说明

```
├── app.py              # Flask后端应用
├── podcast_downloader.py  # 音频提取核心功能
├── index.html          # 前端页面
├── templates/          # Flask模板目录
│   └── index.html      # 复制的前端页面
├── requirements.txt    # Python依赖文件
├── vercel.json         # Vercel配置文件
└── DEPLOYMENT.md       # 部署说明文档
```

## 注意事项

1. **依赖管理**：Vercel会自动读取requirements.txt文件并安装所需依赖
2. **环境变量**：如果需要添加环境变量，可以在Vercel项目设置中配置
3. **域名配置**：您可以在Vercel中添加自定义域名
4. **部署限制**：Vercel的免费计划有一定的使用限制，如果流量较大，可能需要升级到付费计划

## 故障排除

### 常见问题

1. **部署失败**：检查requirements.txt文件是否正确，确保所有依赖版本兼容
2. **音频提取失败**：检查网络连接，确保Vercel服务器可以访问小宇宙网站
3. **下载速度慢**：这可能是由于Vercel服务器位置或网络条件导致的

### 解决方案

- 如果遇到依赖问题，可以尝试调整requirements.txt中的版本号
- 如果遇到网络问题，可以考虑使用Vercel的不同区域部署
- 如果遇到性能问题，可以考虑升级Vercel计划或优化代码

## 本地开发

如果您想在本地进行开发和测试，可以使用以下命令启动服务器：

```bash
# 安装依赖
pip3 install -r requirements.txt

# 启动服务器
python3 app.py
```

然后在浏览器中访问 `http://localhost:5001`

## 联系方式

如果您在部署过程中遇到任何问题，请参考Vercel官方文档或联系技术支持。