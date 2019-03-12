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
    '''Lida com o trânsito de dados entre o banco do elasticsearc e o programa'''
    
    def __init__(self,db_host_name,data): #*args ou **kwargs (?)
        self.fail='Parse fail because: '
        self.db_host_name=db_host_name
        self.data=data

    def write(self):
        '''Write data (dictionary type?) to elasticsearch database.'''
        
        try:
            print("hello")
        except Exception as e:
            print(self.fail + str(e))

    def read(self):
        '''Read data from elalsticsearch database, return dictionary (?)'''
        
        try:
            print("hello")
        except Exception as e:
            print(self.fail + str(e))