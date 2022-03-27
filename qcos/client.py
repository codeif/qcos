import gzip
import json
import mimetypes
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

    def head(self, key, **kwargs):
        return self.request("HEAD", key, **kwargs)

    def get(self, key, **kwargs):
        return self.request("GET", key, **kwargs)

    def delete(self, key):
        return self.request("DELETE", key)

    def put_object(self, key, data, content_type=None, headers=None, **kwargs):
        if content_type is None:
            content_type = guess_content_type(key)
        if headers is None:
            headers = {}
        headers["Content-Type"] = content_type
        return self.request("PUT", key, data=data, headers=headers, **kwargs)

    def put_local(self, key, local_path, **kwargs):
        with open(local_path, "rb") as f:
            return self.smart_put_object(key, data=f.read(), **kwargs)

    def smart_put_object(
        self,
        key,
        data,
        content_type=None,
        headers=None,
        gzip_min_length=20,
        gzip_comp_level=9,
        **kwargs,
    ):
        if isinstance(data, (dict, list)):
            content_type = "application/json"
            data = json.dumps(data, ensure_ascii=False)
        if isinstance(data, str):
            data = data.encode("utf-8")
        if len(data) > gzip_min_length:
            gzip_data = gzip.compress(data, compresslevel=gzip_comp_level)
            if len(data) > len(gzip_data):
                if headers is None:
                    headers = {}
                headers["Content-Encoding"] = "gzip"
                data = gzip_data
        return self.put_object(key, data, content_type, headers=headers, **kwargs)

    def get_object_or_none(self, key):
        """如果status_code是404，返回None"""
        r = self.get(key)
        if r.status_code == 404:
            return
        return r


def guess_content_type(filename):
    content_type = mimetypes.guess_type(filename)[0]
    if not content_type:
        return "application/octet-stream"
    return content_type
