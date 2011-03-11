#!/usr/bin/env python
# 
#   Author: Vincent Perricone <vhp aT lavabit.com>
#   Date: 3/10/2011
#   Title: Dupe Finder - Duplicate File Finder
#   License: Released under "Simplified BSD License" see LICENSE file
#
import sys
import os
import hashlib

hashdict = {}

def output():
    for key in hashdict:
        if hashdict[key][1] > 1:
            print("Matches: ")
            for filename in hashdict[key][0]:
                print("\t{0}").format(filename)

def create_dict(key, filename):
    if key in hashdict:
        hashdict[key][0].append(filename)
        hashdict[key][1] = hashdict[key][1] + 1
    else:
        hashdict[key] = [[filename], 1]

def read_chunk(file_obj):
    while True:
        chunk = file_obj.read(1024)  #SHA512 Blocl Size 1024
        if not chunk:
            break
        yield chunk
    
def hash_file(f):
    sha512 = hashlib.sha512()
    try:
        hashable = open(f, 'r')
    except IOError:
        print("Could not properly open {0}").format(f)
    for chunk in read_chunk(hashable):
        sha512.update(chunk)
    return sha512.digest()

def walkdirs(directory):
    for root, dirs, files in os.walk(directory):
        for f in files:
            print("Working on: {0}").format(str(os.path.join(root,f)))
            create_dict(hash_file(os.path.join(root,f)),os.path.join(root,f))
    
def main(directories):
    map(os.path.expanduser, directories)
    for dirs in directories:
        if os.path.isdir(dirs):
            walkdirs(dirs);
        else:
            print("{0} invalid directory").format(dirs)
    output()

if __name__ == '__main__':
    main(sys.argv[1:])
