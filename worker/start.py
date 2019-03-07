#!/usr/bin/env python
# coding: utf-8

'''

'''

import sys

import os

#path_to_src=os.getcwd().split(sep="docker-cluster")[0]+'docker-cluster/worker'
#sys.path.append(path_to_src)

#import_strategy = 'from src.strategies.'+(var['strategy'])+' import *'

import_strategy = 'from src.strategies.'+(os.environ['strategy'])+' import *'

print(import_strategy)

'''
exec(import_strategy)

if ((os.environ['mode']) == 'bt'): print('python backtest.py')

if ((os.environ['mode']) == 'trade'): print('python trade.py')

if ((os.environ['mode']) == 'both'): 
    print('python backtest.py')
    print('python trade.py')
'''