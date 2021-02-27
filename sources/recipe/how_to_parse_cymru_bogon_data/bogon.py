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
import argparse
import pyasn
import numpy as np
import os

################################# Main Method ##################################
def main():
    parser = argparse.ArgumentParser(description='Checks whether an array of addresses is bogon.')
    parser.add_argument('bogon', metavar='b', type=str,
                        help='path to bogon dataset')

    parser.add_argument('ips', metavar='i', nargs='+', type=str,
                        help='list of ip addresses')

    args = parser.parse_args()
    bogondb = bogon_load(args.bogon)
    return bogon_check_ip(args.ips, bogondb)
    
############################### Helper Methods #################################
def bogon_load(path):
    """
    Loads bogon dataset into memory.
    """
    temp_file = "_bogon.dat"
    f = open(path, "r")
    ips = []
    next(f)
    for line in f.readlines():
        ips.append(line.replace('\n',"") + "\t1")
    hdrtxt = '; IP-ASN32-DAT file\n; Original file : <Path to a rib file>\n; Converted on  : temp\n; CIDRs         : 512490\n;'
    np.savetxt(temp_file, ips, header=hdrtxt,fmt='%s')
    bogondb = pyasn.pyasn('_bogon.dat')
    os.remove(temp_file)
    return bogondb

def bogon_check_ip(ips, bogondb):
    """
    Checks whether a given IP address is bogon
    """
    is_bogon = [False]*len(ips)
    for index in range(len(ips)):
        # Check if IP is valid
        try:
            bogondb.lookup(ips[index])
        except ValueError:
            print("Invalid IP: ", ips[index])
            continue
        
        # Look up IP
        if bogondb.lookup(ips[index])[1]:
            is_bogon[index] = True
        else:
            continue
    print(is_bogon)

if __name__ == '__main__':
    main()