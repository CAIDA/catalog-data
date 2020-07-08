__author__ = "Pooja Pathak"
__email__ = "<pmpathak@ucsd.edu>"
# This software is Copyright © 2020 The Regents of the University of
# California. All Rights Reserved. Permission to copy, modify, and
# distribute this software and its documentation for educational, research
# and non-profit purposes, without fee, and without a written agreement is
# hereby granted, provided that the above copyright notice, this paragraph
# and the following three paragraphs appear in all copies. Permission to
# make commercial use of this software may be obtained by contacting:
#
# Office of Innovation and Commercialization
#
# 9500 Gilman Drive, Mail Code 0910
#
# University of California
#
# La Jolla, CA 92093-0910
#
# (858) 534-5815
#
# invent@ucsd.edu
#
# This software program and documentation are copyrighted by The Regents of
# the University of California. The software program and documentation are
# supplied “as is”, without any accompanying services from The Regents. The
# Regents does not warrant that the operation of the program will be
# uninterrupted or error-free. The end-user understands that the program
# was developed for research purposes and is advised not to rely
# exclusively on the program for any reason.
#
# IN NO EVENT SHALL THE UNIVERSITY OF CALIFORNIA BE LIABLE TO ANY PARTY FOR
# DIRECT, INDIRECT, SPECIAL, INCIDENTAL, OR CONSEQUENTIAL DAMAGES,
# INCLUDING LOST PR OFITS, ARISING OUT OF THE USE OF THIS SOFTWARE AND ITS
# DOCUMENTATION, EVEN IF THE UNIVERSITY OF CALIFORNIA HAS BEEN ADVISED OF
# THE POSSIBILITY OF SUCH DAMAGE. THE UNIVERSITY OF CALIFORNIA SPECIFICALLY
# DISCLAIMS ANY WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE. THE
# SOFTWARE PROVIDED HEREUNDER IS ON AN “AS IS” BASIS, AND THE UNIVERSITY OF
# CALIFORNIA HAS NO OBLIGATIONS TO PROVIDE MAINTENANCE, SUPPORT, UPDATES,
# ENHANCEMENTS, OR MODIFICATIONS.

#!/usr/bin/env python

import _pyipmeta 
import datetime
import os 
import psutil

def returnTime():
    return datetime.datetime.now()

def returnMemUsage():
    process = psutil.Process(os.getpid())
    return process.memory_info()[0]
    

ipm = _pyipmeta.IpMeta()
# print(ipm)

# print("Getting/enabling pfx2as provider (using included test data)")
prov = ipm.get_provider_by_name("pfx2as")
# print(prov)
print(ipm.enable_provider(prov, "-f /test/pfx2as/routeviews-rv2-20170329-0200.pfx2as.gz"))
print()


ips = []
with open('ips.txt') as f:
    for line in f:
        line = line.rstrip().split("\t")[1]
        ips.append(line)

begin_time = returnTime()
begin_mem = returnMemUsage()  

ip2asn = {}
for ip in ips:
    if ipm.lookup(ip):
        (res,) =  ipm.lookup(ip)
        if res.get('asns'):
            ip2asn[ip] = res.get('asns')


# print(ip2asn)
end_time = returnTime()
end_mem = returnMemUsage()

# hour:minute:second:microsecond
print("Delta time:" , end_time - begin_time)
print("Delta memory:", end_mem - begin_mem)
