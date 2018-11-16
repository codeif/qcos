import argparse
import os.path

from termcolor import cprint

from . import Client, Configure

parser = argparse.ArgumentParser(description='腾讯云COS管理.')
parser.add_argument('local_dir')
parser.add_argument('region')
parser.add_argument('bucket')
parser.add_argument('cos_dir')


def main():
    # 参数包含local_path, bucket
    parsed_args = parser.parse_args()

    # 命令行参数
    local_dir = parsed_args.local_dir
    region = parsed_args.region
    bucket = parsed_args.bucket
    cos_dir = parsed_args.cos_dir

    local_dir = os.path.abspath(os.path.expanduser(local_dir))
    slice_start = len(local_dir) + 1

    print('local_dir: ', local_dir)
    print('bucket: ', bucket, 'cos_dir: ', cos_dir)

    # 配置文件配置
    config = Configure()
    client = Client(config.secret_id, config.secret_key, region, bucket)

    for root, dirs, files in os.walk(local_dir):
        for f in files:
            local_path = os.path.join(root, f)
            key = os.path.join(cos_dir, local_path[slice_start:])
            if local_path.endswith('.html') or client.head_object(key).status_code == 404:
                r = client.put_local(key, local_path)
                cprint(f'已上传 {key} {r.status_code}', 'blue')
                assert r.status_code == 200
            else:
                cprint(f'已存在 {key}', 'red')
