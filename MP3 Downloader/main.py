from __future__ import unicode_literals

import shutil
import os
import eyed3
import ffmpeg
import youtube_dl

def run():
    # Setting download parameters
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '320',
        }],
    }

    while True:
        main_cmd = input('Continue? [y/n] ')
        if main_cmd.lower() == 'n':
            print('Exiting program...')
            return
        elif main_cmd.lower() == 'y':
            pass
        else:
            print('CommandError: Invalid Input Command!')
            return

        # Collecting download url and file name from user
        url_input = input('YouTube URL: ')
        file_name = input('File Name [<artist> - <title>]: ') + '.mp3'

        artist = file_name.split(' - ')[0]
        title = file_name.split(' - ')[1][:-4]

        # Download mp3 file
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url_input])

        # Rename downloaded mp3 file
        downloaded_name = [name for name in os.listdir() if name.endswith('.mp3')][0]

        src = os.path.join(os.getcwd(), downloaded_name)
        dest = os.path.join(os.getcwd(), file_name)

        if file_name in os.listdir():
            os.remove(dest)
            os.rename(src, dest)
        else:
            os.rename(src, dest)

        # Update mp3 ID3 tags
        audio = eyed3.load(file_name)

        audio.tag.artist = artist
        audio.tag.title = title

        audio.tag.save()

        # Move downloaded mp3 file to destination folder
        shutil.move(dest, os.path.join(r'C:\Users\Kai Jing\Music\Songs\normalized\00 normalize', file_name))

if __name__ == '__main__':
    run()