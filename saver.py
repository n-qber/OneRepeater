import json
import requests
import pytube.extract
import urllib.parse


class Saver:
    def __init__(self, url):
        self.url = url
        self.main_url = "https://www.googleapis.com/youtube/v3/videos?"
        self.title = ""
        self.description = ""
        self.thumbnail = ""
        self.tags = []
        self.categoryId = 0
        self.apiKey = self.load_api_key()

    def load_api_key(self):
        """
        Loads the api key, to be used for getting the original video data
        (youtube-data-api-v3-key)
        :return: the api key _yay_
        """
        with open("credentials.json", "r") as credentials_json:
            apiKey = json.load(credentials_json)['youtube-data-api-v3-key']
        return apiKey

    def download_information(self, query) -> dict:
        """
        Downloads the information by a link with the information passed by self.load_information
        :param query:
        :return: the information _yay_
        """
        url = self.main_url + urllib.parse.urlencode(query)
        response = requests.get(url)
        return json.loads(response.content)

    def load_information(self) -> dict:
        """
        Downloads the information and organizes it in a dictionary
        :return:
        """
        response = self.download_information({"id": pytube.extract.video_id(self.url), "part": "snippet", "key": self.apiKey})
        snippet = response["items"][0]["snippet"]

        video_information = {
            "title": snippet["title"],
            "description": snippet["description"],
            "thumbnail": snippet["thumbnails"]["default"]["url"],
            "tags": snippet["tags"],
            "categoryId": snippet["categoryId"]
        }
        return video_information

    def save_information(self):
        """
        Saves the original video info and saves in video_information.json
        :return: it doesn't muahahaha
        """
        with open("video_information.json", "w") as video_information_json:
            video_information = self.load_information()
            video_information_json.write(json.dumps(video_information))


if __name__ == '__main__':
    saver = Saver("https://www.youtube.com/watch?v=ekbi5vKSGy4")
    saver.save_information()
