import json
from googleapiclient.discovery import build
from apiclient.http import MediaFileUpload
from oauth2client.client import flow_from_clientsecrets, OAuth2Credentials
from oauth2client.tools import argparser, run_flow
from oauth2client.file import Storage
import httplib2
import urllib.request as ur

#  Poster is for posting, it's not a paper ok haha lol


class YouTubePoster:
    def __init__(self, client_secret, token_json, privacyStatus="unlisted"):
        self.builder = ""
        self.inserter = ""
        self.client_secret = client_secret
        self.token_json = token_json
        self.privacyStatus = privacyStatus

    def body(self, **kwargs):
        """
        To send the video
        :param kwargs: the information of the looped version (which comes from the original video)
        :return: a dict object configured for the posting video part
        """

        body = dict(
            snippet=dict(
                title="",
                description="",
                tags="",
                categoryId=""
            ),
            status=dict(
                privacyStatus=""
            )
        )

        for name, value in kwargs.items():
            if name in body["snippet"].keys():
                body["snippet"][name] = value
            if name == "privacyStatus":
                body["status"][name] = value

        return body

    def get_config(self):
        """
        Load the original video (the one which is being looped) information from video_information.json
        I Don't remember why i didn't customize it's name bu ti think it is bc of different classes using
        the same file
        :return: the config loaded in a dictionary
        """
        with open("video_information.json", "r") as info:
            config = json.load(info)
            config["privacyStatus"] = self.privacyStatus
        return config

    def build(self, filename="output.mp4", token_uri="https://accounts.google.com/o/oauth2/token"):
        """
        To post the video we need
        :param filename: the filename of the 1 hour video
        :param token_uri: the url to exchange the token for an access token (if you don't know what it is, just don't change it)
        """
        with open(self.client_secret, "r") as info:
            client_secrets = json.load(info)
        with open(self.token_json, "r") as info:
            token_secrets = json.load(info)

        credentials = OAuth2Credentials(
                token_secrets["access_token"], client_secrets["web"]["client_id"], client_secrets["web"]["client_secret"],
                token_secrets["refresh_token"], token_secrets["expires_in"], token_uri, "", scopes=token_secrets["scope"])
        self.builder = build('youtube', 'v3', http=credentials.authorize(httplib2.Http()))
        body = self.body(**self.get_config())

        self.inserter = self.builder.videos().insert(part=','.join(body.keys()), body=body,
                                     media_body=MediaFileUpload(filename, chunksize=1024 ** 2 * 10, resumable=True))

    def post(self):
        """
        Post the video
        :returns:
            A status and the response, wich has the information about the posted video
        """
        response = None
        while response is None:
            status, response = self.inserter.next_chunk()

        if hasattr(response, 'id'):
            self.id = response['id']

        return status, response

    def get_thumb_link(self):
        return self.get_config()["thumbnail"]

    def download_thumbnail(self):
        link = self.get_thumb_link()
        ur.urlretrieve(link, 'thumbnail.jpg')

    def post_thumbnail(self):

        self.download_thumbnail()

        self.inserter.thumbnails().set(
            videoId=self.id,
            media_body="thumbnail.jpg"
        ).execute()


if __name__ == '__main__':
    YouTubePoster('client_secret.json', 'token.json').download_thumbnail()
    """
    poster = YouTubePoster('client_secret.json', 'token.json')
    poster.build()
    status, response = poster.post()
    """
