#notice.py

#!/usr/bin/env python3
# coding: utf-8

import os
import telegram
from telegram.ext import Updater, CommandHandler

class telegram_bot:
    
    def __init__(self,message):
        self.fail='Telegram fail'
        self.message=message
        self.bot = telegram.Bot(token=os.environ['telegram_bot_token'])
        pass

    def trade(self):
        try:
            self.bot.send_message(chat_id=os.environ['telegram_trade_chat_id'], text=self.message)
        except:
            print(self.fail)
        pass

    def control(self):
        try:
            self.bot.send_message(chat_id=os.environ['telegram_control_chat_id'], text=self.message)
        except:
            print(self.fail)
        pass
    
    def warning(self):
        try:
            self.bot.send_message(chat_id=os.environ['telegram_warning_chat_id'], text=self.message)
        except:
            print(self.fail)
        pass