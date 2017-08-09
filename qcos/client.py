# -*- coding: utf-8 -*-
import time
import requests
from .auth import Auth


class COSClient(object):

    def __init__(self, secret_id, secret_key, region, appid, bucket):
        self.secret_id = secret_id
        self.secret_key = secret_key
        self.appid = appid
        self.bucket = bucket
        self.auth = Auth(secret_id, secret_key, appid, bucket)

        self.url_prefix = 'http://{}.file.myqcloud.com/files/v2/{}/{}' \
            .format(region, appid, bucket)

        self.session = requests.Session()
        self._reset_auth()

    def _reset_auth(self):
        self.auth_expired = int(time.time()) + 21600
        self.session.headers['Authorization'] = \
            self.auth.sign_multi(self.auth_expired)

    def _request(self, method, cos_path,
                 params=None, data=None, headers=None, files=None):
        if int(time.time()) > self.auth_expired:
            self._reset_auth()
        if not cos_path.startswith('/'):
            cos_path = '/' + cos_path

        url = '{}{}'.format(self.url_prefix, cos_path)
        r = self.session.request(method, url,
                                 params=params, data=data,
                                 headers=headers, files=files)
        if r.json().get('code') == -96:
            self._reset_auth()
        return r

    def upload_local(self, local_path, cos_path,
                     sha=None, biz_attr=None, insertOnly=None):
        filecontent = open(local_path, 'rb')
        return self.upload_content(
            filecontent,
            cos_path,
            sha,
            biz_attr,
            insertOnly
        )

    def upload_content(self, filecontent, cos_path,
                       sha=None, biz_attr=None, insertOnly=None):
        """`简单上传文件
        <https://www.qcloud.com/document/api/436/6066>`_
        """
        data = {'op': 'upload'}
        files = {'filecontent': filecontent}

        if sha is not None:
            data['sha'] = sha

        if biz_attr is not None:
            data['biz_attr'] = biz_attr

        if insertOnly is not None:
            data['insertOnly'] = insertOnly

        return self._request('POST', cos_path, data=data, files=files)

    def stat(self, cos_path):
        """`查询文件属性
        <https://www.qcloud.com/document/api/436/6069>`_
        """
        return self._request('GET', cos_path, params={'op': 'stat'})
