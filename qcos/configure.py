# -*- coding: utf-8 -*-
import json
import os
import os.path


class Configure(object):
    def __init__(self):
        self.cli_path = os.path.join(os.path.expanduser("~"), ".tccli")

        name = "default"
        is_conexit, config_path = self._profile_existed(name + ".configure")
        is_creexit, cred_path = self._profile_existed(name + ".credential")

        conf = {}
        cred = {}
        if is_conexit:
            conf = self._load_json_msg(config_path)
        if is_creexit:
            cred = self._load_json_msg(cred_path)

        self.region = conf.get('region')
        self.secret_id = cred.get('secretId')
        self.secret_key = cred.get('secretKey')

    def _profile_existed(self, profile_name):
        file_path = os.path.join(self.cli_path, profile_name)
        if os.path.exists(file_path):
            return True, file_path
        return False, file_path

    def _load_json_msg(self, filename):
        with open(filename, "r") as f:
            data = json.load(f)
            return data
