#!/usr/bin/env python

# FileClassifier.py was created by Glenn P. Edwards Jr.
#	http://hiddenillusion.blogspot.com
#		@hiddenillusion
# Version 0.1
# Date: 12-19-2013
"""
To-Do:
    [ ] Add pw checker function
"""

import os
import re
import sys
import argparse
import subprocess

parser = argparse.ArgumentParser(description='Determine the filetype of a file for classification & analysis')
parser.add_argument('Path', help='Path to directory/file(s) to be scanned')
args = vars(parser.parse_args())

# Verify supplied path exists or die
if not os.path.exists(args['Path']):
    print "[!] The supplied path does not exist"
    sys.exit()

def q(s):
    quote = "\""
    s = quote + s + quote
    return s

def fileID(infile):
    precent = ''
    ext = ''
    classification = {}
	# change path as needed
    trid_defs = '/usr/local/lib/triddefs.trd'
    cmd = 'trid' + ' -r:1 -d:' + trid_defs + ' ' +  q(infile)
    p = subprocess.Popen(cmd,stderr=subprocess.PIPE,stdout=subprocess.PIPE,shell=True)
    (stdout, stderr) = p.communicate()
    if stdout:
        for line in stdout.split('\n'):
            if "%" in line:
                #  e.g. - 60.8% (.EXE) Win32 Executable MS Visual C++ (generic) (31206/45/13)
                for section in line.split(' '):
                    if re.match('\d.*%',section):
                        if section > 50: 
                            classification['percentage'] = section
                        else:
                            return "Not enough confidence in file type"
                    if re.match('\(\..*\)', section):
                        filetype = section.replace('(.','').replace(')','')
                        classification['filetype'] = filetype
                return classification
            if "Unknown!" in line:
                return "unknown"
    else:
        return stderr

def main():
    infile = args['Path']
    print "[+] Analyzing........:",os.path.basename(infile)
    print "[-] File size (bytes):",os.path.getsize(infile)
    results = fileID(infile)
    if not "unknown" in results:
        print "[-] Filetype.........:",results['filetype']
        print "[-] Confidence.......:",results['percentage']

if __name__ == "__main__":
    main()  