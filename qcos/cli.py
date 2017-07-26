# -*- coding: utf-8 -*-
import argparse
import os.path
from termcolor import cprint

from .configure import QcloudConfig
from .client import COSClient

parser = argparse.ArgumentParser(
    description='腾讯云COS管理.')
parser.add_argument('local_dir')
parser.add_argument('appid')
parser.add_argument('bucket')
parser.add_argument('cos_dir')


def main():
    # 参数包含local_path, bucket
    parsed_args = parser.parse_args()

    # 命令行参数
    local_dir = parsed_args.local_dir
    appid = parsed_args.appid
    bucket = parsed_args.bucket
    cos_dir = parsed_args.cos_dir

    local_dir = os.path.abspath(os.path.expanduser(local_dir))
    slice_start = len(local_dir) + 1

    print('local_dir: ', local_dir)
    print('appid: ', appid, 'bucket: ', bucket, 'cos_dir: ', cos_dir)

    # 配置文件配置
    config = QcloudConfig()
    client = COSClient(config.secret_id, config.secret_key, config.region,
                       appid, bucket)

    for root, dirs, files in os.walk(local_dir):
        for f in files:
            local_path = os.path.join(root, f)
            cos_path = os.path.join(cos_dir, local_path[slice_start:])
            if local_path.endswith('.html'):
                r = client.upload_local(local_path, cos_path, insertOnly=0)
            else:
                r = client.upload_local(local_path, cos_path)
            j = r.json()
            code = j.get('code')
            if code == 0:
                cprint('{} Upload success!'.format(cos_path), 'green')
            elif code == -177:
                cprint('{} Upload failed, file exit.'.format(cos_path), 'blue')
            else:
                cprint('{} Upload failed! {}'.format(cos_path, r.text), 'red')
