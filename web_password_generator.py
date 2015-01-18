#!/usr/bin/env python
#Secure Planet LLC
import urllib2
import re
from collections import OrderedDict
import os, sys

def stripHTMLTags (html):
  """
    Strip HTML tags from any string and transfrom special entities
  """
  import re
  text = html
 
  # apply rules in given order!
  rules = [
    { r'>\s+' : u'>'},                  # remove spaces after a tag opens or closes
    { r'\s+' : u' '},                   # replace consecutive spaces
    { r'\s*<br\s*/?>\s*' : u'\n'},      # newline after a <br>
    { r'</(div)\s*>\s*' : u'\n'},       # newline after </p> and </div> and <h1/>...
    { r'</(p|h\d)\s*>\s*' : u'\n\n'},   # newline after </p> and </div> and <h1/>...
    { r'<head>.*<\s*(/head|body)[^>]*>' : u'' },     # remove <head> to </head>
    { r'<a\s+href="([^"]+)"[^>]*>.*</a>' : r'\1' },  # show links instead of texts
    { r'[ \t]*<[^<]*?/?>' : u'' },            # remove remaining tags
    { r'^\s+' : u'' }                   # remove spaces at the beginning
  ]
 
  for rule in rules:
    for (k,v) in rule.items():
      try:
        regex = re.compile (k)
        text  = regex.sub (v, text)
      except:
        pass
 
  # replace special strings
  special = {
    '&nbsp;' : ' ', '&amp;' : '&', '&quot;' : '"',
    '&lt;'   : '<', '&gt;'  : '>'
  }
 
  for (k,v) in special.items():
    text = text.replace (k, v)
 
  return text


y_arr = []

try:
    file_list = open('sites.txt','r')
    sites = file_list.read().split(',')
except:
    print "###########################################"
    print "#Password Generator Version .01           #"
    print "#Peter Kim                                #"
    print "#Please Create a sites.txt file with a    #"
    print "#Comma Seperated list of URLs             #"
    print "###########################################"
    sys.exit(0)
for site in sites:
    try:
        site = site.strip()
        print "[*] Downloading Content For : " + site
        x_arr = []
        response = urllib2.urlopen(site)
        x = stripHTMLTags(response.read())
        x = x.replace('\n',' ')
        x = x.replace(',',' ')
        x = x.replace('.',' ')
        x = x.replace('/',' ')
        x = re.sub('[^A-Za-z0-9]+', ' ', x)
        x_arr = x.split(' ')
        for y in x_arr:
            y = y.strip()
            if y and (len(y) > 4):
              if ((y[0] == '2') and (y[1] == 'F')) or ((y[0] == '2') and (y[1] == '3')) or ((y[0] == '3') and (y[1] == 'F')) or ((y[0] == '3') and (y[1] == 'D')):
                y = y[2:]
              y_arr.append(y)
    except:
        pass


y_arr_unique = OrderedDict.fromkeys(y_arr).keys()
print "[*] Processing List"
f_write = open("passwordList.txt","w")
for yy in y_arr_unique:
  if yy.strip().isdigit():
    pass
  else:
    #print yy.strip()
    f_write.write(yy.strip() + "\n")
f_write.close()
print "[*] Process Complete"
print "[*] Output Located: passwordList.txt"
print "[*] Total Count of Passwords : " + str(len(y_arr_unique))

