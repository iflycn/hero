import configparser
import ctypes
import os
import sys
import time
from aip import AipOcr
from datetime import datetime
from PIL import Image
from shutil import copyfile
from ai import AI

#获取 config 配置文件
def get_config_data(section, key):
    try:
        config = configparser.ConfigParser()
        config.read(r"./config.ini")
        return config.get(section, key)
    except:
        print("error: read config.ini error")
        return ""

# 处理设备截图
def adb_get_screen(enter, app):
    # 获取设备截图
    os.system("adb shell /system/bin/screencap -p /sdcard/screenshot.png")
    os.system("adb pull /sdcard/screenshot.png ./screenshots/screenshot.png")
    if enter == "+":
        copyfile(os.path.join("./screenshots/", "screenshot.png"), os.path.join("./screenshots/", datetime.now().strftime("%Y%m%d%H%M%S.png")))
    # 裁剪截图
    try:
        img = Image.open(r"./screenshots/screenshot.png").convert("L")
    except:
        print("error: file not found")
        time.sleep(3)
        sys.exit()
    # 截图裁剪坐标
    if app == 26:
        try:
            X1 = int(get_config_data("COORDINATE", "X1"))
            Y1 = int(get_config_data("COORDINATE", "Y1"))
            X2 = int(get_config_data("COORDINATE", "X2"))
            Y2 = int(get_config_data("COORDINATE", "Y2"))
        except:
            print("error: COORDINATE must be INT")
            time.sleep(3)
            sys.exit()
        region = img.crop((X1, Y1, X2, Y2))
    else:
        coordinate = ((70, 240, 70, 1285), (45, 285, 45, 1150), (70, 310, 70, 1160), (60, 300, 60, 1160), (90, 320, 90, 1160), (40, 375, 40, 1320), (70, 260, 70, 1100), (100, 540, 100, 1280), (80, 1100, 80, 1740), (90, 440, 90, 1220), (60, 310, 60, 1180), (80, 420, 80, 1110), (20, 330, 20, 1380), (0, 0, 0, 1920), (0, 0, 0, 1920), (0, 0, 0, 1920), (0, 0, 0, 1920), (0, 0, 0, 1920), (0, 0, 0, 1920), (0, 0, 0, 1920), (0, 0, 0, 1920), (0, 0, 0, 1920), (0, 0, 0, 1920), (138, 500, 138, 1700))
        coordinate = coordinate[app - 1]
        coefficient = img.size[0] / 1080
        region = img.crop((coordinate[0] * coefficient, coordinate[1] * coefficient, img.size[0] - coordinate[2] * coefficient, coordinate[3] * coefficient))
    region.save(r"./screenshots/screenshot_crop.png")

# 获取设备截图
def get_crop_data(img):
    with open(img, "rb") as fp:
        return fp.read()
    return ""

# 获取 OCR 数据
def get_words_result():
    APP_ID = get_config_data("ORC", "APP_ID")
    API_KEY = get_config_data("ORC", "API_KEY")
    SECRET_KEY = get_config_data("ORC", "SECRET_KEY")
    OCR = AipOcr(APP_ID, API_KEY, SECRET_KEY)
    try:
        respon = OCR.basicGeneral(get_crop_data(r"./screenshots/screenshot_crop.png"))
        # print(respon["words_result"])
        return respon["words_result"]
    except:
        print("error: baidu ocr error")
        time.sleep(3)
        sys.exit()

# 处理 OCR 数据
def format_words_result(data, app):
    question = ""
    if app == 24 or (app == 26 and get_config_data("COORDINATE", "ANSWER_SIZE") == "4"):
        answer = ["", "", "", ""]
    else:
        answer = ["", "", ""]
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
    ctypes.windll.kernel32.SetConsoleTextAttribute(ctypes.windll.kernel32.GetStdHandle(-11), 0x07)
    print("-" * 72)
    print("{}百万英雄答题助手".format(" " * 28))
    print("{}1.5.7.20180202".format(" " * 29))
    print("-" * 72)
    print("\n答案抓取自问答网站，无法保证绝对正确，如果回答和你所知不符，请相信自己！\n")
    print("A. 百万英雄\tB. 芝士超人\tC. 冲顶大会\nD. 百万赢家\tE. 黄金十秒\tF. 全民答题\nG. 非答不可\tH. 蘑菇大富翁\tI. 百万黄金屋\nJ. 极速挑战\tK. 小米有乐\tL. 百万文豪\nM. 疯狂夺金\tX. 头脑王者\tZ. 自定义\n")
    while True:
        app = input("输入序号：")
        if app.lower() in ("a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "x", "z"):
            app = ord(app.lower()) - 96
            break
    print("\n手机出现完整题目后按回车键，如果运行中出错，按 CTRL+C 退出并重新运行。")
    while True:
        enter = input("\n回车键作答，q 键退出。等待输入：")
        if enter.lower() == "q":
            break
        else:
            main(enter, int(app))
