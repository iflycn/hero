# 百万英雄答题器
为西瓜视频的百万英雄活动开发的 `Python` 版答题器，支持 Android 手机或电脑模拟器。

## 运行效果截图
![](https://github.com/iflycn/hero/blob/master/cmd.png)

## 如何使用（Windows 系统）
### 安装 ADB
1. 访问 [ADB Shell](http://adbshell.com/downloads) 下载 `ADB Kits`，解压到硬盘目录，例如 `D:\ADB`
2. 进入系统属性，点击环境变量，在弹出窗口的系统变量中找到 Path 并双击，在弹出窗口的变量值最后加上 `;D:\adb`
### 设置你的手机
3. 开启开发者选项，打开 USB 调试，小米手机一并打开 USB 调试（安全设置）
4. 使用数据线连接手机，等待系统自动安装驱动完成
### 下载程序
5. 下载百万英雄答题器程序压缩包，解压到硬盘目录，例如 `D:\MillionHeroes`
6. 修改文件 `mian.py` 中的 `APP_ID`、`API_KEY`、`SECRET_KEY` 为你自己的，申请地址：[百度 AI 开放平台](http://ai.baidu.com/tech/ocr/general)
### 安装 Python
7. 从 [Python 官网](https://www.python.org/downloads)下载安装 `python3.6.4`
8. 电脑运行 `CMD`，依次输入命令 `D:`、`cd millionheroes`、`pip install -r requirements.txt`，等待下载依赖包并安装完成
9. 如果下载依赖包过程中出错，重新输入命令 `pip install -r requirements.txt` 直到下载成功
### 开始使用
10. 手机进入百万英雄界面
11. 电脑运行 `CMD`，输入命令 `python main.py`，根据程序提示操作即可

## 参考项目
- [wuditken/MillionHeroes](https://github.com/wuditken/MillionHeroes)
- [smileboywtu/MillionHeroAssistant](https://github.com/smileboywtu/MillionHeroAssistant)