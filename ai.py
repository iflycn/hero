import _thread
import ctypes
import re
import sys
import urllib.request
import urllib.parse

class AI:

    def __init__(self, data):
        self.question_type = True
        self.question = data[0]
        self.answer = data[1][::-1]
        self.result = -1
        if len(data) > 2:
            try:
                self.result = self.answer.index(data[2])
            except:
                pass
        self.stat = []
        self.count = 0

    def print_color_text(self, color, msg):
        ctypes.windll.kernel32.SetConsoleTextAttribute(ctypes.windll.kernel32.GetStdHandle(-11), color)
        print(msg)
        ctypes.windll.kernel32.SetConsoleTextAttribute(ctypes.windll.kernel32.GetStdHandle(-11), 0x07)

    def ai_search(self, app):
        self.question = self.format_question_pre(self.question, app) # 预格式化题目
        print("-" * 72)
        print("{}\n".format(self.question)) # 输出题目
        self.question = self.format_question(self.question, app) # 格式化题目
        for i in range(len(self.answer)): # 格式化答案并生成权重列表
            self.answer[i] = self.format_answer_pre(self.answer[i], app)
            self.stat.append(0)
        if self.result != -1: # 输出建议回答
            for i in range(len(self.answer)):
                if i == self.result:
                    print("{} (√)".format(self.answer[i]))
                else:
                    print("{} (×)".format(self.answer[i]))
            print("-" * 72)
            self.print_color_text(0x0b, "建议回答：{}".format(self.answer[self.result]))
            print("-" * 72 + "\n")
        for http in ("https://iask.sina.com.cn/search?searchWord=", "http://wenwen.sogou.com/s/?w=", "https://wenda.so.com/search/?q=", "https://zhidao.baidu.com/search?word="):
            _thread.start_new_thread(self.get_count_zhidao, (http + urllib.parse.quote(self.question),))
        while True:
            if self.count == 4:
                break
        if sum(self.stat) == 0: # 计算总数如果为零则发起新搜索
            print("没有找到答案，启用百度搜索...\n")
            http = "https://www.baidu.com/s?wd="
            self.count = 0
            for i in range(len(self.answer)):
                _thread.start_new_thread(self.get_count_baidu, (i, http + urllib.parse.quote(self.answer[i]),))
            while True:
                if self.count == len(self.answer):
                    break
            http += urllib.parse.quote(self.question)
            for i in range(len(self.answer)):
                _thread.start_new_thread(self.get_count_baidu, (i, http + urllib.parse.quote("+{}".format(self.answer[i])),))
            while True:
                if self.count == len(self.answer) * 2:
                    break
        self.print_answer()

    def get_count_zhidao(self, url):
        headers = ("User-Agent", "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11")
        opener = urllib.request.build_opener()
        opener.addheaders = [headers]
        try:
            data = opener.open(url).read()
        except:
            print("error: connection reset\n")
            data = str("error")
        else:
            if "zhidao.baidu.com" in url:
                try:
                    data = str(data.decode("gbk").encode("utf-8"), "utf-8")
                except:
                    print("error: unicode decode error\n")
                    data = str("error")
            else:
                data = str(data, "utf-8")
        for i in range(len(self.answer)):
            self.stat[i] += data.count(self.answer[i])
        self.count += 1

    def get_count_baidu(self, sub, url):
        headers = ("User-Agent", "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11")
        opener = urllib.request.build_opener()
        opener.addheaders = [headers]
        try:
            data = str(opener.open(url).read(), "utf-8")
        except:
            print("error: connection reset\n")
        else:
            count = int(data.split("百度为您找到相关结果约")[1].split("个")[0].replace(",", ""))
            if self.stat[sub] == 0:
                self.stat[sub] = count + 0.001
            else:
                # print("{}: {} / {} = {}".format(sub, count, self.stat[sub], count / self.stat[sub]))
                self.stat[sub] = count / self.stat[sub]
        self.count += 1

    def format_question_pre(self, question, app):
        # 去除多余字符
        question = re.sub(r"本题奖金.*万", "", question)
        # 去除多余编号
        if app == 10:
            if str.isdigit(question[-1]):
                question = question[:-1]
            if str.isdigit(question[-1]):
                question = question[:-1]
        return question

    def format_question(self, question, app):
        # 去除题目编号
        # if app in (1, 3, 4, 8, 9):
        #     if str.isdigit(question[1:2]):
        #         question = question[3:].strip()
        #     else:
        #         question = question[2:].strip()
        question = re.sub(r"[[0-9]]?[:\.]?", "", question).strip()
        # print(question)
        # 去除特殊字符
        for v in ["“", "”", "\"", "？", "?", "以下", "下列"]:
            question = question.replace(v, "")
        # 排除否定式提问
        for v in (["不是", "是"], ["不会", "会"], ["不能", "可以"], ["不同", "相同"], ["不用", "必须"], ["不对", "正确"], ["不宜", "适宜"], ["不可能", "可能"], ["不需要", "需要"], ["不包括", "包括"], ["不属于", "属于"], ["不正确", "正确"], ["不准确", "准确"], ["不相符", "相符"], ["不提供", "提供"], ["不位于", "位于"], ["没有", "有"], ["未在", "在"], ["未曾", "曾经"], ["未获得", "获得"], ["是错", "是对"], ["无关", "有关"], ["并非", ""]):
            if v[0] in question:
                question = question.replace(v[0], v[1])
                self.question_type = False
        return question

    def format_answer_pre(self, answer, app):
        # 去除多余字符
        answer = answer.replace("《", "").replace("》", "")
        # 去除多余序号
        # if app in (5, 6, 8):
        #     answer = re.sub(r"[ABC]?[:\.]?", "", answer)
        answer = re.sub(r"[ABC]?[:\.]?", "", answer).strip()
        # print(answer)
        return answer

    def print_answer(self):
        for i in range(len(self.answer)): # 输出每个答案的权重
            if sum(self.stat) == 0: # 计算总数避免除数依然为零
                print("{} (0)".format(self.answer[i]))
            else:
                if self.answer[i] in self.question: # 如果问题中包含答案则调整权重
                    self.stat[i] = int(self.stat[i] / 3)
                print("{} ({}%)".format(self.answer[i], int(self.stat[i] / sum(self.stat) * 100)))
        print("-" * 72)
        if sum(self.stat) == 0: # 输出建议回答
            print("没有找到答案，蒙一个吧")
        else:
            if self.question_type:
                self.print_color_text(0x0b, "肯定回答：{}".format(self.answer[self.stat.index(max(self.stat))]))
            else:
                self.print_color_text(0x0b, "否定回答：{}".format(self.answer[self.stat.index(min(self.stat))]))
        print("-" * 72)

if __name__ == "__main__":
    pass
