import subprocess
from pytube import YouTube
import pickle
import json


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

        yt = YouTube(self.url)
        video = yt.streams.first()
        video.download()
        self.yt = yt
        self.video = video

    @staticmethod
    def repeat_n_times(seconds):

        n = 3600 // seconds + bool(3600 % seconds)
        return n

    def generate_playlist(self):
        times = VideoExtender.repeat_n_times(int(self.yt.length))

        with open("playlist.txt", "w") as playlist:
            [playlist.write(f"file '{self.video.default_filename}'\n") for _ in range(times)]

    def _extend(self):

        subprocess.run(['ffmpeg', '-f', 'concat', '-safe', '0', '-i', 'playlist.txt', '-c', 'copy', 'output.mp4'])

    def extend(self):
        self.download()
        self.generate_playlist()
        self._extend()


if __name__ == '__main__':
    video = VideoExtender(url="https://www.youtube.com/watch?v=9RTaIpVuTqE")
    video.extend()

