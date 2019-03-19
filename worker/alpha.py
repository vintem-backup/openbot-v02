#alpha.py

#===================================================================================#
#                                 * COMMON HEADER *                                 #
#===================================================================================#
#!/usr/bin/env python3                                                              #
# coding: utf-8                                                                     #
                                                                                    #
import os                                                                           #
import sys                                                                          #
                                                                                    #
sys.path.append(os.getcwd())                                                        #
                                                                                    #
import lib                                                                          #
#===================================================================================#

'''Script "teste_padrão" para validação da estrutura do cluster'''

#__MAIN__

#Specific modules
import time
from lib import notice

msg = str((open(os.environ["strategy"]+'.txt',"r")).read())

notice.Telegrambot('Start get_data-test | from '+os.environ["environment"]).trade()

i=0
while True:
    
    notice.Telegrambot(msg+' | cycle: '+str(i)+' | from '+os.environ["environment"]).trade()
    i+=1
    time.sleep(30)