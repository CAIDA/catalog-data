#!  /usr/bin/env python3
__author__ = "Donald Wolfson"
__email__ = "dwolfson@zeus.caida.org"
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
import sys
import os
import bz2
import re

############################## Global Variables ################################

# Datasets:
as_2_cone = {}
as_pair_2_rel = {}

# Definitions:
re_bz2 = re.compile(r".bz2$")
re_txt = re.compile(r".txt$")

# File Paths:
ppdc_ases_file = None
paths_file = None
as_rel_file = None


################################# Main Method ##################################

def main(argv):
    global as_2_cone
    global as_pair_2_rel
    global re_bz2
    global re_txt
    global ppdc_ases_file
    global paths_file
    global as_rel_file

    parser = argparse.ArgumentParser()
    parser.add_argument("-p", type=str, default=None, dest="ppdc_ases_file", help="Path to an IPv4, .ppdc-ases formatted file.")
    parser.add_argument("-P", type=str, default=None, dest="paths_file", help="Path to an IPv6, .stable.paths6 formatted file.")
    parser.add_argument("-r", type=str, default=None, dest="as_rel_file", help="Path to an IPv6, .as-rel.v6-stable formatted file.")
    args = parser.parse_args() 

    # Create IPv4 as_2_cone dataset if .ppdc-ases file is given.
    if args.ppdc_ases_file is not None:
        ppdc_ases_file = args.ppdc_ases_file
        parse_ppdc_ases_file()

    # Create IPv6 as_2_cone dataset if both .paths and .as-rel file given.
    elif args.paths_file is not None and args.as_rel_file is not None:
        paths_file = args.paths_file
        as_rel_file = args.as_rel_file
        parse_as_rel_file()
        parse_paths_file()

    # Edge Case: Print help and exit if prior conditions weren't met.
    else:
        print_help()

############################### Helper Methods #################################

def print_help():
    sys.stderr.write("python3 as-customer-cone.py -p /data/external/as-rank-ribs/20200101/20200101.ppdc-ases.txt.bz2")
    sys.stderr.write("python3 as-customer-cone.py -P /data/external/as-rank-ribs/20200101/20200101.stable.paths6.bz2 -r /data/external/as-rank-ribs/20200101/20200101.as-rel.v6-stable.txt.bz2")
    sys.exit()

# Open the given .ppdc-ases file and run parse uncommented line.
def parse_ppdc_ases_file():
    global ppdc_ases_file 
    global re_bz2
    global re_txt

    # Parse ppdc_ases_file as an encoded .bz2 file.
    if re_bz2.search(ppdc_ases_file):
        with bz2.open(ppdc_ases_file, "r") as file:
            curr_line = file.readline()
            while curr_line:
                curr_line = curr_line.decode()
                parse_ppdc_ases_line(curr_line)
                curr_line = file.readline()
    
    # Parse ppdc_ases_file as a .txt file.
    elif re_txt.search(ppdc_ases_file):
        with open(ppdc_ases_file, "r") as file:
            curr_line = file.readline()
            while curr_line:
                parse_ppdc_ases_line(curr_line)
                curr_line = file.readline()
    
    # Exit if file is neither a .bz2 or .txt file type.
    else:
        sys.stderr.write("ppdc_ases_file must be a .txt or encoded .bz2 file.")
        print_help()


# Given an line of a .ppdc-ases file, get the asn and its Customer Cone.
def parse_ppdc_ases_line(curr_line):
    global as_2_cone

    # Edge Case: Skip any commented lines.
    if curr_line[0] == "#":
        return

    customer_cone = curr_line.split()
    asn = int(customer_cone[0])
    customer_cone_size = len(customer_cone[1:])

    # Update as_2_cone with this asn's customer_cone_size.
    if asn not in as_2_cone:
        as_2_cone[asn] = {}
    
    as_2_cone[asn]["asn"] = asn
    as_2_cone[asn]["cone"] = customer_cone
    as_2_cone[asn]["size"] = customer_cone_size


