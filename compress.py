#!/usr/bin/python
# -*- coding: UTF-8 -*-
r"""
@author: Martin Klapproth <martin.klapproth@googlemail.com>
"""
from genericpath import isfile

import logging
import argparse
import os
import subprocess
import shutil

from os.path import abspath, join, islink
from os import walk
import fnmatch
import sys

parser = argparse.ArgumentParser(description='')
parser.add_argument('path', metavar='PATH', nargs='*', type=str)
parser.add_argument('-v', '--verbose', dest="verbose", action="store_true")
parser.add_argument('--follow-symlinks', dest="follow_symlinks", action="store_true")
parser.add_argument('--no-png', dest="no_png", action="store_true")
parser.add_argument('--no-gzip', dest="no_gzip", action="store_true")
parser.add_argument('--no-brotli', dest="no_brotli", action="store_true")
args = parser.parse_args()

logger = logging.getLogger()
sh = logging.StreamHandler(sys.stdout)
sh.setFormatter(logging.Formatter("%(asctime)s %(levelname)-8s %(name)-12s %(message)s", datefmt='%Y-%m-%d %H:%M:%S'))
logger.addHandler(sh)
logger.setLevel(logging.DEBUG)

def locate(pattern, root, followlinks=None):
    """
    Locate all files matching supplied filename pattern in and below
    supplied root directory.
    """
    if followlinks is None:
        followlinks = args.followlinks

    for path, _, files in walk(abspath(root), followlinks=followlinks):
        for filename in fnmatch.filter(files, pattern):
            yield join(path, filename)

def log_debug(text):
    if args.verbose:
        logger.debug(text)

class Compressor(object):
    def __init__(self):
        self.brotli_exec_path = "brotli"
        self.gzip_exec_path = "gzip"
        self.optipng_exec_path = "optipng"
        self.root = args.path

        self.ignore_extensions = [".gz", ".br", ".orig"]

    def main(self):
        roots = args.path
        if not roots:
            roots = ["/work"]

        for root in roots:
            logger.info("Compressing files in %s" % root)

            counter = 0
            for path in locate("*", root, followlinks=False):
                self.handle_path(path)
                counter += 1

            logger.info("Checked %s files" % counter)

    def handle_path(self, path):
        directory, fname = os.path.split(path)

        # ignore hidden files
        if fname.startswith("."):
            log_debug("Ignoring %s: hidden file/directory" % path)
            return

        # ignore symlinks
        if islink(path):
            log_debug("Ignoring %s: is a link" % path)
            return

        if not isfile(path):
            log_debug("Ignoring %s: not a file" % path)
            return

        name, extension = os.path.splitext(path)
        if extension in self.ignore_extensions:
            log_debug("Ignoring %s: is a already compressed file" % path)
            return

        if extension == ".png":
            self.exec_optipng(path)

        self.exec_gzip(path)
        self.exec_brotli(path)

    def exec_gzip(self, path):
        gzip_path = path + ".gz"
        if isfile(gzip_path):
            return

        logger.info("%s: compressing gzip" % path)
        command = [self.gzip_exec_path, "-k", "-9", path]
        subprocess.check_output(command)

    def exec_brotli(self, path):
        brotli_path = path + ".br"
        if isfile(brotli_path):
            return

        logger.info("%s: compressing brotli" % path)
        command = [self.brotli_exec_path, "-k", "-f", "-q", "11", path]
        subprocess.check_output(command)

        # set mode and modification time from source file to brotli file
        stat = os.stat(path)
        os.utime(brotli_path, (stat.st_atime, stat.st_mtime))
        os.chmod(brotli_path, stat.st_mode)

    def exec_optipng(self, path):
        orig_path = path + ".orig"
        if isfile(orig_path):
            return

        stat = os.stat(path)

        logger.info("%s: optimizing png" % path)
        shutil.copy2(path, orig_path)
        command = [self.optipng_exec_path, "-o5", path]
        subprocess.check_output(command, stderr=subprocess.STDOUT)

        # set mode and modification time from source file to brotli file
        os.utime(path, (stat.st_atime, stat.st_mtime))
        os.chmod(path, stat.st_mode)

    def exec_noop(self, *args, **kwargs):
        pass

if __name__ == '__main__':
    compressor = Compressor()
    if args.no_png:
        compressor.exec_optipng = compressor.exec_noop
    if args.no_gzip:
        compressor.exec_gzip = compressor.exec_noop
    if args.no_brotli:
        compressor.exec_brotli = compressor.exec_noop

    compressor.main()
