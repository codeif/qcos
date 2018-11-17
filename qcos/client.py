from urllib.parse import urljoin

import requests

from .auth import CosS3Auth


class Client(object):

    def __init__(self, secret_id, secret_key, region, bucket, scheme='https'):
        assert scheme in ['http', 'https']

        self.secret_id = secret_id
        self.secret_key = secret_key

        self.region = region
        self.bucket = bucket
        self.scheme = scheme

        self.session = requests.Session()

    def get_url(self, key):
        return urljoin(f'{self.scheme}://{self.bucket}.cos.{self.region}.myqcloud.com', key)

    def request(self, method, key, **kwargs):
        url = self.get_url(key)
        return self.session.request(
            method,
            url,
            auth=CosS3Auth(self.secret_id, self.secret_key, key),
            **kwargs,
        )

    def head_object(self, key):
        return self.request('HEAD', key)

    def put_object(self, key, data, **kwargs):
        return self.request('PUT', key, data=data, **kwargs)

    def put_local(self, key, local_path, **kwargs):
        with open(local_path, 'rb') as f:
            return self.request('PUT', key, data=f, **kwargs)
