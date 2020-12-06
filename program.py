from __future__ import print_function, unicode_literals
from PyInquirer import style_from_dict, Token, prompt, Separator
from playsound import playsound

import sys
import os

from word import Word
from algor import Algor
from common import *
from pronounce import Pronounce

# 对象
word = Word()
common = Common()
pronounce = Pronounce()
algor = Algor()


# 初始化表格
algor.run()

# 解决编码问题
message.tb_sp("编码测试")
questions = [
        {
            'type': 'confirm',
            'name': 'encoding',
            'message': 'Can you see the Chinese character?',
        }
]
answer = prompt(questions,style=common.style)
if not answer["encoding"]:
    os.popen("chcp 936")


# 显示logo
print("""
    
    ███╗   ███╗██╗   ██╗███╗   ███╗ █████╗ 
    ████╗ ████║██║   ██║████╗ ████║██╔══██╗
    ██╔████╔██║██║   ██║██╔████╔██║███████║
    ██║╚██╔╝██║██║   ██║██║╚██╔╝██║██╔══██║
    ██║ ╚═╝ ██║╚██████╔╝██║ ╚═╝ ██║██║  ██║
    ╚═╝     ╚═╝ ╚═════╝ ╚═╝     ╚═╝╚═╝  ╚═╝
                                           
""")

# 获取计划
if os.path.exists('./resource/plan'):
    try:
        word.read_plan()
    except:
        print("\n\tfail to read your plan\n")
        sys.exit()
else:
    word = set_plan(word)


# 弹出功能菜单
# 功能1 更改plan
# 功能2 开始背诵
# 功能3 退出程序

while True:
    questions = [
        {
            'type': 'list',
            'name': 'type',
            'message': 'What do you want to do?',
            'choices': [
                'Reset plan',
                'Start to learn',
                Separator(),
                'Exit'
            ]
        }
    ]
    answer = prompt(questions, style=common.style)

    if answer['type'] == 'Exit':
        os.system("cls")
        sys.exit()
    elif answer['type'] == 'Reset plan':
        os.system("cls")
        word = change_plan(word)
    elif answer['type'] == 'Start to learn':
        os.system("cls")
        word_list = word.get_words()
        word_time_dict = {word['index']: 0 for word in word_list}
        for word_info in word_list:
            word_list = word_list.extend(word_list)
            questions = [
                {
                    'type': 'confirm',
                    'name': 'familiar_with',
                    'message': 'Do you remember the meaning of || ' + word_info['word'],
                }
            ]
            answer = prompt(questions, style=common.style)

            if not answer['familiar_with']:
                word_list.append(word_info)
            message.tb_sp(word_info['mean'])
            if word_time_dict[word_info['index']] <5:
                word_time_dict[word_info['index']] = word_time_dict[word_info['index']] + 1

            while True:
                next_word = [
                    {
                        'type': 'list',
                        'name': 'type',
                        'message': 'What do you want to do?',
                        'choices': [
                            'next word',
                            'pronunciation',
                        ]
                    }
                ]
                next_word = prompt(next_word,style=common.style)
                if next_word['type'] == 'pronunciation':
                    try:
                        playsound("./audio/"+word_info['word']+".mp3")
                    except:
                        pronounce.get_audio(word_info['word'])
                        playsound("./audio/" + word_info['word'] + ".mp3")
                else:
                    os.system("cls")
                    break

        for index in word_time_dict:
            word.set_s(index,word_time_dict[index])

        sys.exit()

# 一个单词 每答错一次意思需要n+1次通过（上限为5次）

# 需要记录单词打错次数

# 需要可视化曲线
