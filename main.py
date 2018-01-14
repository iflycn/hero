import urllib.request
import sys
import base64
import json
import os
import time
import string
import re
from PIL import Image
from shutil import copyfile
from datetime import datetime
from aip import AipOcr
from ai import AI

# 你的百度 OCR
APP_ID = "10675166"
API_KEY = "66kRY7ZHxNY6z60Ot0cUKfD1"
SECRET_KEY = "ioQpGWnYABpDbBQ8edTkwnaMhG90PH8M"

# 处理设备截图
def adb_get_screen():
    # 获取设备截图
    os.system("adb shell /system/bin/screencap -p /sdcard/screenshot.png")
    os.system("adb pull /sdcard/screenshot.png ./screenshots/screenshot.png")
    # copyfile(os.path.join("./screenshots/", "screenshot.png"), os.path.join("./screenshots/", datetime.now().strftime("%Y%m%d%H%M%S.png")))
    # 裁剪截图
    img = Image.open(r"./screenshots/screenshot.png")
    region = img.crop((70, 230, img.size[0] - 70, 1285))  # 截图裁剪坐标
    region.save(r"./screenshots/screenshot_crop.png")

# 获取 OCR 数据
def get_crop_data(screenshot_crop):
    with open(screenshot_crop, "rb") as fp:
        image_data = fp.read()
        return image_data
    return ""

def main():
    time_start = time.time()
    # 处理设备截图
    adb_get_screen()
    # 获取 OCR 结果
    OCR = AipOcr(APP_ID, API_KEY, SECRET_KEY)
    respon = OCR.basicGeneral(get_crop_data(r"./screenshots/screenshot_crop.png"))
    words_result = respon["words_result"]
    # 处理获取结果
    question = ""
    answer = ["", "", ""]
    i = 0
    for words in words_result:
        i += 1
        if(i < len(words_result) - 2):
            question += words["words"]
        else:
            answer[len(words_result) - i] = words["words"]
    # 开始统计搜索
    AI(question, answer).search()
    # 统计程序用时
    time_end = time.time()
    print("use {0} seconds".format(round(time_end - time_start, 2)))

print("\n" + "-" * 28 + " 百万英雄答题器 " + "-" * 28)
print("\n答案抓取自问答网站，无法保证绝对正确，如果给出的回答和你所知不符，请相信自己！")
print("\n屏幕出现完整题目后按回车键，如果运行中出错，按 CTRL+C 退出并重新运行。")
while True:
    enter = input("\n回车键作答，q 键退出。等待输入：")
    if (enter == chr(113)) or (enter == chr(81)):
        break
    else:
        main()
