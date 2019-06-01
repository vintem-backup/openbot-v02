#teste.py

#===================================================================================#
#                                 * COMMON HEADER *                                 #
#===================================================================================#
#!/usr/bin/env python3                                                              #
# coding: utf-8                                                                     #
                                                                                    #
import os                                                                           #
import sys                                                                          #
                                                                                    #
#sys.path.append(os.getcwd())                                                        #
                                                                                    #
#import lib                                                                          #
#===================================================================================#

'''Script "teste_padrão" para validação da estrutura do cluster'''

#__MAIN__

#Specific modules
import time
import notice

msg = 'teste' + str(sys.argv[1]) + ' ' + str(sys.argv[2])


notice.Telegrambot('hello again').trade()

i=0
while True:
    
    notice.Telegrambot(msg+' | cycle: '+str(i)+' | from local new cluster').trade()
    i+=1
    time.sleep(5)
