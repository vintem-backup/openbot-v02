#notice.py

#!/usr/bin/env python3
# coding: utf-8

import os
import telegram
from telegram.ext import Updater, CommandHandler

class Telegrambot:
    '''Send notifications trough telegram to especific chats, 
    using python-telegram-bot wrapp API. 
    '''
    
    def __init__(self,message):
        self.fail='Telegram fail because: '
        self.message=message
        self.bot=telegram.Bot(token=os.environ['telegram_bot_token'])

    def trade(self):
        '''Notifications to trade chat.'''
        try:
            self.bot.send_message(chat_id=os.environ['telegram_trade_chat_id'], text=self.message)
        except Exception as e:
            print(self.fail + str(e))

    def monitoring(self):
        '''Notifications to monitoring chat.'''
        try:
            self.bot.send_message(chat_id=os.environ['telegram_monitoring_chat_id'], text=self.message)
        except Exception as e:
            print(self.fail + str(e))
    
    def warning(self):
        '''Notifications to warning chat.'''
        try:
            self.bot.send_message(chat_id=os.environ['telegram_warning_chat_id'], text=self.message)
        except Exception as e:
            print(self.fail + str(e))