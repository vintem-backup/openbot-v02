#binance.py

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
from lib import binance_data
from elasticsearch import Elasticsearch

msg = str((open(os.environ["stock_exchange"]+'.txt',"r")).read())

notice.Telegrambot('Start get_data-test | from '+os.environ["environment"]).monitoring()

host=os.environ['database_host']
indexName = 'marketdata-' + os.environ['market'] +'-1m-'+os.environ['stock_exchange']
es = Elasticsearch(hosts=[host])

try:
    es.indices.get_alias("*")[indexName]
    try:
        binance_data.live_update_marketdata(host,indexName)
    except:
        msg = 'Binance connection failure! Check it out.'
        notice.Telegrambot(msg).warning()   
except:
    try:
        binance_data.create_marketdata(host,os.environ['market'].upper(),'1m','1 day ago UTC')
    except:
        msg = 'Binance connection failure! Check it out.'
        notice.Telegrambot(msg).warning()

i=0
while True:
    
    notice.Telegrambot(msg+' | cycle: '+str(i)+' | from '+os.environ["environment"]).monitoring()
    i+=1
    time.sleep(30)