#!/usr/bin/env python
# coding: utf-8

'''

'''

import os
import time

import lib
from lib import notice

notice.telegram_bot('msg_entrada').trade()

i=0
while True:
    
    notice.telegram_bot('msg_ciclo '+str(i)).trade()
    i+=1
    time.sleep(30)