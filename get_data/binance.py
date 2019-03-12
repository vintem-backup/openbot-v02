#binance.py

#!/usr/bin/env python3
# coding: utf-8

'''

Script "teste_padrão" para validação da estrutura do cluster

'''

import os
import sys
import time

sys.path.append(os.getcwd())

import lib
from lib import notice

msg = str((open(os.environ["stock_exchange"]+'.txt',"r")).read())

notice.Telegrambot('Start get_data-test | from '+os.environ["environment"]).monitoring()

i=0
while True:
    
    notice.Telegrambot(msg+' | cycle: '+str(i)+' | from '+os.environ["environment"]).monitoring()
    i+=1
    time.sleep(30)