import subprocess
from youtube_dl import YoutubeDL
import pickle
import json
import os
import shutil


class VideoExtender:
    def __init__(self, url: str = None):

        if url is not None:
            self.url = url
        else:
            self.url = None

    def download(self, url: str = None):

        if url is not None:
            self.url = url

        assert (self.url is not None), "You may have a url to download the video"

        ydl_opts = {
            'format': 'bestvideo+bestaudio/best',
            'outtmpl': 'video/%(title)s.%(ext)s'
        }

        ydl = YoutubeDL(params=ydl_opts)
        self.extracted_info = ydl.extract_info(self.url, download=True)
        self.ydl = ydl

    @staticmethod
    def repeat_n_times(seconds):

        n = 3600 // seconds + bool(3600 % seconds)
        return n

    @property
    def file_name(self):
        try:
            file_name = os.listdir('video')[0]
            if "'" in file_name:
                new = file_name.replace("'", '_')
                os.renames('video/' + file_name, 'video/' + new)
            else:
                new = file_name
            if not new.endswith('mp4'):
                subprocess.run(['ffmpeg', '-i', 'video/' + new, 'video/' + new + ".mp4"])
            return new + ".mp4"
        except FileNotFoundError:
            raise (FileNotFoundError, "The video was not downloaded in the correct path")

    def generate_playlist(self):
        times = VideoExtender.repeat_n_times(self.extracted_info["duration"])
        file_name = self.file_name
        with open("video/playlist.txt", "w") as playlist:
            [playlist.write(f"file '{file_name}'\n") for _ in range(times)]

    def _extend(self):

        subprocess.run(['ffmpeg', '-f', 'concat', '-safe', '0', '-i', 'video/playlist.txt', '-c', 'copy', 'output.mp4'])

    def end(self):
        shutil.rmtree('video', ignore_errors=True)

    def extend(self):
        self.download()
        self.generate_playlist()
        self._extend()
        self.end()


if __name__ == '__main__':
    video = VideoExtender(url="https://www.youtube.com/watch?v=Gus4dnQuiGk")
    video.extend()

