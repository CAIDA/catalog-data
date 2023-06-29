# Copyright (c) 2023 The Regents of the University of California
# All Rights Reserved

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

# Definitions:
re_bz2 = re.compile(r".bz2$")
re_txt = re.compile(r".txt$")

# File Paths:
ppdc_ases_file = None

################################# Main Method ##################################

def main(argv):
    global as_2_cone
    global re_bz2
    global re_txt
    global ppdc_ases_file

    parser = argparse.ArgumentParser()
    parser.add_argument("-p", type=str, default=None, dest="ppdc_ases_file", help="Path to an IPv4, .ppdc-ases formatted file.")
    args = parser.parse_args() 

    # Create IPv4 as_2_cone dataset if .ppdc-ases file is given.
    if args.ppdc_ases_file is not None:
        ppdc_ases_file = args.ppdc_ases_file
        parse_ppdc_ases_file()

    # Edge Case: Print help and exit if prior conditions weren't met.
    else:
        print_help()

############################### Helper Methods #################################

def print_help():
    sys.stderr.write("python3 as-customer-cone.py -p /data/external/as-rank-ribs/20200101/20200101.ppdc-ases.txt.bz2")
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
    as_2_cone[asn]["cone"] = customer_cone[1:]
    as_2_cone[asn]["size"] = customer_cone_size

# Run the script given the inputs from the terminal.
main(sys.argv[1:])
