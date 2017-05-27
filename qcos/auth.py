# -*- coding: utf-8 -*-
import random
import time
import hmac
import hashlib
import base64

from .compat import quote


class Auth(object):
    def __init__(self, secret_id, secret_key, appid, bucket):
        self.secret_id = secret_id
        self.secret_key = secret_key
        self.appid = appid
        self.bucket = bucket

    def _sign(self, cos_path, expired):
        """expired为0时是multi签名方式"""
        rdm = random.randint(0, 999999999)

        if cos_path:
            fileid = '/{}/{}{}'.format(self.appid,
                                       self.bucket,
                                       quote(cos_path, '/'))
        else:
            fileid = ''

        now = int(time.time())
        if expired and expired <= 7776000:
            expired = now + expired

        sign_items = [
            ('a', self.appid),
            ('b', self.bucket),
            ('k', self.secret_id),
            ('t', now),
            ('e', expired),
            ('r', rdm),
            ('f', fileid)
        ]

        plain_text = '&'.join('{}={}'.format(*x) for x in sign_items)
        plain_bin = plain_text.encode('utf-8')

        sha1_hmac = hmac.new(self.secret_key.encode('utf-8'),
                             plain_bin,
                             hashlib.sha1)

        return base64.b64encode(sha1_hmac.digest() + plain_bin)

    def sign_once(self, cos_path):
        """单次签名(针对删除和更新操作)
        :param cos_path: 要操作的cos路径, 以'/'开始
        :return: 签名字符串
        """
        return self._sign(cos_path, 0)

    def sign_multi(self, expired):
        """多次签名(针对上传文件，创建目录, 获取文件目录属性, 拉取目录列表)
        :param expired: 签名过期时间, UNIX时间戳, 或者过期时长
        :return: 签名字符串
        """
        return self._sign('', expired)
