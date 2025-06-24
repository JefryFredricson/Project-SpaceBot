import requests
import os

req = requests.get("https://www.youtube.com/embed/rQcKIN9vj3U?rel=0")

print(req.status_code)
print(req.headers['content-type'])
if 'image' in req.headers['content-type']:
    with open("test.jpg", "wb") as file:
        file.write(req.content)
        
import yt_dlp

def download(link, name='%(title)s'):
    ydl_opts = {
        'format': 'bestvideo+bestaudio/best', #берем самое лучшее качество видео и фото
        'outtmpl': '{}.%(ext)s'.format(name), #наше выбраное имя, если его не было, то стандартное - название видео на самом сайте
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(link, download=True)
        downloaded_file_path = ydl.prepare_filename(info_dict)
    print(f"Видео {downloaded_file_path} успешно загружено!")
    return downloaded_file_path


print(download('https://www.youtube.com/watch?v=uHgt8giw1LY', 'Привет!'))