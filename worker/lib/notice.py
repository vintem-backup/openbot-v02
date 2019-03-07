#notice.py

#!/usr/bin/env python3
# coding: utf-8

import os
import telegram
from telegram.ext import Updater, CommandHandler

class telegram_bot:
    
    def __init__(self,tag,message):
        self.tag=tag
        self.message=message

        if  (self.tag == 'trade'):
            self.ident = os.environ['telegram_trade_chat_id']
       
        elif  (self.tag == 'control'):
            self.ident = os.environ['telegram_control_chat_id']

        elif  (self.tag == 'warning'):
            self.ident = os.environ['telegram_warning_chat_id']
        
        else:
            print('Not a valid tag')
        
        pass
    
    def send(self):
        bot = telegram.Bot(token=os.environ['telegram_bot_token'])
        
        try:
            bot.send_message(chat_id=self.ident, text=self.message)
        
        except:
            mess = 'Falha no telegram'
            #mail_sender2(mess)
            print (mess)

        pass