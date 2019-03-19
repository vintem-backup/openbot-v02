#esdb.py

#!/usr/bin/env python3
# coding: utf-8

'''Este módulo deve tratar, "pythonicamente" do banco elasticsearch (leitura, escrita
e funções complementares, como retornar um índece ou Id específicos), abstraindo boa 
parte da sintaxe das APIs (elasticsearch, elasticsearch DSL e requests), para que o 
foco seja a análise de dados.
'''

#import os

class Parser:
    '''Lida com o trânsito de dados entre um banco elasticsearc e os programas
    que consoem, criam ou modificam essas entradas de dados.
    '''
    
    def __init__(self,db_host_name,data): #*args ou **kwargs (?)
        self.fail='Parse fail because: '
        self.db_host_name=db_host_name
        self.data=data

    def post_single(self):
        '''Post a single data to a single Id.'''
        
        try:
            print("hello")
            return 'done'
        except Exception as e:
            print(self.fail + str(e))
            return 'undone'

    def post_various(self):
        '''Post each entry in the dataframe to differents single Ids.'''
        
        try:
            print("hello")
            return 'done'
        except Exception as e:
            print(self.fail + str(e))
            return 'undone'

    def get_single(self):
        '''Get single data from single Id.'''
        
        try:
            print("hello")
            return 'done'
        except Exception as e:
            print(self.fail + str(e))
            return 'undone'

    def get_various(self):
        '''Get a single dataframe from differents single Ids.'''
        
        try:
            print("hello")
            return 'done'
        except Exception as e:
            print(self.fail + str(e))
            return 'undone'

class Dev:
    '''Lida com o trânsito de dados entre o banco elasticsearc em produção e os programas
    que consoem ou criam essas entradas de dados.
    '''

    def start(self):
        '''Start dev_db.'''
        
        try:
            print("hello")
            return 'done'
        except Exception as e:
            print(self.fail + str(e))
            return 'undone'

    def stop(self):
        '''Stop dev_db.'''
        
        try:
            print("hello")
            return 'done'
        except Exception as e:
            print(self.fail + str(e))
            return 'undone'