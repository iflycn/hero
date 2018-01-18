import os
import time
import sys
from PIL import Image
from shutil import copyfile
from datetime import datetime
from aip import AipOcr
from config import APP_ID
from config import API_KEY
from config import SECRET_KEY
from ai import AI

# 处理设备截图
def adb_get_screen(enter, app):
    # 获取设备截图
    os.system("adb shell /system/bin/screencap -p /sdcard/screenshot.png")
    os.system("adb pull /sdcard/screenshot.png ./screenshots/screenshot.png")
    if enter == "+":
        copyfile(os.path.join("./screenshots/", "screenshot.png"), os.path.join("./screenshots/", datetime.now().strftime("%Y%m%d%H%M%S.png")))
    # 裁剪截图
    try:
        img = Image.open(r"./screenshots/screenshot.png")
    except:
        print("error: file not found")
        sys.exit()
    # 截图裁剪坐标
    coordinate = ((70, 240, 70, 1285), (45, 285, 45, 1200), (70, 310, 70, 1160), (), (), (), (), (), (138, 500, 138, 1700))
    coordinate = coordinate[app - 1]
    region = img.crop((coordinate[0], coordinate[1], img.size[0] - coordinate[2], coordinate[3]))
    region.save(r"./screenshots/screenshot_crop.png")

# 获取设备截图
def get_crop_data(img):
    with open(img, "rb") as fp:
        return fp.read()
    return ""

# 获取 OCR 数据
def get_words_result():
    OCR = AipOcr(APP_ID, API_KEY, SECRET_KEY)
    try:
        respon = OCR.basicGeneral(get_crop_data(r"./screenshots/screenshot_crop.png"))
        return respon["words_result"]
    except:
        print("error: baidu ocr error")
        sys.exit()

# 处理 OCR 数据
def format_words_result(data, app):
    question = ""
    if app in (1, 2, 3):
        answer = ["", "", ""]
    else:
        answer = ["", "", "", ""]
    i = 0
    for words in data:
        i += 1
        if i <= len(data) - len(answer):
            question += words["words"]
        else:
            answer[len(data) - i] = words["words"]
    return [question, answer]

def main(enter, app):
    time_start = time.time()
    # 处理设备截图
    adb_get_screen(enter, app)
    # 开始统计搜索
    AI(format_words_result(get_words_result(), app)).ai_search(app)
    # 统计程序用时
    time_end = time.time()
    print("use {0} seconds".format(round(time_end - time_start, 2)))

if __name__ == "__main__":
    print("\n" + "-" * 27 + " 百万英雄答题助手 " + "-" * 27)
    print("\n答案抓取自问答网站，无法保证绝对正确，如果回答和你所知不符，请相信自己！\n")
    app_list = ("1", "2", "3", "9")
    while True:
        app = input("输入数字（1.百万英雄、2.芝士超人、3.冲顶大会、9.头脑王者）：")
        if app in app_list:
            break
    print("\n手机出现完整题目后按回车键，如果运行中出错，按 CTRL+C 退出并重新运行。")
    while True:
        enter = input("\n回车键作答，q 键退出。等待输入：")
        if enter.lower() == "q":
            break
        else:
            main(enter, int(app))
