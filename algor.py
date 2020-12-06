import pandas as pd
from datetime import *
import math



# 在选每天复习的单词之前 更新一次概率
class Algor(object):

    def __init__(self):
        self.path = "./resource/3000_back1.csv"
        self.df = pd.read_csv(self.path, index_col=0)

    def clean_data(self):
        try:
            filter1 = (self.df['last_attempt_date'].astype(str) != '0') & (self.df['forget_times'].astype(int) == 0)
            df = self.df[filter1]
            for index in df.index:
                self.df.loc[index, 'last_attempt_date'] = 0
            # 输出csv表
            self.df.to_csv(self.path)
        except:
            pass

    def get_t(self):
        # 获取今天的日期
        today = date.today().strftime("%d/%m/%Y")
        today = datetime.strptime(today, '%d/%m/%Y')
        # 获取过了几天
        df = self.df[self.df['last_attempt_date'].astype(str) != '0']
        for ele, index in zip(df['last_attempt_date'], df.index):
            t = datetime.strptime(ele, '%d/%m/%Y')
            # 设置为csv的t值
            self.df.loc[index, "t"] = (today - t).days
        # 输出csv表
        self.df.to_csv(self.path)

    def get_s(self):
        # 获取背诵次数
        df = self.df[self.df['forget_times'].astype(int) != 0]
        # 计算s值
        for ele, index in zip(df['forget_times'], df.index):
            s = math.log(1 / ele)
            self.df.loc[index, "s"] = s
        # 输出csv表
        self.df.to_csv(self.path)

    def get_probability(self):
        df = self.df[self.df['forget_times'].astype(int) != 0]
        for index in df.index:
            # 获取t值
            t = self.df.loc[index, "t"]
            # 获取s值
            s = self.df.loc[index, "s"]
            # 计算概率
            probability = math.pow(math.e, 1 / (t * s)) * 100
            self.df.loc[index, "probability"] = probability
        # 输出csv表
        self.df.to_csv(self.path)

    def get_weight(self):
        sum = self.df['probability'].sum()
        self.df['weight'] = self.df['probability'] / sum
        self.df.to_csv(self.path)

    def run(self):
        self.clean_data()
        self.get_t()
        self.get_s()
        self.get_probability()
        self.get_weight()


if __name__ == '__main__':
    algor = Algor()
    algor.clean_data()
