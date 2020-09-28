# -*- coding: utf-8 -*-

import telebot
import requests
import time
from telebot import apihelper

class Bot:
    def __init__(self):
        self.bot_token =
        self.channel =
        self.bot = telebot.TeleBot(self.bot_token)
        self.proxy_param = apihelper.proxy =
        self.delay = 0

    def send_message(self, message):
        time.sleep(self.delay)
        requests.get(f'https://api.telegram.org/bot{self.bot_token}/sendMessage', params=dict(
            chat_id=self.channel,
            text=message,
        ))


proxy_1 = Bot()

proxy_2 = Bot()
proxy_2.proxy_param = apihelper.proxy = {'https': 'socks5://userproxy:password@proxy_address:port'}
proxy_2.delay = 1

proxy_3 = Bot()
proxy_3.proxy_param = apihelper.proxy = {'https': 'https://88.204.154.155:8080'}
proxy_3.delay = 1

def send_message(data):
    try:
        proxy_1.send_message(data)
    except:
        try:
            proxy_2.send_message(data)
        except:
            proxy_3.send_message(data)


