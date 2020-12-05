from __future__ import print_function, unicode_literals
from PyInquirer import style_from_dict, Token, prompt, Separator

import sys
import os

from message import Message

message = Message()

def change_plan(word):
    questions = [
        {
            'type': 'input',
            'name': 'amount',
            'message': 'How many word you want to learn each day?'
        }
    ]
    answer = prompt(questions, style=Common.style)
    word.change_plan(int(answer['amount']))
    if os.path.exists('./resource/plan') is False:
        message.normal("fail to set plan")
        sys.exit()

    return word


def set_plan(word):
    questions = [
        {
            'type': 'input',
            'name': 'amount',
            'message': 'How many word you want to learn each day?'
        }
    ]
    answer = prompt(questions, style=Common.style)
    word.set_plan(int(answer['amount']))
    if os.path.exists('./resource/plan') is False:
        message.normal("fail to set plan")
        sys.exit()

    return word


class Common(object):
    style = style_from_dict({
        Token.Separator: '#cc5454',
        Token.QuestionMark: '#673ab7 bold',
        Token.Selected: '#cc5454',  # default
        Token.Pointer: '#FFFFCC bold',
        Token.Instruction: '',  # default
        Token.Answer: '#f44336 bold',
        Token.Question: '',
    })
