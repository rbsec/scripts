#!/usr/bin/env python3
#
# Script to generate NSRL formatted hash lists from a Git repo
# Clones the git repo and calculates MD5 and SHA1 hashes for every file in every tag
# Primarily for use with X-Ways Forensics, but could be used with any other tool
# Usage: $ ./xhash.py <repo> <outputfile>
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

if len(sys.argv) < 3:
    print("Usage: $ hash.py <repo> <outfile>")
    sys.exit(1)

repo = sys.argv[1]
outfile = sys.argv[2]
start_time = datetime.now()

with open(outfile, 'w') as out:
    try:
        reponame = repo.rsplit('/',1)[1]
    except IndexError:
        reponame = repo
    if not (os.path.isdir(reponame)):
        print("Trying to clone " + repo + " into " + reponame)
        os.system('git clone ' + repo + ' ' + reponame)
    os.chdir(reponame)
    seen = set()
    tags = os.popen('git tag').readlines()
    out.write('"SHA-1","MD5","CRC32","FileName","FileSize","ProductCode","OpSystemCode","SpecialCode"\n')
    i = 1
    hashcount = 0
    for tag in tags:
        print("["+str(i)+"/"+str(len(tags))+"] " + str(hashcount) + " - "+ tag.strip())
        i+=1
        a = os.system('git checkout --quiet ' + tag)
        for root,subdirs,files in os.walk('.'):
            if '/.git' in root:
                continue
            for f in files:
                fpath = os.path.join(root,f)
                size = (os.stat(fpath).st_size)
                if size == 0:
                    continue
                md5hash = md5(fpath).upper()
                if md5hash in seen:
                    continue
                seen.add(md5hash)
                sha1hash = sha1(fpath).upper()
                out.write('"' + sha1hash + '","' + md5hash + '","0000000000000000","' + f + '","'+str(size)+'","0","0",""\n')
                hashcount += 1
    print("Wrote " + str(len(seen)) + " hashes to " + outfile + " in " + str(datetime.now() - start_time))
