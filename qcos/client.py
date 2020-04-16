from urllib.parse import urljoin

import requests

from .auth import CosS3Auth


class Client:
    def __init__(self, secret_id, secret_key, region, bucket, scheme="https"):
        assert scheme in ["http", "https"]

        self.secret_id = secret_id
        self.secret_key = secret_key

        self.region = region
        self.bucket = bucket
        self.scheme = scheme

    def get_object_url(self, key):
        return urljoin(
            f"{self.scheme}://{self.bucket}.cos.{self.region}.myqcloud.com", key
        )

    def request(self, method, key, **kwargs):
        url = self.get_object_url(key)
        return requests.request(
            method, url, auth=CosS3Auth(self.secret_id, self.secret_key, key), **kwargs,
        )

    def head_object(self, key):
        return self.request("HEAD", key)

    def get_object(self, key):
        return self.request("GET", key)

    def put_object(self, key, data=None, **kwargs):
        return self.request("PUT", key, data=data, **kwargs)

    def put_local(self, key, local_path, **kwargs):
        with open(local_path, "rb") as f:
            return self.request("PUT", key, data=f, **kwargs)

    def get_object_or_none(self, key):
        """如果status_code是404，返回None"""
        r = self.get_object(key)
        if r.status_code == 404:
            return
        return r
