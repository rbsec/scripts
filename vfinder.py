#!/usr/bin/env python3
#
# Search for a file hash in a Git repo
# Clones the git repo and steps through every commit checking if a file matches a hash
# Intended to fingerprint website versions based on a public file (such as .js or .css)
# Usage: $ ./vfinder.py <repo> <url> [filepath]
# Filepath is only needed if the URL path to the file doesn't match the URL path
#
import hashlib
import os
import subprocess
import sys
import time
from urllib.request import urlopen
from urllib.parse import urlparse
from datetime import datetime

def md5(fname):
    hash_md5 = hashlib.md5()
    with open(fname, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()

if len(sys.argv) < 3:
    print("Usage: $ ./vfinder.py <repo> <url> [filepath]")
    sys.exit(1)
if len(sys.argv) == 4:
    filepath = sys.argv[3].lstrip('/')
else:
    filepath = ""
repo = sys.argv[1]
url = sys.argv[2]


if os.path.isfile(url):
    filehash = md5(url)
else:
    try:
        o = urlparse(url)
    except Exception as e:
        print(e)
        print("Inavlid URL")
        sys.exit(1)
    try:
        page = urlopen(url).read()
        print("Retrieved page " + url)
        if not filepath:
            filepath = o.path.lstrip('/')
    except Exception as e:
        print(e)
        sys.exit(1)
    filehash = hashlib.md5(page).hexdigest().upper()


try:
    reponame = repo.rsplit('/',1)[1]
except IndexError:
    reponame = repo
if not (os.path.isdir(reponame)):
    print("Trying to clone " + repo + " into " + reponame)
    try:
        os.system('git clone ' + repo + ' ' + reponame)
    except KeyboardInterrupt:
        sys.exit(1)
os.chdir(reponame)
seen = set()
tags = os.popen('git tag').readlines()
print("Scanning for " + filepath + " (" + filehash + ") in " + str(len(tags)) + " tags")
for tag in tags:
    ret = os.system('git checkout -f --quiet ' + tag)
    if ret != 0:
        sys.exit(1)
    if os.path.isfile(filepath):
        md5hash = md5(filepath).upper()
        if md5hash == filehash:
            print(tag.strip())
