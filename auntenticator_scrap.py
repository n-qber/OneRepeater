"""
THIS IS A SCRAP I CREATED FOR UNDERSTANDING OAUTH2
I DONT KNOW WHY I AM PUSHING IT BUT OK IDC
"""



import os
import flask
import google.oauth2.credentials
import google_auth_oauthlib.flow
from apiclient.http import MediaFileUpload
import urllib.parse
import json
from googleapiclient.discovery import build

# Use the client_secret.json file to identify the application requesting
# authorization. The client ID (from that file) and access scopes are required.
flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
    'client_secret.json',
    ['https://www.googleapis.com/auth/youtube.upload'])

# Indicate where the API server will redirect the user after the user completes
# the authorization flow. The redirect URI is required. The value must exactly
# match one of the authorized redirect URIs for the OAuth 2.0 client, which you
# configured in the API Console. If this value doesn't match an authorized URI,
# you will get a 'redirect_uri_mismatch' error.
flow.redirect_uri = "http://localhost:5000/oauth2callback"

# Generate URL for request to Google's OAuth 2.0 server.
# Use kwargs to set optional request parameters.
authorization_url, state = flow.authorization_url(
    # Enable offline access so that you can refresh an access token without
    # re-prompting the user for permission. Recommended for web server apps.
    access_type='offline',
    # Enable incremental authorization. Recommended as a best practice.
    include_granted_scopes='true')


app = flask.Flask(__name__)

@app.route('/')
def hello():
    return flask.redirect(authorization_url)

@app.route('/oauth2callback')
def oauth2callback():
    with open("token.json", "w") as token_json:
        token_json.write(json.dumps(flask.request.args.to_dict()))

    y = build('youtube', 'v3', credentials=flask.request.args.to_dict())

    body = dict(
        snippet=dict(
            title="TestTitle",
            description="SuperDescription",
            tags=["yay"],
            categoryId="22"
        ),
        status=dict(
            privacyStatus="unlisted"
        )
    )

    print(body.keys())
    inserter = y.videos().insert(part=','.join(body.keys()), body=body, media_body=MediaFileUpload("output.mp4", chunksize=1024**2, resumable=True))

    response = None
    while response is None:
        status, response = inserter.next_chunk()

    print(response["id"])
    print(response)

    return b""

if __name__ == '__main__':
    # Bind to PORT if defined, otherwise default to 5000.
    port = 5000
    app.run(host='localhost', port=port)