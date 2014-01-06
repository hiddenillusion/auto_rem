#!/usr/bin/env python

# AutoAnalyzer.py was created by Glenn P. Edwards Jr.
#	http://hiddenillusion.blogspot.com
#		@hiddenillusion
# Version 0.1
# Date: 10-28-2013

import os
import sys
import html_generator
import general as gen

fname = sys.argv[1]
rpt_dir = os.path.join(os.getcwd(), 'rpt')

"""
def OS_check():
    if os.name == "nt":
	    platform = 'Gates'
    else:
        platform = 'Linus'

    return platform
"""

if TL.OS_check() == 'Gates':
	print "[!] Analysis platform is Windows"
	sys.exit()

# write the reports
with open(os.path.join(rpt_dir, 'general.txt'), 'a') as outty:
    for item in fileID.trid(fname):
        
    outty.write(gen.exif(fname))
    outty.write(gen.sigchecker(fname))
    #outty.write(#gen.adobe_classifer(fname))

# HTML reports
print "[+] Generating HTML reports"
index_html   = os.path.join(rpt_dir, "index.html")
menu_html    = os.path.join(rpt_dir, "menu.html")
content_html = os.path.join(rpt_dir, "content.html")
html_generator.printIndex(index_html, content_html)
html_generator.printContent(content_html)		
html_generator.printMenu(rpt_dir, index_html, menu_html, content_html)