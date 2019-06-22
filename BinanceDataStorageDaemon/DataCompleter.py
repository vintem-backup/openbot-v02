import os
import sys
import time
from datetime import datetime
from modules import binance_functions as bf, db_functions as dbf, general_functions as gf

#FAZER A DOCSTRING

pair = str(sys.argv[1])

interval = str(sys.argv[2])

start_time = str(sys.argv[3])

table_name = 'binance_klines_' + pair + '_' + interval

keys = {'open_time': 'timestamp', 'open': 'numeric', 'high': 'numeric', 'low': 'numeric', 'close': 'numeric',
    'volume': 'numeric', 'quote_asset_volume': 'numeric', 'number_of_trades': 'integer',
    'taker_buy_base_asset_volume': 'numeric', 'taker_buy_quote_asset_volume': 'numeric'}

max_attempts = 10 #pode vir de um parâmetro depois

default_logm = 'mute'
default_logw = 'logw'

#Atualiza o status do par em operação para 'building'
update_table_job_status = dbf.update_table('binance_pairs', 'name', pair, 'status', 'building')

if (update_table_job_status == 'fail'): #Tratar exceção update_table_job_status = 'fail'

    msg = '''
FROM.: DataCompleter
AT...: ''' + str(datetime.now()) + '''
PAR..: ''' + pair + '''

Atualização do status para building falhou!

'''

    gf.log_handler(msg,default_logw)

#total_num_requests = 0
round_counter = 1

while True:

    msg = '''ENTRADA (ciclo: ''' + str(round_counter) + ''')
=================================================================================================
FROM.: DataCompleter
AT...: ''' + str(datetime.now()) + '''
PAR..: ''' + pair + '''

'''
        
    gf.log_handler(msg,default_logm)

    klines = []
    
    klines = bf.binance_klines_request_handler(pair, interval, start_time, max_attempts)
    
    if (len(klines) > 0):
        
        if (len(klines) < 500): #Chegou na kline mais recente
            
            klines = klines[:(len(klines)-1)] #Apaga o último resgistro (candle não fechado)
            
            if (len(klines) == 0): 
                
                msg = '''
FROM.: DataCompleter
AT...: ''' + str(datetime.now()) + '''
PAR..: ''' + pair + '''

*********************
 **  KLINE NULA  ***
*********************
'''

                gf.log_handler(msg,default_logw)
                
                break
        
        most_recent_open_time = klines[len(klines)-1][0] #open_time do último candle

        start_time = str(most_recent_open_time + 30000) #Um passo de 30s (30000 milissegundos)
        
        klines = gf.binance_klines_to_postgres_klines(klines) #Parse das klines
        
        save_in_table_job_status = dbf.save_in_table(table_name, keys, klines)

        msg = '''
Leva de ''' + str(len(klines)) + ''' klines salvas no banco
'''

        gf.log_handler(msg,default_logm)  
        
        if (len(klines) < 500):
            
            data_completer_job_status = 'done'

            msg = '''
Kline mais recente!
'''

            gf.log_handler(msg,default_logm) 

            break

        if (len(klines) > 500): #Alguma anomalia.

            msg = '''
FROM.: DataCompleter
AT...: ''' + str(datetime.now()) + '''
PAR..: ''' + pair + '''

ATENÇÃO, OCORREU UMA ANOMALIA: MAIS DE 500 AMOSTRAS RETORNADAS!

'''

            gf.log_handler(msg, default_logw) 
            
            break
            
    else: #(Falha de comunicação com a binance: klines nulas)

        msg = '''
FROM.: DataCompleter
AT...: ''' + str(datetime.now()) + '''
PAR..: ''' + pair + '''

ATENÇÃO, ERRO DE COMUNICAÇÃO COM A BINANCE!

'''

        gf.log_handler(msg, default_logw) 
    
    msg = '''
FROM.: DataCompleter
AT...: ''' + str(datetime.now()) + '''
PAR..: ''' + pair + '''
=================================================================================================
SAÍDA (ciclo: ''' + str(round_counter) + ''').

'''
        
    gf.log_handler(msg,default_logm)
    
    response_ping = requests.get('https://api.binance.com/api/v1/ping')

    total_req_courrent_minute = int(response_ping.headers['X-MBX-USED-WEIGHT'])
    
    if(total_req_courrent_minute >= 1100):

        msg = '''
Número máximo de requests atingido, dormindo 1 min
'''

        gf.log_handler(msg,default_logm) 

        time.sleep(60)

    round_counter+=1

#Atualiza o status do par em operação para 'full'
update_table_job_status = dbf.update_table('binance_pairs', 'name', pair, 'status', 'full')

if (update_table_job_status == 'fail'): #Tratar exceção update_table_job_status = 'fail'

    msg = '''
FROM.: DataCompleter
AT...: ''' + str(datetime.now()) + '''
PAR..: ''' + pair + '''

Atualização do status para full falhou!

'''

    gf.log_handler(msg,default_logw)

msg = '''
FROM.: DataCompleter
AT...: ''' + str(datetime.now()) + '''
PAR..: ''' + pair + '''

FIM DATACOMPLETER
'''
   
gf.log_handler(msg,default_logm)