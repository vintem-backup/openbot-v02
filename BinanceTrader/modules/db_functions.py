#Db functions

#Import
import psycopg2
import psycopg2.extras
import os
from datetime import datetime
from . import general_functions as gf

#Environment
#POSTGRES_DB = os.environ.get('POSTGRES_DB')
#POSTGRES_USER = os.environ.get('POSTGRES_USER')
#POSTGRES_PASSWORD = os.environ.get('POSTGRES_PASSWORD')
#DB_HOST = os.environ.get('DB_HOST')


DB_HOST='localhost'
POSTGRES_DB='pg_dev' 
POSTGRES_PASSWORD='06Fj@%r7KTXm5+eWn2'
POSTGRES_USER='openbot'

#Functions

def create_table(table_name,keys,**kwargs):
    
    """Cria a tabela <table_name>, com as colunas <keys[i]>. Opcionalmente pode-se definir uma das chaves como 
    chave primária, ao invés da chave default atribuida pelo postgres.
    
    
    Keyword arguments:
    =================
    
    table_name  -- Nome da tabela a ser criada
    keys        -- Chaves (nomes das colunas)


    **kwargs:
    ========
    
    pk   -- Chave que será atribuida como primária 
    mute -- Suprime o log se 'yes'
    """
    
    pk = kwargs.get('pk')
    
    mute = kwargs.get('mute')
    
    connection = '' #Inicialmente definida como string
    
    #NÃO DEVERIA ESTAR AQUI
    #records = [] #Inicialmente definida como uma lista vazia
    
    create_table_job_status = 'fail' 
    
    default_log = 'logw'
    
    if(mute):
        
        if(mute == 'yes'): default_log = 'mute'
    
    #Tenta conectar ao banco
    try:

        connection = psycopg2.connect(host=DB_HOST, database=POSTGRES_DB, 
                                      user=POSTGRES_USER, password=POSTGRES_PASSWORD)

        pointer = connection.cursor(cursor_factory=psycopg2.extras.DictCursor)
    
    #Não conecta ao banco
    except (Exception, psycopg2.Error) as error: #TRATAR EXCEÇÃO AQUI

        msg = '''
FROM.: create_table
AT...: ''' + str(datetime.utcnow()) + '''

Não foi possível conectar ao banco devido ao erro: 
''' + str(error) + '''.

'''
        
        gf.log_handler(msg,default_log)

    finally:

        if (type(connection) != str): #Conexão bem sucedida com o banco de dados    
    
            #Tenta criar a tabela
            try:
                
                sql_create_query = gf.sql_command(table_name, keys, 'create')
                
                if (pk):
                    
                    sql_create_query = gf.sql_command(table_name, keys, 'create', pk=pk)
                
                pointer.execute(sql_create_query)
                
                connection.commit()
                
                create_table_job_status = 'done'

            #Erro aocriar tabela
            except (Exception, psycopg2.Error) as error: #TRATAR EXCEÇÃO AQUI
                
                #Desfaz ação do ponteiro
                pointer.execute("ROLLBACK")

                msg = '''
FROM.: create_table
AT...: ''' + str(datetime.utcnow()) + '''

Não foi possível criar tabela ''' + table_name + ''' devido ao erro: 
''' + str(error) + '''.

'''
   
                gf.log_handler(msg,default_log)
    
    return create_table_job_status

                    
