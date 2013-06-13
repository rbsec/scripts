#!/usr/bin/python
#
# Simple script to generate a list of nano backup files (.php~) from a burp sitemap
# Usage: $ ./nanobackup-burp.py <inputfile> [outfile]
# Saves output to wordlist.txt by default
#
import base64
import re
import sys
import urlparse
try:    # Use faster C implementation if we can
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET

wordlist = set()

for event, elem in ET.iterparse(sys.argv[1]):
    if event == 'end':
        if elem.tag == 'url':
            u = str(elem.text)
            url = urlparse.urlsplit(u)
            if url.path.endswith('php'):
                wordlist.add(url.path)
    elem.clear() # Discard the element to free memory


wordlist = sorted(wordlist, key=lambda s: s.lower())    # Case insensitive sort

try:
    outfile = sys.argv[2]
except IndexError:
    outfile = "wordlist.txt"
f = open(outfile, "w")
for word in wordlist:
    f.write(word + "~\n")
print("Wrote " + str(len(wordlist)) + " words to " + outfile)
