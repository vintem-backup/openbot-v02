#!/usr/bin/env python
# coding: utf-8

'''
Recebe os parâmetros e compõe os comandos a fim de executar as runtimes 
(***get_data, BT ou trade***) corretas.

Usage: 
python main.py '<operation_name>' '<strategy>' '<state>' '<stock_exchange>' '<market>'

'''

import sys
import os

path_to_src=os.getcwd().split(sep="docker-cluster")[0]+'docker-cluster/worker'
sys.path.append(path_to_src)

if __name__ == "__main__":
    operation_name=str(sys.argv[1])
    strategy = str(sys.argv[2])
    state = str(sys.argv[3])
    stock_exchange = str(sys.argv[4])
    market = str(sys.argv[5])

    import_strategy = 'from '+'src.strategies.'+strategy+' import *'
    start_get_data = 'python get-data.py '+stock_exchange+' '+market
    start_back_test = 'python BT_'+strategy+'.py '+operation_name+' '+stock_exchange+' '+market
    start_operation = 'python '+strategy+'.py '+operation_name+' '+stock_exchange+' '+market
  
    exec(import_strategy)
    
    if (state != 'off'): exec(start_get_data)
    if (state == 'bt'): exec(start_back_test)
    if (state == 'trade'): exec(start_operation)
    if (state == 'both'): 
        exec(start_back_test)
        exec(start_operation)

    #print(start_get_data)

    #print(start_back_test)

    #print(start_operation)