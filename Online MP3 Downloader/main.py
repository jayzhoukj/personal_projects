from __future__ import unicode_literals
import os
import ffmpeg
import youtube_dl

ydl_opts = {
    'format': 'bestaudio/best',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '320',
    }],
}

url_input = input('YouTube URL: ')
file_name = input('File Name: ')

with youtube_dl.YoutubeDL(ydl_opts) as ydl:
    ydl.download([url_input])

