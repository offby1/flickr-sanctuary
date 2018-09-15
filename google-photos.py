"""

So ... I'd like to learn how to upload photos to Google Photos.
Sounds like it should be simple, right?  Noooo.

The only Google Photos API I know of is at
https://developers.google.com/photos/library/guides/overview; I
haven't looked at it yet."""

import logging
import requests
import secrets

logging.basicConfig(level=logging.DEBUG)


# from https://developers.google.com/identity/protocols/OAuth2InstalledApp
# This returns a Google-branded web page that asks the user to log in
def get_token(client_id="661666866149-42r2bldb8karc5bv5vltj0suis2fm4up.apps.googleusercontent.com"):
    response = requests.post(
        'https://accounts.google.com/o/oauth2/v2/auth',
        data={
            'client_id': client_id,
            'code_challenge': secrets.token_hex(nbytes=64),
            'code_challenge_method': 'plain',
            'redirect_uri': 'urn:ietf:wg:oauth:2.0:oob',
            'response_type': 'code',
            'scope': ' '.join(['https://www.googleapis.com/auth/photoslibrary', 'https://www.googleapis.com/auth/photoslibrary.readonly.appcreateddata', 'https://www.googleapis.com/auth/photoslibrary.sharing']),
        })
    print(response.text)
    return response
