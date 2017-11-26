#!/usr/bin/python
# -*- coding: UTF-8 -*-
r"""
@author: Martin Klapproth <martin.klapproth@googlemail.com>
"""
from genericpath import isdir, isfile

import logging
import os
from os.path import exists
import shutil

logger = logging.getLogger(__name__)

def rm(path):
    if isdir(path):
        shutil.rmtree(path)
    elif exists(path):
        os.remove(path)
