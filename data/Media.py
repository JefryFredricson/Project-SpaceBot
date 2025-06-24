import os
import csv, re, json
import requests
from telebot.types import InputFile

def isDate(date_str):
    if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", date_str):
        return False
    
    day, month, year = map(int, date_str.split('-'))
    if (day, month, year) > (9999, 12, 31):
        return False
    if (day, month, year) < (1900, 1, 1):
        return False
    return (day, month, year)

class Media:
    filename: str
    filepath: str
    
    def __init__(self, filename:str, filepath:str, bot, NASA_API_KEY:str):
        self.filename = os.path.join(os.path.dirname(__file__), filename)
        self.filepath = filepath
        self.NASA_API_KEY = 'DEMO_KEY'
    
    def getFile(self, date):
        type = 'NONE'
        info = None
        with open(self.filename, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                print(date, row['DATE'])
                if row['DATE'] == date:
                    return [row['LINK'], row['TEXT']]
            else:
                type = 'NF'               # no file
                info = date

        if type == 'NF':
            r = requests.get(f"https://api.nasa.gov/planetary/apod?api_key={self.NASA_API_KEY}&date={date[2]}-{date[1]}-{date[0]}&thumbs=False")
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
                
                with open(os.path.join(self.filepath, ), 'wb') as file:
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

                    
        
        
def photoSender(bot, message):
    date = isDate(message.text)
    r = requests.get(f"https://api.nasa.gov/planetary/apod?api_key={TPCZTjkVRKllaLRbqTH8Qtq2mpHTiGAg0MVXj6Fb}&date={date[2]}-{date[1]}-{date[0]}&thumbs=False")
    if r.status_code != 200:
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
        bot.send_photo(message.chat.id, photo=nasa['url'], caption = nasa['explanation'])
        
    elif nasa['media_type'] == 'video':
        pass
    else:
        bot.reply_to(message, "Это не фото, я сожалею")
        print(f"media_type {nasa['media_type']} \t {nasa['url']}")
        return
