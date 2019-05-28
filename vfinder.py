#!/usr/bin/env python3
#
# Search for a file hash in a Git repo
# Clones the git repo and steps through every commit checking if a file matches a hash
# Intended to fingerprint website versions based on a public file (such as .js or .css)
# Usage: $ ./vfinder.py <repo> <filepath> <MD5 hash>
#
import hashlib
import os
import subprocess
import sys
import time

from datetime import datetime

def md5(fname):
    hash_md5 = hashlib.md5()
    with open(fname, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()

def sha1(fname):
    hash_sha1 = hashlib.sha1()
    with open(fname, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_sha1.update(chunk)
    return hash_sha1.hexdigest()

if len(sys.argv) < 4:
    print("Usage: $ ./vfinder.py <repo> <filepath> <MD5 hash>")
    sys.exit(1)

repo = sys.argv[1]
filepath = sys.argv[2]
filehash = sys.argv[3].upper()

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
print("Scanning for " + filepath + " in " + str(len(tags)) + " tags")
for tag in tags:
    ret = os.system('git checkout --quiet ' + tag)
    if ret != 0:
        sys.exit(1)
    if os.path.isfile(filepath):
        md5hash = md5(filepath).upper()
        if md5hash == filehash:
            print(tag.strip())
