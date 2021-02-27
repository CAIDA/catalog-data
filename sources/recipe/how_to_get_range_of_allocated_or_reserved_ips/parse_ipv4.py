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
import pandas as pd
import sys
import more_itertools as mit

################################# Main Method ##################################
def main():
    print(parse_ip_assignees(sys.argv[1]), parse_ip_compressed(sys.argv[1]))

############################### Helper Methods #################################
def parse_ip_assignees(csv_path):
    """
    Parses the IP address csv to ranges in which designations occupy. Takes in a path to the csv file and outputs a dictionary.
    """
    ip = pd.read_csv(csv_path).reset_index()
    ip["Designation"] = ip["Designation"].apply(lambda x: x.lower().replace("administered by", "").strip())

    consec = (lambda x: [list(group) for group in mit.consecutive_groups(list(x))])

    ip = (ip.drop(ip.columns.difference(["index","Designation"]), axis=1)
    .groupby(["Designation"])["index"]
    .apply(lambda x: [[y[0], y[-1]] for y in consec(x)])
    .to_dict())
    return ip

def parse_ip_compressed(csv_path):
    """
    Parses the IP address csv to ranges IP addresses are either reserved, allocated, or legacy. Takes in a path to the csv file and outputs a dictionary.
    """
    ip = pd.read_csv(csv_path).reset_index()
    ip["Status [1]"] == ip["Status [1]"].apply(lambda x: x.lower())

    consec = (lambda x: [list(group) for group in mit.consecutive_groups(list(x))])

    ip = (ip.drop(ip.columns.difference(["index","Status [1]"]), axis=1)
    .groupby(["Status [1]"])["index"]
    .apply(lambda x: [[y[0], y[-1]] for y in consec(x)])
    .to_dict())
    return ip

if __name__ == "__main__":
    main()
