#notice.py

#!/usr/bin/env python3
# coding: utf-8

import os
import telegram
from telegram.ext import Updater, CommandHandler

telegram_bot_token='454164830:AAGYDxHizoRpQUbFsZEaAFZOmfR_14RqPBk'
telegram_trade_chat_id='-292468956'
telegram_monitoring_chat_id='-313228619'
telegram_warning_chat_id='-307631184'

class Telegrambot:
    '''Send notifications trough telegram to especific chats, 
    using python-telegram-bot wrapp API. 
    '''
    
    def __init__(self,message):
        self.fail='Telegram fail because: '
        self.message=message
        self.bot=telegram.Bot(token=telegram_bot_token)

    def trade(self):
        '''Notifications to trade chat.'''
        try:
            self.bot.send_message(chat_id=telegram_trade_chat_id, text=self.message)
            return 'done'
        except Exception as e:
            print(self.fail + str(e))
            return 'undone'
        
    def monitoring(self):
        '''Notifications to monitoring chat.'''
        try:
            self.bot.send_message(chat_id=telegram_monitoring_chat_id, text=self.message)
        except Exception as e:
            print(self.fail + str(e))
    
    def warning(self):
        '''Notifications to warning chat.'''
        try:
            self.bot.send_message(chat_id=telegram_warning_chat_id, text=self.message)
        except Exception as e:
            print(self.fail + str(e))