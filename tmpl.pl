#!/usr/bin/env python
# -*- coding: utf-8 -*-
import argparse
import sys
import re
import requests
import lxml.html

def error(msg):
    print("[!]",msg)  
    exit()

# option parser
parser = argparse.ArgumentParser(description='generate report for vlunnerability')
parser.add_argument('cve', help="target cve nunmber")
args = parser.parse_args()

# validation
cve = args.cve.upper()
if not re.match(r"^CVE-\d{4}-\d{4}$" , cve): error("invalid cve format")

# nvd
nvd_url = "https://web.nvd.nist.gov/view/vuln/detail?vulnId=" + cve
nvd_html = requests.get(nvd_url).text
# print(nvd_html)
root = lxml.html.fromstring(nvd_html)
cvss3 = root.cssselect('#BodyPlaceHolder_cplPageContent_plcZones_lt_zoneCenter_VulnerabilityDetail_VulnFormView_Vuln3CvssPanel > div[class="row"]')

for elm in cvss3:
    label, value = (elm.text_content().split(':',1))
    label = label.replace('\r\n','')
    label = re.sub(r'\s+', '', label)
    print(label)
    exit()
    
    # a = re.search(r"^\s*(.+?):(.+?)$", elm.text_content().replace('\n',''))
    #print(a.groups())


#    print(a.group())
#    label, value = elm.text_content().replace('\n','').split(':', 1)
#    print("label = ", label, "value = ", value)
