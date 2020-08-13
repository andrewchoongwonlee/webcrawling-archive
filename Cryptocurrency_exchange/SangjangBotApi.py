import telegram
from googletrans import Translator
import time

# Telegram
class TelegramApi():
    def __init__(self, token):
        self.core = telegram.Bot(token)
        # telegram self id
        self.id = 505440198
        #self.id = '@choong_test'

    def sendMessage(self, text):
        self.core.sendMessage(chat_id = self.id, text=text, parse_mode='HTML')

class TelegramBot(TelegramApi):
    def __init__(self):
        # telegram bot token
        self.token = '611537205:AAHHaF4mXDfmlZaj3zvALC0hXEeKFWypQgU' ## Sangjang Bot
        TelegramApi.__init__(self, self.token)

    def sendPlain(self, msg):
        #self.sendMessage(msg)
        try:
            self.sendMessage(msg)
        except:
            print('Failed to send message')
        else:
            print('Message sent!')
