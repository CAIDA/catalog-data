# Copyright (c) 2023 The Regents of the University of California
# All Rights Reserved

#!/usr/bin/env python2
__author__ = "Bradley Huffaker"
__email__ = "<bradley@caida.org>"
# This software is Copyright (C) 2022 The Regents of the University of
# California. All Rights Reserved. Permission to copy, modify, and
# distribute this software and its documentation for educational, research
# and non-profit purposes, without fee, and without a written agreement is
# hereby granted, provided that the above copyright notice, this paragraph
# and the following three paragraphs appear in all copies. Permission to
# make commercial use of this software may be obtained by contacting:
#
# Office of Innovation and Commercialization
# 9500 Gilman Drive, Mail Code 0910
# University of California
# La Jolla, CA 92093-0910
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
#

#import the low level _pybgpsteam library and other necessary libraries
from pybgpstream import BGPStream
from datetime import date
from datetime import timedelta
import argparse

import sys
import bz2

parser = argparse.ArgumentParser()
parser.add_argument("link_file", nargs=1, type=str)
parser.add_argument("-d", "--debug", type=int, default=-1)
args = parser.parse_args()

def main():
    sys.stderr.write("This is going to take some time\n")

    # Handle debug option
    debug_count = args.debug

    peer_provider = download_links(args.link_file[0])
    asn__cone = download_paths(peer_provider, debug_count)

    print "# ASN followed by ASNs in it's customer cone"
    print "# '1 23 4' means  ASN 1's customer cone includes ASN 23 and ASN 4"
    for asn,cone in sorted(asn__cone.items(), key=lambda a_c: len(a_c[1]),reverse=True):
        print asn + " "+" ".join(sorted(cone,key=lambda a: int(a.lstrip('{').rstrip('}'))))

# Find the set of AS Relationships that are 
# peer to peer or provider to customer.
def download_links(filename):
    sys.stderr.write("loading relationships\n")
    first = 1000
    offset = 0
    hasNextPage = True

    peer_provider = set()
    with bz2.BZ2File(filename, mode='r') as fin:
        for line in fin:
            # skip comments
            if len(line) == 0 or line[0] == "#":
                continue
            asn0, asn1, rel = line.rstrip().split("|")

            # peers work in both directions
            if rel == 0:
                peer_provider.add(asn1+" "+asn0)
                peer_provider.add(asn0+" "+asn1)

            # store the link from provider to customer 
            elif rel == -1:
                peer_provider.add(asn1+" "+asn0)
            else:
                peer_provider.add(asn0+" "+asn1)

    return peer_provider

# download the AS paths from BGPStream
# crop the path to the section after the 
# first peer or provider link, then add
# all the remaining ASes to the preceeding 
# ASes in the cropped path
def download_paths(peer_provider, debug_count):
    # The set of ASes reachable through an AS's customers
    asn__cone = {}

    sys.stderr.write("downloading paths\n")

    # Return a rib from yesterday's first second
    from_time = date.today() - timedelta(days=1)
    until_time = from_time + timedelta(seconds=1)
    stream = BGPStream(
        from_time=from_time.strftime("%Y-%m-%d %H:%M:%S"), until_time=until_time.strftime("%Y-%m-%d %H:%M:%S"),
        record_type="ribs"
    )
    stream.add_rib_period_filter(86400) # This should limit BGPStream to download the full first BGP dump

    # counter
    count = 0
    for elem in stream:
        # Break when debug mode activated and count equals debug count
        if (debug_count >= 0) and (count >= debug_count):
            break

        asns = elem.fields['as-path'].split(" ")

        # Skip until the first peer-peer or provider->customer link
        i = 0
        while i+1 < len(asns):
            link = asns[i]+" "+asns[i+1] 
            i += 1
            if link in peer_provider:
                break

        # Since an AS only announces it's customer cone to it's peer or provider,
        # the remaining ASes in the path are in the preciding ASes customer cone.
        while i+1 < len(asns):
            if asns[i] not in asn__cone:
                asn__cone[asns[i]] = set()
            cone = asn__cone[asns[i]]
            j = i+1
            while j < len(asns):
                print (">",i,j,asns[i], asns[j])
                cone.add(asns[j])
                j += 1
            i += 1

        # Increment count
        count += 1

    return asn__cone

#run the main method
main()
