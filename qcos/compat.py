# -*- coding: utf-8 -*-

"""
qcos.compat
~~~~~~~~~~~~~~~
This module handles import compatibility issues between Python 2 and
Python 3.
"""

import sys

# -------
# Pythons
# -------

# Syntax sugar.
_ver = sys.version_info

#: Python 2.x?
is_py2 = (_ver[0] == 2)

#: Python 3.x?
is_py3 = (_ver[0] == 3)

# ---------
# Specifics
# ---------

if is_py2:
    from urllib import quote
    from ConfigParser import ConfigParser

elif is_py3:
    from urllib.parse import quote
    from configparser import ConfigParser


__all__ = ['quote', 'ConfigParser']
