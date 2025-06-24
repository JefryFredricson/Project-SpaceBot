import os
import csv
import re
import json

import requests


def is_date(date_str):
    """
    Проверяет, что date_str соответствует шаблону YYYY-MM-DD и
    находится в диапазоне от 1900-01-01 до 9999-12-31.
    
    Возвращает кортеж (day, month, year), если валидно, иначе False.
    """
    if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", date_str):
        return False
    
    day, month, year = map(int, date_str.split('-'))
    if (day, month, year) > (9999, 12, 31):
        return False
    if (day, month, year) < (1900, 1, 1):
        return False
    return (day, month, year)

class Media:
    """
    Класс для работы с локальным кешем APOD-картинок и их загрузкой.

    Атрибуты:
        filename (str): путь к CSV-файлу с уже загруженными картинками.
        filepath (str): директория для сохранения новых картинок.
        NASA_API_KEY (str): ключ для доступа к NASA APOD API.
    """
    filename: str
    filepath: str
    
    def __init__(self, filename:str, filepath:str, bot, NASA_API_KEY:str):
        """
        Инициализирует параметры кеша и путей для Media.
        """
        self.filename = os.path.join(os.path.dirname(__file__), filename)
        self.filepath = filepath
        self.NASA_API_KEY = 'DEMO_KEY'
    
    def get_file(self, date):
        """
        Возвращает данные по картинке за дату из кеша или загружает её из NASA.

        Args:
            date (tuple): кортеж (day, month, year).

        Returns:
            [url, explanation] или None, если что-то пошло не так.
        """
        status = 'NONE'
        info = None
        with open(self.filename, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                print(date, row['DATE'])
                if row['DATE'] == date:
                    return [row['LINK'], row['TEXT']]
            else:
                status = 'NF'               # no file
                info = date

        if status == 'NF':
            r = requests.get(
                f"https://api.nasa.gov/planetary/apod?api_key={self.NASA_API_KEY}"
                f"&date={date[2]}-{date[1]}-{date[0]}&thumbs=False"
            )
            if r.status_code != 200:
                print(r.status_code, r.headers)
                return None
            
            nasa = json.loads(r.content)
            print(nasa)
            if nasa['media_type'] == 'image':
                if "hdurl" in nasa:
                    r = requests.get(nasa['hdurl'])
                else:
                    r = requests.get(nasa['url'])
                    
                if r.status_code != 200:
                    return None
                
                with open(os.path.join(self.filepath,), 'wb') as file:
                    file.write(r.content)
                
                with open(self.filename, 'a', encoding='utf-8') as file:
                    writer = csv.DictWriter(file, fieldnames=['ID', 'NAME', 'LINK', 'TEXT'])
                    writer.writerow({
                        'ID': date,
                        'NAME': date,
                        'LINK': nasa['hdurl'],
                        'TEXT': nasa['explanation'],
                    })
                
                return [nasa['url'], nasa['explanation']]

def photo_sender(bot, message):
     """
    Обрабатывает сообщение с датой и отправляет пользователю
    картинку NASA APOD за указанную дату.

    Args:
        bot (TeleBot): объект Telegram-бота.
        message (Message): входящее сообщение, text которого — дата YYYY-MM-DD.
    """
    date = is_date(message.text)
    r = requests.get(
        f"https://api.nasa.gov/planetary/apod?"
        f"api_key={NASA_API_KEY}&"
        f"date={date[2]}-{date[1]}-{date[0]}&thumbs=False"
    )
    if r.status_code != 200:
        # Ошибка сети или неверный API-ключ — выводим код и выходим
        print(r.status_code, r.headers)
        bot.reply_to(message, "Что-то пошло не так, возможно в другой раз")
        return
    
    nasa = json.loads(r.content)
    print(nasa)
    if nasa['media_type'] == 'image':
        if "hdurl" in nasa:
            r = requests.get(nasa['hdurl'])
        else:
            r = requests.get(nasa['url'])
            
        if r.status_code != 200:
            bot.reply_to(message, "Это не моя вина, сервис не вернул фото")
            return
    
        bot.reply_to(message, f"Лови фотоку {date[0]}-{date[1]}-{date[2]}")
        bot.send_photo(message.chat.id, photo=nasa['url'], caption=nasa['explanation'])
        
    elif nasa['media_type'] == 'video':
        pass
    else:
        bot.reply_to(message, "Это не фото, я сожалею")
        print(f"media_type {nasa['media_type']} \t {nasa['url']}")
        return
