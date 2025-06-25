import os
import requests

import yt_dlp

# Make a request to check if the video file is an image
req = requests.get("https://www.youtube.com/embed/rQcKIN9vj3U?rel=0")
print(req.status_code)
print(req.headers['content-type'])

# Check if the response is an image
if 'image' in req.headers['content-type']:
    with open("test.jpg", "wb") as file:
        file.write(req.content)
        
def download(link, name='%(title)s'):
    """
    Download a video from the provided link.

    Arguments:
    link -- URL of the video
    name -- desired name for the downloaded file
    """
    ydl_opts = {
        'format': 'bestvideo+bestaudio/best', # Get the best quality video and audio
        'outtmpl': '{}.%(ext)s'.format(name), # The name chosen for the file, if not provided, will default to the video's title on the website
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(link, download=True)
        downloaded_file_path = ydl.prepare_filename(info_dict)
        
    print(f"Видео {downloaded_file_path} успешно загружено!")
    return downloaded_file_path

# Example download call
print(download('https://www.youtube.com/watch?v=uHgt8giw1LY', 'Привет!'))
