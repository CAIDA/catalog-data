
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

# Datasets
pair_2_rel = {}
"""
{
    "asn0 asn1" : -1/0/1
}
"""

# Definitions:
re_bz2 = re.compile(r".bz2$")
re_txt = re.compile(r".txt$")

# File Path:
as_rel_file = None

################################# Main Method ##################################

def main(argv):
    global pair_2_rel
    global re_bz2
    global re_txt
    global as_rel_file

    parser = argparse.ArgumentParser()
    parser.add_argument("-r", type=str, default=None, dest="as_rel_file", help="Path to a .as-rel formatted file.")
    args = parser.parse_args()

    if args.as_rel_file is None:
        print_help()

    as_rel_file = args.as_rel_file

    parse_as_rel_file()

############################### Helper Methods #################################

def print_help():
    sys.stderr.write("python3 pair_2_rel.py -r 20200101.as-rel.txt")
    sys.exit()


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
    global pair_2_rel

    # Edge Case: Skip any commented lines.
    if curr_line[0] == "#":
        return

    as_rel_set = curr_line.split("|")
        
    # Get each piece of data from the current line.
    asn0 = as_rel_set[0]
    asn1 = as_rel_set[1]
    relationship = int(as_rel_set[2])

    # Place both related AS's in par_2_re; based om value of ASes.
    if (asn0 > asn1):
        temp = asn0
        asn0 = asn1
        asn1 = temp
        relationship = -1 * relationship

    key = asn0 + " " + asn1

    # Add the pair's relationship if doesn't already exist.
    if key not in pair_2_rel:
        pair_2_rel[key] = relationship


# Helper function to return the relationship of two given asns. 
def get_relationship(asn0, asn1):
    global pair_2_rel

    if (asn0 > asn1):
        temp = asn0
        asn0 = asn1
        asn1 = temp

    key = str(asn0) + " " + str(asn1)

    if key in pair_2_rel:
        rel = pair_2_rel[key]
        return rel
        # return "asn0: " + str(asn0) + " asn1: " + str(asn1) + " rel: " + rel
    else:
        return None

# Run the script given the inputs from the terminal.
main(sys.argv[1:])