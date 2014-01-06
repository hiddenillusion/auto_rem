#!/usr/bin/env python

# auto_rem.py was created by Glenn P. Edwards Jr.
#	http://hiddenillusion.blogspot.com
#		@hiddenillusion
# Version 0.1.1
# Date: 01-06-2014

import os
import sys
import time
import hashlib
import argparse
import subprocess
from FileClassifier import fileID
from ConfigParser import SafeConfigParser

parser = argparse.ArgumentParser(description='Determine the filetype of a file for classification & analysis')
parser.add_argument('Path', help='Path to directory/file(s) to be scanned')
args = vars(parser.parse_args())

# Verify supplied path exists or die
if not os.path.exists(args['Path']):
    print "[!] The supplied path does not exist"
    sys.exit()

def md5sum(file):
    try:
        f = open(file, "rb")
        data = f.read()
        md5 =  hashlib.md5(data).hexdigest()
        f.close()
    except Exception, msg:
        print msg

    return md5

def header(msg):
    return "\n" + ("*" * 90)  + "\n" + msg + "\n" + ("*" * 90) + "\n"

# change as needed
cfg = '/usr/local/auto_rem/tools.conf'
if not os.path.exists(cfg):
	print "[!] Path to config. file needs to be set"
	sys.exit()
config = SafeConfigParser()
config.read(cfg)        

def results(data):   
    results = fileID(data)
    if "unknown" in results:
    	print "[?] Couldn't classify the file..."
    	analyze(data, 'idk')
    else:
        print "[-] Filetype.........:",results['filetype']
        print "[-] Confidence.......:",results['percentage']    
        analyze(data, results['filetype'])

def execute(report, tool, fname):
    try:
	    cmd = tool + ' ' + fname
	    p = subprocess.Popen(cmd,stderr=subprocess.PIPE,stdout=subprocess.PIPE,shell=True)
	    (stdout, stderr) = p.communicate()
	    if stdout:
	    	with open(report, 'a') as outty:
	    		outty.write(stdout)
	    		outty.write ('\n')
	    else:
	    	with open(report, 'a') as outty:
	    		outty.write(stderr)
	    		outty.write ('\n')	    	
    except Exception as err:
        print "[!] ERROR on execution"
        with open(report, 'a') as outty:
            outty.write(err)
            outty.write ('\n')
        pass

def analyze(fname, filetype):
    cfg_report_dir = config.get('Report', 'dir') 
    report_dir = os.path.join(cfg_report_dir, md5sum(fname))
    if os.path.exists(report_dir):
    	print "[*] Looks like report directory already exists; appending"
    else:
        try:
            os.makedirs(report_dir)
        except Exception as err:
            print "[!] Couldn't create report directory, does it already exist?"
            sys.exit()
    
    # this will add EPOCH w/ millisecond to the end of the report in case multiple are within the folder
    report_name = md5sum(fname) + '_' + str(time.time()) + '.txt'
    print "[-] Saving report as :",report_name
    report = os.path.join(report_dir, report_name)
    print "[-] Plugin category..: General"
    for key, value in config.items('General'):
    	with open(report, 'a') as outty:
    		outty.write(header(key))
        print "[.]",key
        execute(report, value, fname)

    if filetype == "EXE" or "DLL":
        print "[-] Plugin category..:",filetype
        for key, value in config.items('EXE'):
            with open(report, 'a') as outty:
                outty.write(header(key))
            print "[.]",key
            execute(report, value, fname)

    if filetype == "PDF":
        print "[-] Plugin category..:",filetype
        for key, value in config.items('PDF'):
            with open(report, 'a') as outty:
                outty.write(header(key))
            print "[.]",key
            execute(report, value, fname)            

        '''
	    # Iterate over a specific plugin section and display all keys
	    '''
	    #    for option in config.options('EXE'):
	    #        print "[.]",option
        '''
	    # Iterate over a plugin section and display key,value
	    '''
        #for section_name in config.sections():
        #    for key, value in config.items(section_name):
        #        print '%s = %s' % (key,value)

def pwalk(indir):
    # Recursivly walk the supplied path and process files accordingly
    for root, dirs, files in os.walk(indir):
        for name in files: 
            f = os.path.join(root, name)
            print "[+] Analyzing........:",os.path.basename(f) 
            print "[-] File size (bytes):",os.path.getsize(f) 
            results(f)       

def main():
    # Set the path to file(s)
    infile = args['Path']
    print "[+] Analyzing........:",os.path.basename(infile)    
    if os.path.isfile(infile):
        print "[-] File size (bytes):",os.path.getsize(infile)    	
        results(infile)
    elif os.path.isdir(infile):
    	print "[-] Directory provided, traversing..."
        pwalk(infile)	        

if __name__ == "__main__":
	main()  