# Open the as_rel_file and parse each line in a helper method.
def parse_as_rel_file():
    global as_rel_file
    global re_bz2
    global re_txt

    # Parse as_rel_file as an encoded .bz2 file.
    if re_bz2.search(as_rel_file):
        with bz2.open(as_rel_file, "r") as file:
            curr_line = file.readline()
            while curr_line:
                curr_line = curr_line.decode()
                parse_as_rel_line(curr_line)
                curr_line = file.readline()
    
    # Parse as_rel_file as a .txt file.
    elif re_txt.search(as_rel_file):
        with open(as_rel_file, "r") as file:
            curr_line = file.readline()
            while curr_line:
                parse_as_rel_line(curr_line)
                curr_line = file.readline()
    
    # Exit if file is neither a .bz2 or .txt file type.
    else:
        sys.stderr.write("as_rel_file must be in a .txt or encoded .bz2 file.")
        print_help()


# Parse a given line of the as_rel_file and map two ASes to their relationship.
def parse_as_rel_line(curr_line):
    global as_pair_2_rel

    # Edge Case: Skip any commented lines.
    if curr_line[0] == "#":
        return

    as_rel_set = curr_line.split("|")
        
    # Get each piece of data from the current line.
    asn0 = as_rel_set[0]
    asn1 = as_rel_set[1]
    relationship = int(as_rel_set[2])

    # Place both related AS's in as_pair_2_rel based value of AS.
    if (asn0 > asn1):
        temp = asn0
        asn0 = asn1
        asn1 = temp
        relationship = -1 * relationship

    key = asn0 + " " + asn1

    # Add the pair's relationship if doesn't already exist.
    if key not in as_pair_2_rel:
        as_pair_2_rel[key] = relationship


# Open the paths_file and parse each line in a helper method.
def parse_paths_file():
    global paths_file
    global re_bz2
    global re_txt

    # Parse paths_file as an encoded .bz2 file.
    if re_bz2.search(paths_file):
        with bz2.open(paths_file, "r") as file:
            curr_line = file.readline()
            while curr_line:
                curr_line = curr_line.decode()
                parse_paths_line(curr_line)
                curr_line = file.readline()
    
    # Parse paths_file as a .txt file.
    elif re_txt.search(paths_file):
        with open(paths_file, "r") as file:
            curr_line = file.readline()
            while curr_line:
                parse_paths_line(curr_line)
                curr_line = file.readline()
    
    # Exit if file is neither a .bz2 or .txt file type.
    else:
        sys.stderr.write("paths_file must be in a .txt or encoded .bz2 file.")
        print_help
        

# Given a line from a .paths file update as_2_cone with an asn's cone and size.
def parse_paths_line(curr_line):
    global as_2_cone
    global as_pair_2_rel

    # Edge Case: Skip any commented lines.
    if curr_line[0] == "#":
        return

    asns = curr_line.rstrip().split("|")
    for i in range(0, len(asns)):
        asn = int(asns[i])
        
        # Map the current asn if the asn is not in as_2_cone yet.
        if asn not in as_2_cone:
            as_2_cone[asn] = {}
            as_2_cone[asn]["asn"] = asn
            as_2_cone[asn]["cone"] = [asn]
            as_2_cone[asn]["size"] = 1

        # Compare asns[i] to each asn that comes after it.
        for j in range(i + 1, len(asns)):
            key = format_key(asn, int(asns[j]))
            
            # Add asns with a "provider" relationship between: asn[i] asn[j]
            if key in as_pair_2_rel and as_pair_2_rel[key] == 1:
                as_2_cone[asn]["size"] += 1
                as_2_cone[asn]["cone"].append(int(asns[j]))
            else:
                break   


# Helper function to format two given asns into a key for as_pair_2_rel. 
def format_key(asn0, asn1):
    if (asn0 > asn1):
        temp = asn0
        asn0 = asn1
        asn1 = temp

    return str(asn0) + " " + str(asn1)

# Run the script given the inputs from the terminal.
main(sys.argv[1:])