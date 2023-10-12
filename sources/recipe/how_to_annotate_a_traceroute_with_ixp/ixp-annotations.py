# Copyright (c) 2020 The Regents of the University of California
# All Rights Reserved

#!  /usr/bin/env python3
__author__ = "Nicole Lee"
__email__ = "nlee@zeus.caida.org"
# This software is Copyright (C) 2020 The Regents of the University of
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

################################## Imports #####################################
import json
import argparse
import numpy as np
import pyasn
import os

################################# Main Method ##################################
def main():
    parser = argparse.ArgumentParser(description='Finds IXP annotations.')
    parser.add_argument('path', metavar='p', type=str,
                        help='path to ixp dataset')
    parser.add_argument('list', metavar='l', nargs='+', type=str,
                        help='list of ip addresses')
    args = parser.parse_args()

    ixpdb, diction = load_traceroute(args.path)
    return annotate_traceroute(ixpdb, diction, args.list)

############################### Helper Methods #################################
def load_traceroute(path):
    temp_file = "_ixp.dat"
    with open(path) as f:
        next(f)
        data = []
        diction = {}
        i = 1
        for line in f:
            obj = json.loads(line)
            name = obj['name']
            diction[i] = name
            recorded_ipv4 = list(map(lambda x: x+"\t%d"%i, obj['prefixes']['ipv4']))
            recorded_ipv6 = list(map(lambda x: x+"\t%d"%i, obj['prefixes']['ipv6']))
            data+=(recorded_ipv4+recorded_ipv6)
            i+=1
        hdrtxt = '; IP-ASN32-DAT file\n; Original file : <Path to a rib file>\n; Converted on  : temp\n; CIDRs         : 512490\n;'
        np.savetxt(temp_file, data, header=hdrtxt,fmt='%s')
        ixpdb = pyasn.pyasn(temp_file)
        os.remove(temp_file)
        return ixpdb, diction


def annotate_traceroute(ixpdb, diction, ips):
    """
    Inputs a path to data file and a list of IP addresses and returns a corresponding list of IXP names.
    """
    # Converts all into IP address format, appends None if not IP address
    ixp_list = [None]*len(ips)
    for index in range(len(ips)):
        try:
            ixpdb.lookup(ips[index])
        except ValueError:
            print("Invalid IP: ", ips[index])
            continue  
        if ixpdb.lookup(ips[index])[1]:
            ixp_list[index] = diction[ixpdb.lookup(ips[index])[0]]
        else:
            continue                
    print(ixp_list)

if __name__ == '__main__':
    main()
