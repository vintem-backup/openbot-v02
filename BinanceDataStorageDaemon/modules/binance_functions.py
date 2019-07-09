#binance functions

#Import
import requests
import json
import time
from datetime import datetime
from . import general_functions as gf

#ESCREVER DOCSTRING
def binance_klines_request_handler(pair, interval, start_time, max_attempts):
    
    klines = []
    
    url = '''https://api.binance.com/api/v1/klines?symbol=''' + pair + '''&interval=''' + interval + '''&startTime=''' + start_time
    
    default_log = 'logw'
    
    for i in range(max_attempts):
        
        #Tenta conexão com a Binance
        try:

            response = requests.get(url)
            
            response.raise_for_status()
                        
        #Request falhou
        except (Exception, requests.exceptions.RequestException) as error: #TRATAR EXCEÇÃO AQUI
            
            msg = '''
FROM.: binance_klines_request_handler
AT...: ''' + str(datetime.now()) + '''

Par ''' + pair + ''': Comunicação com a Binance falhou no ''' + str(i+1) + '''\u00bA request, devido ao erro:

''' + str(error) + '''

'''
            
            gf.log_handler(msg,default_log)
            
            time.sleep(5)
            
        finally:
            
            if (int(response.status_code) == 200):
                
                klines = response.json()
                
                break

    return klines