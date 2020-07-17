#!/usr/bin/env python
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

import pybgpstream
import os.path

# Create pybgpstream
stream = pybgpstream.BGPStream(
    from_time="2017-07-07 00:00:00", until_time="2017-07-07 00:10:00 UTC",
    collectors=["route-views.sg", "route-views.eqix"],
    record_type="updates",  
)

prefix_asn = dict()
for elem in stream:
    # record fields can be accessed directly from elem
    if "as-path" in elem.fields:
        asns = elem.fields["as-path"].rstrip().split(" ")
    if "prefix" in elem.fields:
        prefix = elem.fields["prefix"]
    

    if len(asns) < 1:
        continue

    # Get origin as 
    asn = asns[-1]

    # Drop origin as sets
    if len(asn.split(",")) > 1:
        continue 

    if asn[0] == '{':
        continue

    # Populate prefix_asn with prefix to asn mapping
    if asn not in prefix_asn:
        prefix_asn[prefix] = set()
    prefix_asn[prefix].add(asn)

# Write prefix-asn mapping to prefix2asn.dat

fout = open('prefix2asn.dat', "w")
for prefix,asns in prefix_asn.items():
    if len(asns) == 1:
        fout.write(prefix)
        fout.write("\t")
        fout.write("".join(prefix_asn[prefix]))
        fout.write("\n")

fout.close() 
