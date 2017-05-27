# -*- coding: utf-8 -*-
import os
import os.path

from .compat import ConfigParser


class QcloudConfig(object):
    def __init__(self):
        config = ConfigParser()
        config.read([os.path.expanduser('~/.qcloudcli/configure'),
                     os.path.expanduser('~/.qcloudcli/credentials'), ])
        section = 'default'
        self.secret_id = config.get(section, 'qcloud_secretid')
        self.secret_key = config.get(section, 'qcloud_secretkey')
        self.region = config.get(section, 'region')
