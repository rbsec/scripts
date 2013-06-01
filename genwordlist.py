#!/usr/bin/python
#
# Simple script to generate a sorted unique wordlist from an input file
# Usage: $ ./genwordlist.py <inputfile>
# Saves output to wordlist.txt
#
import re
import sys

wordlist = set()
with open(sys.argv[1]) as f:
    lines = f.readlines()
for line in lines:
    words = re.findall("[a-zA-Z0-9\-]+", line)
    for word in words:
        wordlist.add(word)

wordlist = sorted(wordlist, key=lambda s: s.lower())
f = open("wordlist.txt", "w")
for word in wordlist:
    f.write(word + "\n")
print("Wrote " + str(len(wordlist)) + " words to wordlist.txt")
