import sys
import os
import subprocess
import time
from datetime import datetime
import requests
from modules import db_functions as dbf, general_functions as gf

"""A cada minuto lê a tabela dos pares e, para todos aqueles cujo campo "get_data" estiver marcado como
"on" (e cujo campo "status" não seja "building"), chamará um subprocesso para completar o dado, até o tempo
presente. Deve escrever na mesma tabela dos pares o PID do subprocesso evocado para cada par. Caso a tabela
de dados para aquele i-ésimo par não exista, será criada.
"""

keys = {'open_time': 'timestamp', 'open': 'numeric', 'high': 'numeric', 'low': 'numeric', 'close': 'numeric', 
        'volume': 'numeric', 'quote_asset_volume': 'numeric', 'number_of_trades': 'integer', 
        'taker_buy_base_asset_volume': 'numeric', 'taker_buy_quote_asset_volume': 'numeric'}

default_log = 'logm'

DataCompleter = 'DataCompleter.py'

if (os.environ['run_mode'] == 'dev'): DataCompleter = str(os.getcwd()) + '/BinanceDataStorageDaemon/DataCompleter.py'
    
round_count = 0

binance_time = datetime.fromtimestamp(int((requests.get('https://api.binance.com/api/v1/time').json()['serverTime'])/1000))

#utc_time = datetime.utcnow()

utc_time = gf.utc_time_func()

delta_time = utc_time - binance_time

delta_hour = round(delta_time.total_seconds()/3600)

delta = delta_hour*3600

while True:
    
    msg = '''ENTRADA (ciclo: ''' + str(round_count) + ''')
=================================================================================================
FROM.: Main
AT...: ''' + str(datetime.now()) + '''

'''
        
    gf.log_handler(msg,default_log)

    #Busca pela tabela de pares
    pairs = dbf.read_table('binance_pairs')#,mute = 'yes')
    
    if (len(pairs) > 0): #Enconta a tabela dos pares
        
        n_pairs_on = 0
        for pair in pairs:
            
            if (pair['get_data'] == 'ON'): n_pairs_on+=1
        
        if(n_pairs_on > 0): 
            
            for pair in pairs:

                candle_interval = '1m' #Futuramente, pode ser passada por um parâmetro.

                table_name = 'binance_klines_' + str(pair['name']) + '_' + candle_interval

                if (pair['get_data'] == 'ON'):

                    if (pair['status'] == 'absent'):

                        start_time = '1241893500000'
                        
                        create_table_job_satus = dbf.create_table(table_name,keys,pk='open_time')

                        pid = subprocess.Popen([sys.executable, DataCompleter, str(pair['name']), candle_interval, start_time])

                        update_table_job_status = dbf.update_table('binance_pairs', 'name', str(pair['name']), 'last_change_by_pid', int(pid.pid))

                        msg = '''
{ciclo: ''' + str(round_count) + ''', par: ''' + str(pair['name']) + ''', PID: ''' + str(pid.pid) + '''} 
'''
        
                        gf.log_handler(msg,default_log)

                    elif (pair['status'] == 'full'):

                        #Tenta buscar a tabela de candles para este par, retornando a amostra gravada mais recentemente
                        last_saved_candle = dbf.read_table(table_name, field_key = 'open_time',
                                                            sort_type = 'DESC', limit = '1')#, mute = 'yes')

                        open_time = datetime.timestamp(last_saved_candle[0]['open_time'])
                        
                        if (delta != 0): open_time = datetime.timestamp(last_saved_candle[0]['open_time']) - delta

                        start_time = str(int((open_time*1000) + 30000))
                            
                        pid = subprocess.Popen([sys.executable, DataCompleter, str(pair['name']), candle_interval, start_time])
                            
                        update_table_job_status = dbf.update_table('binance_pairs', 'name', str(pair['name']), 'last_change_by_pid', int(pid.pid))
                          
                        msg = '''
{ciclo: ''' + str(round_count) + ''', par: ''' + str(pair['name']) + ''', PID: ''' + str(pid.pid) + '''} 
'''
        
                        gf.log_handler(msg,default_log)
                    
                    elif (pair['status'] == 'building'):
        #AQUI SERÁ TRATADO O CENÁRIO EM QUE O STATUS ESTÁ "BUILDING", PORÉM O PID CAIU

                        msg = '''
{ciclo: ''' + str(round_count) + ''', par: ''' + str(pair['name']) + ''', PID: ''' + str(pair['last_change_by_pid']) + '''} 
'''
        
                        gf.log_handler(msg,default_log)
       
            sleep_time = 60 - int(datetime.now().second)

        else: #n_pairs_on = 0
            
            sleep_time = 300

            msg = '''
nenhum par marcado com get_data "ON".
'''

            gf.log_handler(msg,default_log)

    else: #Não encontra a tabela de PARES.

        msg = '''
Tabela de pares não encontrada.
'''

        gf.log_handler(msg,default_log)

        sleep_time = 300
    
    msg = '''
FROM.: Main
AT...: ''' + str(datetime.now()) + '''
=================================================================================================
SAÍDA (ciclo: ''' + str(round_count) + '''). Dormindo ''' + str(sleep_time) + ''' segundos

'''
        
    gf.log_handler(msg,default_log)
    
    round_count+=1
    
    time.sleep(sleep_time)