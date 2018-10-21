#!/usr/bin/env python

""" Copy all my flickr photos to s3, since I don't expect flickr will
be around for long.

Similar idea: https://github.com/tgerla/flickr-s3-backup

TODO: write a counterpart that uploads from S3 to Google Photos.  See
https://developers.google.com/picasa-web/docs/2.0/developers_guide_protocol#PostPhotos

There's also https://www.amazon.com/photos; I imagine it'd be easy to
get photos from S3 to there.
https://developer.amazon.com/public/apis/experience/cloud-drive/content/restful-api-getting-started

https://rclone.org/ might also let me get from S3 to Google Photos (well, at least to Google Drive)
"""

# Core
import json
import logging
import os
import pathlib
import tempfile

# 3rd-party
import boto3                    # pip install boto3
import botocore.exceptions
import configobj                # pip install configobj
import flickrapi                # pip install flickrapi
import requests                 # pip install requests
import tqdm                     # pip install tqdm

_log = logging.getLogger(__name__)

# API docs: https://www.flickr.com/services/api/


def get_auth_stuff(filename=None):
    if filename is None:
        filename = os.path.expanduser('~/.flickr-auth')

    c = configobj.ConfigObj(filename)

    return(c['flickr']['api_key'],
           c['flickr']['shared_secret'])


class FlickrAdapter:
    def __init__(self, flickr, username='offby1'):
        self.flickr = flickr
        self.username = username
        self.method_map = {
            'Exif':  self.getExif,
            'Info':  self.getInfo,
            'Original': self.get_original,
        }

    def getExif(self, id_):
        return json.dumps(self.flickr.photos_getExif(photo_id=id_)['photo'])

    def getInfo(self, id_):
        return json.dumps(self.flickr.photos_getInfo(photo_id=id_)['photo'])

    def get_original(self, id_):
        getSizes_response = self.flickr.photos_getSizes(photo_id=id_)

        for d in getSizes_response['sizes']['size']:
            if d['label'] == 'Original':
                return requests.get(d['source']).content

    def all_photo_metadata(self):
        requested_page = 1
        per_page = 100

        my_nsid = self.flickr.people_findByUsername(username=self.username)['user']['nsid']

        while True:
            rsp = self.flickr.photos_search(user_id=my_nsid,
                                            page=requested_page,
                                            per_page=str(per_page))

            photos = rsp['photos']

            for photo in photos['photo']:
                yield int(photos['total']), photo

            if int(photos['page']) == int(photos['pages']):
                return

            requested_page += 1


class S3Storage:
    def __init__(self):
        self.bucket_name = 'flickr-sanctuary'
        self.session = None
        self.s3 = None
        self.bucket = None

    def _make_object_name(self, id_, datum_name):
        return '{}/{}'.format(id_, datum_name)

    def _object_exists(self, object_name):
        if self.session is None:
            self.session = boto3.session.Session()

        if self.s3 is None:
            self.s3 = self.session.resource('s3')

        if self.bucket is None:
            self.bucket = self.s3.Bucket (self.bucket_name)

        try:
            self.bucket.Object(object_name).metadata
        except botocore.exceptions.ClientError:
            return False

        return True

    def ensure_stored(self, id_, datum_name, data_thunk):
        objname = self._make_object_name(id_, datum_name)

        if not self._object_exists(objname):
            with tempfile.TemporaryFile() as tf:
                data = data_thunk()
                if hasattr(data, 'encode'):
                    data = data.encode()
                tf.write(data)
                tf.flush()
                with tqdm.tqdm(unit='byte',
                               desc=objname,
                               total=tf.tell()) as pbar:
                    tf.seek(0)
                    self.bucket.upload_fileobj(tf,
                                               objname,
                                               Callback=pbar.update)


def _get_metadata(flickr):
    CACHE_FILE_NAME = pathlib.Path(__file__).parent / '.metadata_cache.json'
    try:
        with open(CACHE_FILE_NAME) as inf:
            _log.info(f"Reading metadata cache file {CACHE_FILE_NAME}")
            return json.load(inf)
    except FileNotFoundError:
        _log.info(f"No metadata cache file {CACHE_FILE_NAME}; grabbing metadata for all photos")

        metadata = []
        for datum in tqdm.tqdm(flickr.all_photo_metadata(),
                               unit='',
                               total=2213 # "empirically determined" :-)
    ):
            metadata.append(datum)
        with open(CACHE_FILE_NAME, 'w') as outf:
            json.dump(metadata, outf,
                      separators=(',', ':'),
                      indent=2)
            _log.info(f"Wrote metadata cache file {CACHE_FILE_NAME}")

        return _get_metadata(flickr)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s %(levelname)-5.5s [%(name)s] %(message)s')

    # fix logging to be more like RFC3339
    logging.Formatter.default_time_format = '%FT%T'
    logging.Formatter.default_msec_format = '%s.%03dZ'

    logging.getLogger('flickrapi.core').setLevel(logging.WARN)

    api_key, shared_secret = get_auth_stuff()

    flickr = FlickrAdapter(flickrapi.FlickrAPI(api_key,
                                               shared_secret,
                                               format='parsed-json',
                                               cache=True))

    all_photo_metadata = _get_metadata(flickr)

    try:
        storage = S3Storage()
        _log.info("Ensuring all photos are uploaded")
        for (_, photo) in tqdm.tqdm(all_photo_metadata,
                                    unit='photo'):

            id_ = photo['id']
            for (datum_name, method) in flickr.method_map.items():
                storage.ensure_stored(id_,
                                      datum_name=datum_name,
                                      data_thunk=lambda : method(id_))

    except KeyboardInterrupt:
        pass