def read_table(table_name, **kwargs):
    
    """Busca no banco a tabela [table_name], retornando uma lista, tal que cada elemento representa
    uma linha (registro) da tabela, ou uma lista vazia, caso a tabela não seja encontrada. Pode retornar
    a tabela inteira, ou parte dos valores se forem informados, corretamente, os argumentos opcionais
    **kwargs.
    
    
    Keyword arguments:
    =================
    
    table_name  -- Nome da tabela a ser buscada
    
    **kwargs:
    =========
    
    mute -- Suprime o log se 'yes'
    
    field_key -- Chave (nome da coluna) do campo tomado como referência de ordenamento
    
    sort_type      -- Modo como os registros são buscados:
        
    *sort_type options*
     -----------------
        - DESC ==> Do maior para o menor
        - ASC  ==> Do menor para o maior
        
    limit     -- Número de registros que devem ser retornados
    """
    
    field_key = kwargs.get('field_key')
    
    sort_type = kwargs.get('sort_type')
    
    limit = kwargs.get('limit')

    mute = kwargs.get('mute')
    
    connection = '' #Inicialmente definida como string
    
    records = [] #Inicialmente definido como uma lista vazia.
    
    default_log = 'logw'

    if(mute):
        
        if(mute == 'yes'): default_log = 'mute'
    
    #Tenta conectar ao banco
    try:

        connection = psycopg2.connect(host=DB_HOST, database=POSTGRES_DB, 
                                      user=POSTGRES_USER, password=POSTGRES_PASSWORD)

        pointer = connection.cursor(cursor_factory=psycopg2.extras.DictCursor)
        
        msg = '''
FROM.: read_table
AT...: ''' + str(datetime.utcnow()) + '''

Conectado ao banco com sucesso!

'''

        gf.log_handler(msg,'mute')

    #Não conecta ao banco    
    except (Exception, psycopg2.Error) as error: #TRATAR EXCEÇÃO AQUI

        msg = '''
FROM.: read_table
AT...: ''' + str(datetime.utcnow()) + '''

Não foi possível conectar ao banco devido ao erro: 
''' + str(error) + '''

'''
        
        gf.log_handler(msg,default_log)

    finally:

        if (type(connection) != str): #Conexão bem sucedida com o banco de dados
            
            #Tenta obter a tabela
            try:
                
                sql_select_query = 'SELECT * FROM ' + table_name
                
                if (field_key and sort_type and limit):
                    
                    sql_select_query = sql_select_query + ' ORDER BY ' + field_key + ' ' + sort_type + ' LIMIT ' + limit

                pointer.execute(sql_select_query)

                records= pointer.fetchall()
                
                msg = '''
FROM.: read_table
AT...: ''' + str(datetime.utcnow()) + '''

Tabela ''' + table_name +''' obtida com sucesso! 

'''
                
                gf.log_handler(msg,'mute')

            #Não encontra tabela
            except (Exception, psycopg2.Error) as error: #TRATAR EXCEÇÃO AQUI
                
                #Desfaz ação do ponteiro
                pointer.execute("ROLLBACK")

                msg = '''
FROM.: read_table
AT...: ''' + str(datetime.utcnow()) + '''

Não foi possível obter tabela ''' + table_name +''' devido ao erro: 
''' + str(error) + '''

'''
                
                gf.log_handler(msg,default_log)
            
            pointer.close()
            connection.close()
    
    return records


