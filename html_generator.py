#!/usr/bin/env python

# created by Glenn P. Edwards Jr.
#   http://hiddenillusion.blogspot.com
#       @hiddenillusion
# Version 0.2
# Date: 07-23-2013
# (while at FireEye)

import os
import sys
import datetime
import argparse

def printIndex(index_html, content_fn):
    """
    Creating the Index HTML page to house the other frameset
    """	  
    content_lnk = '<frame src="%s" name="content">' % content_fn

    with open(index_html, 'w') as index_out:
        index_out.write('''
		    <html>
		    <head>
		    <title>Automated Report</title>
		    </head>

		    <frameset cols="20%,*">
		    <frame src="menu.html" name="menu">
            ''')
        index_out.write(content_lnk)
        index_out.write('''
		    </frameset>
		    ''')

def printMenu(rpt_dir, index_html, menu_html, content_fn):
    """
    Creating the HTML menu for the left side of the report
    """	
    lnks_list = []
    cnt = len(os.walk(rpt_dir).next()[2])	
    print "[-] Total reports found:",cnt
    now = datetime.datetime.now() 
    generated = now.strftime("%Y-%m-%d %H:%M")    

    if os.path.exists(menu_html):
        print "[!] HTML menu already exists"
        sys.exit()
    else:
        # This add the javascript that allows for collapsing and expanding
        with open(menu_html, 'w') as menu_out:
                menu_out.write('''
                    <html> 
                    <head> 
            <script type="text/javascript">
            var collapseDivs, collapseLinks;

            function createDocumentStructure (tagName) {
              if (document.getElementsByTagName) {
                var elements = document.getElementsByTagName(tagName);
                collapseDivs = new Array(elements.length);
                collapseLinks = new Array(elements.length);
                for (var i = 0; i < elements.length; i++) {
                  var element = elements[i];
                  var siblingContainer;
                  if (document.createElement &&
                      (siblingContainer = document.createElement('div')) &&
                      siblingContainer.style)
                  {
                    var nextSibling = element.nextSibling;
                    element.parentNode.insertBefore(siblingContainer, nextSibling);
                    var nextElement = elements[i + 1];
                    while (nextSibling != nextElement && nextSibling != null) {
                      var toMove = nextSibling;
                      nextSibling = nextSibling.nextSibling;
                      siblingContainer.appendChild(toMove);
                    }
                    siblingContainer.style.display = 'none';

                    collapseDivs[i] = siblingContainer;

                    createCollapseLink(element, siblingContainer, i);
                  }
                  else {
                    // no dynamic creation of elements possible
                    return;
                  }
                }
                createCollapseExpandAll(elements[0]);
              }
            }

            function createCollapseLink (element, siblingContainer, index) {
              var span;
              if (document.createElement && (span = document.createElement('span'))) {
                span.appendChild(document.createTextNode(String.fromCharCode(160)));
                var link = document.createElement('a');
                link.collapseDiv = siblingContainer;
                link.href = '#';
                link.appendChild(document.createTextNode(' [+]'));
                link.onclick = collapseExpandLink;
                collapseLinks[index] = link;
                span.appendChild(link);
                element.appendChild(span);
              }
            }

            function collapseExpandLink (evt) {
              if (this.collapseDiv.style.display == '') {
                this.parentNode.parentNode.nextSibling.style.display = 'none';
                this.firstChild.nodeValue = ' [+]';
              }
              else {
                this.parentNode.parentNode.nextSibling.style.display = '';
                this.firstChild.nodeValue = ' [-]';
              }

              if (evt && evt.preventDefault) {
                evt.preventDefault();
              }
              return false;
            }

            function createCollapseExpandAll (firstElement) {
              var div;
              if (document.createElement && (div = document.createElement('div'))) {
                var link = document.createElement('a');
                link.href = '#';
                link.appendChild(document.createTextNode('[expand all]'));
                link.onclick = expandAll;
                div.appendChild(link);
                div.appendChild(document.createTextNode(' '));
                link = document.createElement('a');
                link.href = '#';
                link.appendChild(document.createTextNode('[collapse all]'));
                link.onclick = collapseAll;
                div.appendChild(link);
                firstElement.parentNode.insertBefore(div, firstElement);
              }
            }

            function expandAll (evt) {
              for (var i = 0; i < collapseDivs.length; i++) {
                collapseDivs[i].style.display = '';
                collapseLinks[i].firstChild.nodeValue = ' [-]';
              }

              if (evt && evt.preventDefault) {
                evt.preventDefault();
              }
              return false;
            }

            function collapseAll (evt) {
              for (var i = 0; i < collapseDivs.length; i++) {
                collapseDivs[i].style.display = 'none';
                collapseLinks[i].firstChild.nodeValue = ' [+]';
              }

              if (evt && evt.preventDefault) {
                evt.preventDefault();
              }
              return false;
            }
            </script>

            <script type="text/javascript">
            window.onload = function (evt) {
              createDocumentStructure('h3'); //what to collapse/expand
            }
            </script>

        <style type="text/css">
        body {font-family:Calibri;
            margin-left: 2em;
            margin-right: 2em;
            width: 75%
        }
        a{color: #4298B5;
            font-weight: normal;
        }
        a:link {color: #4298B5;
            text-decoration:none}

        h1 { color: #C8102E
        }
        h3 { color: #4298B5}
        th { text-align: center;
            font-weight: bold;
            color: white;
            vertical-align: baseline;
            border: 1px solid #4298B5;
            background-color:#317187
        }
        td { vertical-align: middle }
        table { border-collapse: collapse;
            table-layout: fixed;
            margin-left: 2em;
            margin-right: 2em;
            width: 80%;
            font-size:medium
        }
        tr { border: 1px solid #4298B5}
        td { border: 1px solid #4298B5}
        caption { caption-side: top }
        table tr:nth-child(odd) td{
            background-color:#E3E8ED
        }
        </style>
                    <title> Menu </title> 
                    </head> 
                    <body bgcolor="#FFFFFF">            
                    ''')

    for rpt in os.listdir(rpt_dir):
        if os.path.join(rpt_dir, rpt) == content_fn:
            lnk = '<br><a href="%s" target="content"><b>%s</b></a>' % (os.path.join(rpt_dir, rpt), generated)
            with open(menu_html, 'a') as menu_out:
                menu_out.write(lnk)

    with open(menu_html, 'a') as menu_out:
                menu_out.write('<br><h3>Automated Reports</h3>')

    for rpt in os.listdir(rpt_dir):
        if not os.path.join(rpt_dir, rpt) == content_fn:                
            # Don't want to include our generated reports in this menu, change these if you change the above name
            if (os.path.join(rpt_dir, rpt) == menu_html) or \
               (os.path.join(rpt_dir, rpt) == index_html) or \
               (os.path.join(rpt_dir, rpt) == content_fn):  
                   pass
            else:                          
                lnk = '<br>' + '<a href="%s" target="content">%s</a>' % (os.path.join(rpt_dir, rpt), os.path.basename(rpt)) 
                lnks_list.append(lnk)
    
    with open(menu_html, 'a') as menu_out:
        for l in lnks_list:
            menu_out.write(l)

    with open(menu_html, 'a') as menu_out:
        menu_out.write('''
            </body>
            </html>
            ''')

"""
def printContent(content_fn):
    '''
    Creating the main body HTML page for the right frame if the sys_info report couldn't be found
    '''
    if os.path.exists(content_fn):
        pass
    else:
	    with open(content_fn, 'w') as content_out:
    		content_out.write('''
			    <html> 
			    <head> 
			    <title> content </title> 
			    </head> 
			    <body bgcolor="#FFFFFF"> 
			    This should hold relevant case details, alerts and/or what will be included in the default reports
			    <br>
			    (Timezone settings, disk layout, user accounts etc.)
			    </body> 
			    </html> 
			    '''
			    )	
"""
# Automatically open in default browser in Windows... might need subprocess in *nix?
#os.startfile(index_html)
