from saver import Saver
from extender import VideoExtender
from authenticator import Authenticate
from poster import YouTubePoster
import os

def delete_everything(token=True, code=True):
    global extender
    os.remove('playlist.txt')
    #os.remove(extender.video.default_filename)
    os.remove('thumbnail.jpg')
    os.remove('video_information.json')
    if token: os.remove('token.json')
    if code: os.remove('code.json')
    try:
        os.remove('output.mp4')
    except:
        #Sometimes the upload didn't really end at all
        pass



if __name__ == '__main__':
    try:
        delete_everything()
    except:
        pass
    url = input("Put a url:  ").strip()

    Saver(url).save_information()
    extender = VideoExtender(url)
    extender.extend()
    if input("Do you already have the upload code (Y/N):  ").lower().startswith("N"):

        auth = Authenticate('client_secret.json', ['https://www.googleapis.com/auth/youtube.upload'])
        auth.start()
        auth.run('localhost', 5000)
        input("Got credentials? >  ")
        auth.exchange_code()
    
    poster = YouTubePoster('client_secret.json', 'token.json')
    poster.build()
    status, response = poster.post()
    print("http://youtu.be/" + response['id'])
    delete_everything()
