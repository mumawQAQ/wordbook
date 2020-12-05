import pandas as pd
from datetime import date
import math


from message import Message


class Word(object):

    def __init__(self):
        self.path = "./resource/3000_back1.csv"
        self.df = pd.read_csv(self.path, index_col=0)
        self.message = Message()

    def set_plan(self, num):
        """
        set the word amount you want to remember each day
        :param num:int
        :return:
        """
        # 第一天n=100个单词 以后每天背n/2个单词并复习前一天的单词
        # day 1 随机n个单词
        # day n 随机n/2个单词 并复习n-n/2个单词

        each_day = num
        day_n = math.floor(num/2)
        review = each_day-day_n

        self.info_dict = {
            "each_day": each_day,
            "review": review,
            "day_n": day_n,
            "start_day": date.today().strftime("%d/%m/%Y")
        }
        with open("./resource/plan", "w") as file:
            file.write("each_day:" + str(each_day) + "\n")
            file.write("review:" + str(review) + "\n")
            file.write("day_n:" + str(day_n) + "\n")
            file.write("start_day:" + date.today().strftime("%d/%m/%Y") + "\n")

        self.message.tb_sp("Your plan is "+ str(self.info_dict['each_day']) +" each day")

    def change_plan(self,num):

        with open("./resource/plan", "r") as file:
            start_day = file.readlines()[3].replace("\n","").split(":")[1]

        each_day = num
        day_n = math.floor(num/2)
        review = each_day-day_n

        self.info_dict = {
            "each_day": each_day,
            "review": review,
            "day_n": day_n,
            "start_day": start_day
        }
        with open("./resource/plan", "w") as file:
            file.write("each_day:" + str(each_day) + "\n")
            file.write("review:" + str(review) + "\n")
            file.write("day_n:" + str(day_n) + "\n")
            file.write("start_day:" + start_day + "\n")

        self.message.tb_sp("Your plan is "+ str(self.info_dict['each_day']) +" each day")

    def read_plan(self):
        """
        :return: dict
        """

        info_dict = {}
        with open("./resource/plan", "r") as file:
            for line in file:
                info_list = line.split(":")
                info_list[1] = info_list[1].replace("\n", "")
                info_dict[info_list[0]] = info_list[1]

        self.info_dict = info_dict

        self.message.tb_sp("Your plan is "+ str(self.info_dict['each_day']) +" each day")


    def get_words(self):
        """
        :param info_dict: dict
        :return: list
        """
        word_list = []

        # 获取每天需要背诵的词汇 第一天为n个新单词 后面每天为n/2个新单词+n/2个复习单词

        # 获取今天是不是第一天
        today = date.today().strftime("%d/%m/%Y")
        start_day = self.info_dict["start_day"]

        if today == start_day:
            # 如果是第一天则 获取n个新单词
            df = self.df[self.df['last_attempt_date'].astype(str) == '0']
            sample = df.sample(int(self.info_dict["each_day"]))
            # 给每个单词添加尝试的时间
            for i in sample.index:
                self.df.loc[i,"last_attempt_date"] = today
                word_list.append({'index':i,'word':self.df.loc[i,'word'],'mean':self.df.loc[i,'mean']})

            self.df.to_csv(self.path)
        else:
            # 如果不是第一天则 获取n/2个新单词和n/2个复习单词
            # 查找尝试时间为0的单词
            df = self.df[self.df['last_attempt_date'].astype(str) == '0']
            # 获取n/2个单词 [edge case所有单词都被背过了一遍]
            # 检查剩余单词数量 如果剩余单词数量小于计划新单词 更新复习计划
            if len(df) < int(self.info_dict['day_n']):
                self.info_dict['day_n'] = len(df)
                self.info_dict['review'] = int(self.info_dict['each_day']) - int(self.info_dict['day_n'])
            sample = df.sample(int(self.info_dict['day_n']))
            # 给单词添加尝试时间
            for i in sample.index:
                self.df.loc[i, "last_attempt_date"] = today
                word_list.append({'index':i,'word':self.df.loc[i,'word'],'mean':self.df.loc[i,'mean']})
            # 根据权重获取复习的单词
            review_sample = self.df.sample(int(self.info_dict['review']),weights="weight")
            # 给单词添加尝试时间
            for i in review_sample.index:
                # 这个应该放在背完单词以后
                self.df.loc[i,"last_attempt_date"] = today
                word_list.append({'index':i,'word':self.df.loc[i,'word'],'mean':self.df.loc[i,'mean']})
            self.df.to_csv(self.path)
        return word_list


    def set_s(self,index,s):
        self.df.loc[index, "forget_times"] = s
        self.df.to_csv(self.path)



if __name__ == '__main__':
    # df = pd.read_csv("./resource/3000_back.csv",index_col=0)
    # df.loc[2,"last_attempt_date"] = '04/12/2020'
    # df.to_csv("./resource/3000_test1.csv")
    word = Word()
    word.change_plan(100)
    # try:
    #     info_dict = word.read_plan()
    # except:
    #     word.set_plan(100)
    #
    # word_list = word.get_words()
    # print(word_list,len(word_list))
