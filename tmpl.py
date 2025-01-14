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

def print_nvd_info_table(cve):
    # nvd
    nvd_url = "https://web.nvd.nist.gov/view/vuln/detail?vulnId=" + cve
    nvd_html = requests.get(nvd_url).text
    # print(nvd_html)
    root = lxml.html.fromstring(nvd_html)
    cvss3 = root.cssselect('#BodyPlaceHolder_cplPageContent_plcZones_lt_zoneCenter_VulnerabilityDetail_VulnFormView_Vuln3CvssPanel > div[class="row"]')
    
    for elm in cvss3:
        label, value = (elm.text_content().split(':',1))
        label = label.replace('\r\n','')
        label = re.sub(r'\s{2,}', '', label)
        value = value.replace('\r\n','')
        value = re.sub(r'\s{2,}', '', value)
        print("|%s|%s|" % (label, value))

def print_reference(cve):
    reference = {
        'Redhat':'https://access.redhat.com/security/cve/%s' % cve,
        'Debian':'https://security-tracker.debian.org/tracker/%s' % cve,
        'NVD':'https://web.nvd.nist.gov/view/vuln/detail?vulnId=%s' % cve,
        'CERT':'https://www.kb.cert.org/vuls/byid?query=%s&searchview=' % cve,
        'LWN':'https://lwn.net/Search/DoSearch?words=%s' % cve,
        'oss-sec':'https://marc.info/?s=%s&l=oss-security' % cve,
        'fulldisc':'https://marc.info/?s=%s&l=full-disclosure' % cve,
        'bugtraq':'https://marc.info/?s=%s&l=bugtraq' % cve,
        'exploitdb':'https://www.exploit-db.com/search/?action=search&cve=%s' % cve.replace('CVE-',''),
        'metasploit':'https://www.rapid7.com/db/search?q=%s' % cve,
        'Ubuntu':'https://people.canonical.com/~ubuntu-security/cve/%s.html' % cve,
        'Github':'https://github.com/search?q="%s"' % cve,
        'PacketStorm':'https://packetstormsecurity.com/search/?q=%s' % cve,
        'bugzilla':'https://bugzilla.redhat.com/show_bug.cgi?id=%s' % cve,
        'twitter':'https://twitter.com/search?q=%s' % cve,
        'centos':'https://www.centos.org/forums/search.php?keywords=%s' % cve,
        'cvedetail':'http://www.cvedetails.com/cve/%s/' % cve,
    }

    for k,v in sorted(reference.items()):
        print(" * [%s](%s)" % (k, v))

# option parser
parser = argparse.ArgumentParser(description='generate report for vlunnerability')
parser.add_argument('cve', help="target cve nunmber")
args = parser.parse_args()

# validation
cve = args.cve.upper()
if not re.match(r"^CVE-\d{4}-\d{4}$" , cve): error("invalid cve format")

print('#', cve)
print()
print('## 概要')
print()
print('## CVSS v3')
print()
print_nvd_info_table(cve)
print()
print('## 解決策、緩和策情報')
print()
print('## 影響を受けるソフトウェアとバージョン')
print()
print('## 技術的な詳細')
print()
print('## 追跡が必要な情報源')
print()
print_reference(cve)
print()

