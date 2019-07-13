# -*- coding: utf-8 -*-
'''
@author: yaleimeng@sina.com
@license: (C) Copyright 2017
@desc:  python3 版本中文Alice，暂时简单添加空格
@DateTime: Created on 2017/11/15，at  10:20       '''

from py3aiml.Kernel import Kernel
from filter import DFAFilter, test_first_character
import os

alice = Kernel()
# if os.path.isfile("bot_brain.brn"):
#     alice.bootstrap(brainFile = "bot_brain.brn")
# else:
#     alice.bootstrap(learnFiles = "std-startup.xml", commands = "load aiml b")
#     alice.saveBrain("bot_brain.brn")
alice.learn("std-startup.aiml")
while True:
    s = input('Finty请您提问...>>')
    gfw = DFAFilter()
    gfw.parse("keywords2.txt")
    s = gfw.filter(s, '')
    if s == "退出对话":
        break
    else:
        result = alice.respond(s).strip()
        if result=="":
            print("我好像不明白")
        else:
            print(result)
