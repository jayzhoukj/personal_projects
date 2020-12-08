from __future__ import unicode_literals

import eyed3
import ffmpeg
import os
import pyautogui as pag
import requests
import shutil
import time
import youtube_dl

class mp3downloader:

    def __init__(self):

        self.original = []
        self.tempName = []
        self.root_dir = os.getcwd()
        self.dest_dir = r'C:\Users\Kai Jing\Music\Songs\normalized\00 normalize'

        # Download parameters
        self.ydl_opts = {
            'format': 'bestaudio/best',
            'postprocessors': [
                {
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '320',
                },
            ],
        }

    def download(self):

        while True:
            main_cmd = input('Continue? [y/n] ')
            if main_cmd.strip().lower() == 'n':
                print('Finished downloading...')
                return
            elif main_cmd.strip().lower() == 'y':
                pass
            else:
                print('CommandError: Invalid Input Command!')
                return

            # Collecting download url and file name from user
            url_input = input('YouTube URL: ')
            file_name = input('File Name [<artist> - <title>]: ') + '.mp3'

            # Clean youtube url
            if '&' in url_input:
                url_input = url_input.split('&')[0]

            artist = file_name.split(' - ')[0]
            title = file_name.split(' - ')[1][:-4]

            # Download mp3 file
            with youtube_dl.YoutubeDL(self.ydl_opts) as ydl:
                ydl.download([url_input])

            # Rename downloaded mp3 file
            youtube_uri = url_input.split('=')[-1]
            downloaded_name = [name for name in os.listdir() if youtube_uri in name][0]

            src = os.path.join(self.root_dir, downloaded_name)
            dest = os.path.join(self.root_dir, file_name)

            if file_name in os.listdir():
                os.remove(dest)
                os.rename(src, dest)
            else:
                os.rename(src, dest)

            # Update mp3 ID3 tags
            audio = eyed3.load(file_name)

            audio.tag.artist = artist
            audio.tag.title = title

            url = r'https://i3.ytimg.com/vi/' + youtube_uri + '/maxresdefault.jpg'
            response = requests.get(url)
            cover_art = response.content

            audio.tag.images.set(3,
                                 img_data=cover_art,
                                 mime_type='image/jpeg')

            audio.tag.save()

    def normalize(self):

        self.original = [file for file in os.listdir() if file.endswith('.mp3')]
        self.tempName = [str(i)+'.mp3' for i in range(len(self.original))]

        # Map from chinese to english
        for i, file in enumerate(self.original):
            src = os.path.join(self.root_dir, file)
            dest = os.path.join(self.root_dir, self.tempName[i])

            os.rename(src, dest)

        for i, name in enumerate(self.tempName):
            pag.click(20, 1060)
            time.sleep(1)

            pag.typewrite([char for char in 'mp3gain'] + ['enter'], interval=0.1)
            time.sleep(2.5)

            # Add file
            pag.click(40, 80)
            time.sleep(1)

            # Select file
            if i == 0:
                pag.click(500, 95)
                pag.typewrite([char for char in self.root_dir] + ['enter'], interval=0.05)
                time.sleep(.5)

            pag.click(330, 530)
            pag.typewrite([char for char in name] + ['enter'], interval=0.1)
            time.sleep(.5)

            # Analyze track
            pag.click(210, 80)
            time.sleep(7)

            # Track gain
            pag.click(310, 80)
            time.sleep(5)

            # Exit program
            pag.click(1895, 10)

        # Reverse map from english to chinese
        for i, file in enumerate(self.tempName):
            src = os.path.join(self.root_dir, file)
            dest = os.path.join(self.root_dir, self.original[i])

            os.rename(src, dest)

    def moveToDest(self):

        for file in self.original:
            src = os.path.join(self.root_dir, file)
            dest = os.path.join(self.dest_dir, file)

            shutil.move(src, dest)

if __name__ == '__main__':

    musicDownloader = mp3downloader()

    musicDownloader.download()
    musicDownloader.normalize()
    musicDownloader.moveToDest()