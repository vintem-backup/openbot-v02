#!/usr/bin/env python
# coding: utf-8

'''

'''

import os
import time

import lib
from lib import notice

notice.telegram_bot('trade','msg_entrada').send()

while True:
    
    notice.telegram_bot('trade','msg_ciclo').send()
    time.sleep(30)