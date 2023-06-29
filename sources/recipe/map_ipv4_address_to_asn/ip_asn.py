# Copyright (c) 2023 The Regents of the University of California
# All Rights Reserved

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

import pyasn
import argparse 
import datetime
import resource
import os
import psutil

def returnTime():
    return datetime.datetime.now()

def returnMemUsage():
    process = psutil.Process(os.getpid())
    return process.memory_info()[0]
    

parser = argparse.ArgumentParser()
parser.add_argument('-p', dest = 'prefix2asn_file', default = '', help = 'Please enter the prefix2asn file name')
parser.add_argument('-i', dest = 'ips_file', default = '', help = 'Please enter the file name of the ips file')
args = parser.parse_args()


# Get list of ips 
ips = []
with open(args.ips_file) as f:
    for line in f:
        line = line.rstrip().split("\t")[1]
        ips.append(line)


asndb = pyasn.pyasn(args.prefix2asn_file)

begin_time = returnTime()
begin_mem = returnMemUsage() 

# Create ip2asn mapping
ip2asn = {}
for ip in ips:
    if asndb.lookup(ip):
        asn,prefix =  asndb.lookup(ip)
        if asn:
             ip2asn[ip] = asn

# print(ip2asn)
end_time = returnTime()
end_mem = returnMemUsage()

# hour:minute:second:microsecond
print("Delta time:" , end_time - begin_time)
print("Delta memory use:", end_mem - begin_mem)

    