def update_table(table_name, pk_field, pk_value, field_to_update, new_field_value, **kwargs):
  
    """Dada uma certa tabela, atualiza uma entrada específica da mesma.
    
    
    Keyword arguments:
    =================
    
    table_name      -- Nome da tabela a ser buscada
    pk_field        -- Chave (nome da coluna) atribuída como chave primária; ``pk``, se chave default.
    pk_value        -- Valor da chave primária do registro
    field_to_update -- Chave (nome da coluna) do campo a ser regravado
    new_field_value -- Novo valor a ser gravado no campo
    
    **kwargs:
    =========
    
    mute -- Suprime o log se 'yes'
    """
    
    mute = kwargs.get('mute')

    connection = ''
    
    update_table_job_satus = 'fail'
    
    default_log = 'logw'
    
    if(mute):
        
        if(mute == 'yes'): default_log = 'mute'
    
    #Tenta conectar ao banco
    try:

        connection = psycopg2.connect(host=DB_HOST, database=POSTGRES_DB, 
                                      user=POSTGRES_USER, password=POSTGRES_PASSWORD)

        pointer = connection.cursor(cursor_factory=psycopg2.extras.DictCursor)
    
    #Não conecta ao banco
    except (Exception, psycopg2.Error) as error: #TRATAR EXCEÇÃO AQUI
        
        msg = '''
FROM.: update_table
AT...: ''' + str(datetime.utcnow()) + '''

Não foi possível conectar ao banco devido ao erro: 
''' + str(error) + '''

'''
        gf.log_handler(msg,default_log)
        
    finally:

        if (type(connection) != str): #Conexão bem sucedida com o banco de dados
            
            #Tenta atualizar entrada na tabela
            try:

                sql_update_query = 'Update ' + table_name + ' set ' + field_to_update + ' = %s where ' + pk_field + '= %s'
                
                pointer.execute(sql_update_query, (new_field_value, pk_value))

                connection.commit()

                update_table_job_satus = 'done'

            #Não consegue atualizar entrada
            except (Exception, psycopg2.Error) as error: #TRATAR EXCEÇÃO AQUI

                #Desfaz a ação do ponteiro
                pointer.execute("ROLLBACK")

                msg = '''
FROM.: update_table
AT...: ''' + str(datetime.utcnow()) + '''

Tabela ''' + table_name + ''': Não foi possível atualizar a entrada ''' + field_to_update + ''' 
do registro ''' + pk_value + ''' para ''' + new_field_value + ''' devido ao erro: 
''' + str(error) + '''

'''
   
                gf.log_handler(msg,default_log)
    
            pointer.close()
            connection.close()

    return update_table_job_satus


def save_in_table(table_name, keys, data, **kwargs):
    
    """Salva na tabela <table_name>, nas respectivas colunas <keys[i]>, os dados correspondentes, <data>.
    
    
    Keyword arguments:
    =================
    
    table_name  -- Nome da tabela na qual os dados devem ser gravados
    keys        -- Chaves (nomes das colunas)
    data_list   -- Lista de dados a serem gravados


    **kwargs:
    ========

    mute -- Suprime o log se 'yes'
    """

    mute = kwargs.get('mute')

    connection = ''
    
    save_in_table_job_satus = 'fail'
    
    default_log = 'logw'
    
    if(mute):
        
        if(mute == 'yes'): default_log = 'mute'
    
    #Tenta conectar ao banco
    try:

        connection = psycopg2.connect(host=DB_HOST, database=POSTGRES_DB, 
                                      user=POSTGRES_USER, password=POSTGRES_PASSWORD)

        pointer = connection.cursor(cursor_factory=psycopg2.extras.DictCursor)
    
    #Não conecta ao banco
    except (Exception, psycopg2.Error) as error: #TRATAR EXCEÇÃO AQUI
        
        msg = '''
FROM.: save_in_table
AT...: ''' + str(datetime.utcnow()) + '''

Não foi possível conectar ao banco devido ao erro: 
''' + str(error) + '''.

'''
        
        gf.log_handler(msg,default_log)
        
    finally:

        if (type(connection) != str): #Conexão bem sucedida com o banco de dados
            

            #Tenta salvar os dados na tabela
            try:
                
                sql_save_query = gf.sql_command(table_name, keys, 'save')
                
                for i in range(len(data)):
                    
                    pointer.execute(sql_save_query, data[i])
                
                connection.commit()
                
                save_in_table_job_satus = 'done'

            except (Exception, psycopg2.Error) as error: #TRATAR EXCEÇÃO AQUI

                #Desfaz ação do ponteiro
                pointer.execute("ROLLBACK")

                msg = '''
FROM.: save_in_table
AT...: ''' + str(datetime.utcnow()) + '''

Não foi possível salvar dados na tabela: ''' + table_name + ''' devido ao erro: 
''' + str(error) + '''.

'''

                gf.log_handler(msg,default_log)
    
    return save_in_table_job_satus