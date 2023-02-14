#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Author: Aaron-Yang [code@jieyu.ai]
Contributors:

"""
import logging
import os
import sys
from importlib.metadata import version
from os import path

import os

logger = logging.getLogger(__name__)


def get_config_dir():
    _dir = os.path.expanduser("~/.chatter/config")

    sys.path.insert(0, _dir)
    logger.info("config dir is %s", _dir)
    return _dir


def endpoint():
    return "abcde"
