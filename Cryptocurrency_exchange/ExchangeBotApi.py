import telegram
# from telegram.error import TelegramError as err
from googletrans import Translator


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
        self.token = '606817182:AAFH_eGd0xJOf4rt9iudrwkzHjS5gUdP2Hg' ## Exchange Bot
        TelegramApi.__init__(self, self.token)

    def sendPlain(self, msg):
        #self.sendMessage(msg)
        try:
            self.sendMessage(msg)
        except:
            print('Failed to send message')
        else:
            print('Message sent!')


# Google Tranlator
class GoogleTrans:
    def __init__(self):
        self.translator = Translator()

    def detectLang(self, text):
        self.text = text
        return str(self.translator.detect(text).lang)

    def translate(self, text):
        self.text = text
        for lang in ['ja', 'ko']:   # 원문 -> 일어 -> 한국어
            self.translated = self.translator.translate(self.text, dest=lang)
        return str(self.translated.text)
