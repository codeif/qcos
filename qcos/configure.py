import json
from pathlib import Path


class Configure(object):
    """加载tccli配置的配置文件
    https://cloud.tencent.com/document/product/440
    """
    def __init__(self):
        conf = self._load_json('default.configure')
        cred = self._load_json('default.credential')

        self.region = conf.get('region')
        self.secret_id = cred.get('secretId')
        self.secret_key = cred.get('secretKey')
        assert self.region and self.secret_id

    def _load_json(self, name):
        p = Path.home() / '.tccli' / name
        if not p.exists():
            return
        with p.open() as f:
            return json.load(f)
