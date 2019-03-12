#alpha.py

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

msg = str((open(os.environ["strategy"]+'.txt',"r")).read())

notice.Telegrambot('Start worker-test').trade()

i=0
while True:
    
    notice.Telegrambot(msg+' | cycle: '+str(i)).trade()
    i+=1
    time.sleep(30)