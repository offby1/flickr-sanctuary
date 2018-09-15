"""

So ... I'd like to learn how to upload photos to Google Photos.
Sounds like it should be simple, right?  Noooo.

The only Google Photos API I know of is at
https://developers.google.com/photos/library/guides/overview; I
haven't looked at it yet."""

import requests

# This will probably fail due to lack of auth.
print(requests.get('https://photoslibrary.googleapis.com/v1/albums').text)
