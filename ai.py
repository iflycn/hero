import urllib.request
import urllib.parse
import time
import _thread

class AI:

    def __init__(self, question, answer):
        self.question = question
        self.question_type = True
        self.answer = answer
        self.stat = [0, 0, 0]
        self.count = 0

    def getcount(self, url):
        headers = ("User-Agent", "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11")
        opener = urllib.request.build_opener()
        opener.addheaders = [headers]
        date = opener.open(url).read()
        if "zhidao.baidu.com" in url:
            get = str(date.decode("gbk").encode("utf-8"), "utf-8")
        else:
            get = str(date, "utf-8")
        for i in [0, 1, 2]:
            self.stat[i] += get.count(self.answer[i].replace("《", "").replace("》", ""))
        self.count += 1

    def formatquestion(self, question):
        # 去除题目编号
        if str.isdigit(question[1:2]):
            question = question[3:]
        else:
            question = question[2:]
        # 去除特殊字符
        for v in ["“", "”", "\"", "？", "?"]:
            question = question.replace(v, "")
        # 排除否定式提问
        for v in ["不是", "不会", "不用", "不宜", "不包括", "不属于", "不正确", "没有", "是错"]:
            if v in question:
                question = question.replace(v, "")
                self.question_type = False
        return question

    def search(self):  # 搜索引擎
        print("-" * 72)
        print(self.question + "\n") # 输出题目
        self.question = self.formatquestion(self.question)
        _thread.start_new_thread(self.getcount, ("https://zhidao.baidu.com/search?word=" + urllib.parse.quote(self.question, encoding="gbk"),))
        _thread.start_new_thread(self.getcount, ("http://wenwen.sogou.com/s/?w=" + urllib.parse.quote(self.question),))
        _thread.start_new_thread(self.getcount, ("https://iask.sina.com.cn/search?searchWord=" + urllib.parse.quote(self.question),))
        _thread.start_new_thread(self.getcount, ("https://wenda.so.com/search/?q=" + urllib.parse.quote(self.question),))
        while 1:
            if(self.count == 4):
                break
        for i in [2, 1, 0]:
            if self.answer[i] in self.question: # 如果问题中包含答案则调整权重
                self.stat[i] = int(self.stat[i] / 3)
            if self.stat[0] + self.stat[1] + self.stat[2] == 0:
                print(str(self.answer[i]) + " (0)")
            else:
                print(str(self.answer[i]) +" (" + str(int(round(self.stat[i] / (self.stat[0] + self.stat[1] + self.stat[2]) * 100))) + "%)")  # 输出每个答案的权重
        print("-" * 72)
        if self.stat[0] + self.stat[1] + self.stat[2] == 0: # 输出建议回答
            print("没有找到答案，蒙一个吧")
        else:
            if self.question_type:
                print("肯定回答：" + str(self.answer[self.stat.index(max(self.stat))]))
            else:
                print("否定回答：" + str(self.answer[self.stat.index(min(self.stat))]))
        print("-" * 72)
