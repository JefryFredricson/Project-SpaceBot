import os
from dotenv import load_dotenv
import json
import threading
import datetime
import schedule
import time

import asyncio
from telebot import TeleBot, types

from data.users import Users
from data.Media import Media, isDate, photoSender

import requests
import re

API_KEY_NASA = 'Your_API_KEY'
API_KEY_TG = 'Your_API_KEY'
load_dotenv()
NASA_API_KEY = os.getenv(API_KEY_NASA)
bot = TeleBot(API_KEY_TG)
users = Users('users.csv')

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.from_user.id, "Привет, я SpaceBot! Моя задача заключается в том, чтобы показывать любителям космоса лучшие фотографии с ним связанные")

@bot.message_handler(commands=['subscription'])
def subscription(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    status = users.isUser(message.from_user.id)
    if status:
        bot.send_message(message.from_user.id, "Вы подписаны на ежедневную рассылку")
    else:
        bot.send_message(message.from_user.id, "Вы не подписаны на ежедневную рассылку")

@bot.message_handler(commands=['subscribe'])
def subscription(message):
    status = users.isUser(message.from_user.id)
    if status:
        bot.send_message(message.from_user.id, "Вы уже подписаны на ежедневную рассылку. Подписываться еще раз необязательно:)")
    else:
        users.addUser(message.from_user.id)
        bot.send_message(message.from_user.id, "Вы подписались на ежедневную рассылку")


@bot.message_handler(commands=['unsubscribe'])
def subscription(message):
    status = users.isUser(message.from_user.id)
    if not(status):
        bot.send_message(message.from_user.id, "Вы уже отписались или еще не подписывались")
    else:
        users.delUser(message.from_user.id)
        bot.send_message(message.from_user.id, "Вы отписались от ежедневной рассылку")

@bot.message_handler(commands=['like'])
def subscription(message):
    status = users.isUser(message.from_user.id)
    if not(status):
        bot.send_message(message.from_user.id, "Вы уже отписались или еще не подписывались")
    else:
        users.delUser(message.from_user.id)
        bot.send_message(message.from_user.id, "Вы отписались от ежедневной рассылку")

def newsletter():
    users = users.getUsers()
    current_date = datetime.date.today().isoformat()
    picture = Media.getFile(date=current_date)
    for user in users:
        sender_p = threading.Thread(target=photoSender, args=(bot, user.id,))
        sender_p.start()

def checktime():
    schedule.every(24).hours.do(newsletter)
    while True:
        schedule.run_pending()
        time.sleep(3600)


thread=threading.Thread(target=newsletter())
thread.start()
bot.infinity_polling()