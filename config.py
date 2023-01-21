import telebot 
import logging 
from decouple import config

VERSION = 0.1
TELEGRAM_TOKEN = config('TELEGRAM_TOKEN') 
bot = telebot.TeleBot(TELEGRAM_TOKEN) 
telebot.logger.setLevel(logging.INFO)