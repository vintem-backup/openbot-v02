import sys
import os
from datetime import datetime
import requests

def utc_time_func():

    try:
    
        url = 'http://worldclockapi.com/api/json/utc/now'

        time_utc_now = requests.get(url).json

        year = int(time_utc_now()['currentDateTime'].split('T')[0].split('-')[0])
        month = int(time_utc_now()['currentDateTime'].split('T')[0].split('-')[1])
        day = int(time_utc_now()['currentDateTime'].split('T')[0].split('-')[2])

        hour = int(time_utc_now()['currentDateTime'].split('T')[1].split(':')[0])
        minute = int(time_utc_now()['currentDateTime'].split('T')[1].split(':')[1].split('Z')[0])
    
        utc_now = datetime(year, month, day, hour, minute)
    
    except (Exception) as error: #Tratar exceção (provavelmente enviar para telegram)
        
        utc_now = datetime.utcnow()

    return utc_now

def log_handler(msg,destination):
    
    from . import notification

    """Envia uma mensagem de log para o destino escolhido pelo usuário.
    
    
    Keyword arguments:
    =================
    
    msg         -- Mensagem de log
    destination -- Caminho padrão para saída da mensagem de log
    
    *destination options*
     -------------------
        - mute   ==> Ignora a mensagem
        - print  ==> Printa na tela
        - logm   ==> Envia para o arquivo padrão de monitoramento
        - logw   ==> Envia para o arquivo padrão de alertas
        - tlgrm  ==> Envia para o grupo de monitoramento do telegram
        - tlgrw  ==> Envia para o grupo de alertas do telegram    
    """
    
    if (destination == 'mute'):
        
        pass
    
    elif (destination == 'print'):
        
        print(msg)
    
    elif (destination == 'logm'):
        
        #Se em desenvolvimento:
        #path_to_logfile = os.getcwd().split(sep="BinanceDataStorageDaemon/")[0] + 'logs/monitoring.log'
        
        path_to_logfile = 'logs/monitoring.log'
        
        sys.stdout = open(path_to_logfile, "a")
        
        print(msg)
        
    elif (destination == 'logw'):
        
        #Se em desenvolvimento:
        #path_to_logfile = os.getcwd().split(sep="BinanceDataStorageDaemon/")[0] + 'logs/warning.log'
        
        path_to_logfile = 'logs/warning.log'
        
        sys.stdout = open(path_to_logfile, "a")
        
        print(msg)
        
    elif (destination == 'tlgrm'):
        
        notification.Telegrambot(msg).monitoring()
        
    elif (destination == 'tlgrw'):
        
        notification.Telegrambot(msg).warning()


def sql_command(table_name, keys, action, **kwargs):
    
    """Dado um nome de tabela <table_name> e o dicionário <keys> (em que a chave será o nome da coluna e 
    o valor definirá o tipo de dado gravado - vide documentação do PostgreSQL), retorna o comando SQL ade-
    quado para criação da tabela ou salvamento de dados em uma tabela.
    
    
    Keyword arguments:
    =================
    
    table_name  -- Nome da tabela a ser buscada
    keys        -- Dicionário com as chaves e seus respectivos tipos
    action      -- O tipo de ação desejada com o comando SQL, criar ou salvar.

    *action options*
     ------------
        - create ==> SQL para criar uma tabela
        - save   ==> SQL para salvar em uma tabela
    
    **kwargs:
    =========
    
    pk -- Chave primária
    """
    
    pk = kwargs.get('pk')
    
    key_list = list(keys.keys())
    type_list = list(keys.values())
    
    sql = ''
    
    if (action == 'create'):
        
        sql = 'CREATE TABLE ' + table_name + ' ('
        
        for i in range (len(keys)-1):
            
            entry = key_list[i] + ' ' + type_list[i]
            
            if (pk):
                
                if (key_list[i] == pk):
                    
                    entry = key_list[i] + ' ' + type_list[i] + ' PRIMARY KEY'
                        
            sql = sql + entry + ', '

        sql = sql + key_list[len(keys)-1] + ' ' + type_list[len(keys)-1] + ')'
        
    if (action == 'save'):
        
        format_code = ''
        
        sql = 'INSERT INTO ' + table_name + ' ('
        
        for i in range (len(keys)-1):
            
            sql = sql + key_list[i] + ' ' + ', '
            
            format_code = format_code + '%s, '

        sql = sql + key_list[len(keys)-1] + ' ' + ') VALUES (' + format_code + '%s)'
                        
    return sql

#ESCREVER DOCSTRING
def binance_klines_to_postgres_klines(in_dt):
    
    binance_time = datetime.fromtimestamp(int((requests.get('https://api.binance.com/api/v1/time').json()['serverTime'])/1000))
    
    #utc_time = datetime.utcnow()

    utc_time = utc_time_func()
    
    delta_time = utc_time - binance_time

    delta_hour = round(delta_time.total_seconds()/3600)
    
    delta = delta_hour*3600
    
    out_dt = []
    
    for i in range (len(in_dt)):
        
        open_time = datetime.fromtimestamp(int(in_dt[i][0]/1000))
        
        if (delta != 0): open_time = datetime.fromtimestamp(int(in_dt[i][0]/1000) + delta)
                
        data = (open_time, in_dt[i][1], in_dt[i][2], in_dt[i][3], in_dt[i][4], 
                in_dt[i][5], in_dt[i][7], in_dt[i][8], in_dt[i][9], in_dt[i][10])
    
        out_dt.append(data)
    
    return out_dt


def export_env_var(path_to_env_file):
    
    try:
        
        env_file = open(path_to_env_file).readlines()
        export_status = 'done'
    
    except:

        export_status = 'fail'
                
    finally:

        if (export_status == 'done'):

            for i in range(1,len(env_file)-1):

                if ('=' in env_file[i]):

                    key=env_file[i].split('=')[0]
                    value=env_file[i].split('=')[1].split()[0]
                    os.environ[key] = value
    
    return export_status