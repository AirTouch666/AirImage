<p align="center">
  <img src="https://img.airtouch.top/350224c08858f7fdc52cbeae09ab85c9.png" alt="Static Badge" width="25%;" />
</p>

<p align="center">
  <img src="https://img.shields.io/badge/language-Python-light" />
  <img src="https://img.shields.io/badge/release-v1.0.0-light" />
  <img src="https://img.shields.io/badge/licence-MIT-orange" />
  <img src="https://img.shields.io/badge/platform-linux%20%7C%20macos%20%7C%20windows-light" />
  <a href="https://github.com/AirTouch666/AirImage/actions/workflows/docker-build-push.yml">
    <img src="https://github.com/AirTouch666/AirImage/actions/workflows/docker-build-push.yml/badge.svg" alt="Docker Image CI" />
  </a>
  <a href="https://github.com/AirTouch666/AirImage/actions/workflows/build-release.yml">
    <img src="https://github.com/AirTouch666/AirImage/actions/workflows/build-release.yml/badge.svg" alt="Build and Release CI" />
  </a>
</p>


## ⚡️关于

AirImage 是一个简单的图床，使用 Python 开发，基于 Flask 框架。

## ✨功能

- 支持拖放上传和多文件选择
- 自动将上传的图片转换为 WebP 格式以节省空间
- 为每个上传的文件生成唯一的文件名，防止覆盖
- 显示所有已上传图片的缩略图和链接
- 响应式设计，适配各种设备
- 复制链接功能
- 支持自定义配置

## ⌨️技术

- 后端: Python Flask
- 前端: HTML，CSS，JavaScript
- 图像处理: Pillow

## 💽安装稳定版
+ [GitHub](https://github.com/AirTouch666/AirImage/releases)上提供了已经编译好的程序，当然你也可以自己克隆代码编译打包。

+ 通过 docker 安装
   ```
   docker run -d -p {端口}:8080 -v {本地存放图片的位置}:/app/uploads airtouch/airimage
   ```

## 💽从源码安装

1. 克隆仓库:
   ```
   git clone https://github.com/AirTouch666/AirImage.git
   cd AirImage
   ```

2. 安装依赖:
   ```
   pip install -r requirements.txt
   ```

3. 运行应用:
   ```
   python run.py
   ```

4. 在浏览器中打开 `http://{IP}:{POST}`

  
## 🔧配置
应用程序使用 `config.json` 文件进行配置。首次运行时会自动创建此文件，包含以下默认设置：
```json
{
    "secret_key": "9b6ecabd5c55f6f85ca6f0a87f67c89e",
    "port": 8080,//端口
    "background": "#f4f4f4",//背景
    "site_name": "AirImage",//名称
    "site_icon": "",//图标
    "max_file_size": 10,//最大文件大小(MB)
    "allowed_extensions": ["png", "jpg", "jpeg", "gif", "webp"]//允许的文件类型
}
```

您可以根据需要修改以下设置：
- `port`: 应用程序运行的端口号（默认为 8080）
- `background`: 应用程序的背景颜色或图片（默认为 #f4f4f4）
- `site_name`: 应用程序的名称（默认为 AirImage）
- `site_icon`: 应用程序的图标（默认为空）
- `max_file_size`: 上传文件的最大大小（默认为 10MB）
- `allowed_extensions`: 允许上传的文件类型（默认为 ["png", "jpg", "jpeg", "gif", "webp"]）

## 🖥应用界面
![应用界面](https://img.airtouch.top/1a27d5c1d8d2288a887dc84398c8a4cd.webp)
![应用界面](https://img.airtouch.top/0ccd3a488a0c1a1ee4e32314ba8b0c9a.webp)

## 🤝贡献

欢迎提交 Pull Requests 来改进这个项目。对于重大更改，请先开 issue 讨论您想要改变的内容。

## 📜许可证

本项目基于 MIT 许可证开源，详情见 [LICENSE](./LICENSE) 。