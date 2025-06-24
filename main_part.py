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

API_KEY_NASA = 'YOUR_NASA_API_KEY'
API_KEY_TG = 'YOUR_TG_KEY'
load_dotenv()
NASA_API_KEY = os.getenv(API_KEY_NASA)
bot = TeleBot(API_KEY_TG)
users = Users('users.csv')

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.from_user.id, "Привет, я SpaceBot! Моя задача заключается в том, чтобы показывать любителям космоса лучшие фотографии с ним связанные")

@bot.message_handler(commands=['help'])
def help(message):
    bot.send_message(message.from_user.id, "Ввода в команды subscription, subscribe, unsubscribe не требуется. Для команды apod требуется параметр даты в формате YYYY-MM-DD(например, 2025-10-05)")

@bot.message_handler(commands=['subscription'])
def subscription(message):
    status = users.isUser(message.from_user.id)
    sub_status = users.getStatus(message.from_user.id)
    if status and sub_status:
        bot.send_message(message.from_user.id, "Вы подписаны на ежедневную рассылку")
    else:
        bot.send_message(message.from_user.id, "Вы не подписаны на ежедневную рассылку")

@bot.message_handler(commands=['subscribe'])
def subscription(message):
    status = users.isUser(message.from_user.id)
    sub_status = users.getStatus(message.from_user.id)
    if status and sub_status:
        bot.send_message(message.from_user.id, "Вы уже подписаны на ежедневную рассылку. Подписываться еще раз необязательно:)")
    else:
        if not status:
            users.addUser(message.from_user)
        else:
            users.returnUser(message.from_user.id)
        bot.send_message(message.from_user.id, "Вы подписались на ежедневную рассылку")



@bot.message_handler(commands=['unsubscribe'])
def subscription(message):
    status = users.isUser(message.from_user.id)
    sub_status = users.getStatus(message.from_user.id)
    if not(sub_status) or not(status):
        bot.send_message(message.from_user.id, "Вы уже отписались или еще не подписывались")
    else:
        users.delUser(message.from_user.id)
        bot.send_message(message.from_user.id, "Вы отписались от ежедневной рассылки")

def newsletter():
    users = users.getUsers()
    current_date = datetime.date.today().isoformat()
    picture = Media.getFile(date=tuple(map(int, current_date.split('-')))[::-1])
    for user in users:
        bot.send_photo(user, photo=picture[0], caption=picture[1])

def checktime():
    schedule.every(24).hours.do(newsletter)
    while True:
        schedule.run_pending()
        time.sleep(1)


@bot.message_handler(commands=['apod'])
def apod_by_date(message):
    parts = message.text.split(maxsplit=1)
    if len(parts) != 2 or not isDate(parts[1]):
        return bot.reply_to(
            message,
            "Неверный формат. Используй:\n/apod YYYY-MM-DD"
        )

    date_str = parts[1]
    media = Media('media.csv', 'images', bot, NASA_API_KEY)
    result = media.getFile(tuple(map(int, date_str.split('-')))[::-1])

    if not result:
        return bot.reply_to(message, "Не удалось получить картинку за эту дату.")

    bot.send_photo(message.chat.id, photo=result[0], caption=result[1])




thread=threading.Thread()
thread.start()
bot.infinity_polling()
