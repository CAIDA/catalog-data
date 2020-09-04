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
import json
import sys
import os
import gzip
import re

############################## Global Variables ################################

# Dataset(s)
as_2_data = {}              # Maps a given asn to it's data from the given file.
"""
{
    "asn0" : {
        "asn" : "asn0",
        "source" : "...",
        "class" : "..."
    }
}
"""
as_2_print = None           # Will hold a list of asns to print from as_2_data.

# Definitions
re_txt = re.compile(r".txt")
re_gzp = re.compile(r".gz")

# File Path(s)
as_2_types_file = None

################################# Main Method ##################################

def main(argv):
    global as_2_data
    global re_txt
    global re_gzp
    global as_2_types_file

    parser = argparse.ArgumentParser()
    parser.add_argument("-f", type=str, default=None, dest="as_2_types", help="Path to a .as2types file. (.txt/.gz)")
    parser.add_argument("-a", type=str, default=None, dest="ases", help="Comma seperate list of asns to print.")
    args = parser.parse_args() 

    # Edge Case: Print help if no file given.
    if args.as_2_types is None:
        print_help()

    # Edge Case: Update as_2_print if -a flag was used.
    if args.ases is not None:
        as_2_print = args.ases.split(",")
    else:
        as_2_print = None

    as_2_types_file = args.as_2_types

    # Updates as_2_data with all values in the given file.
    parse_as_2_types_file()

    # Prints out a json value of a given asn.
    if as_2_print is not None:
        for asn in as_2_print:
            get_asn(asn)

############################### Helper Methods #################################

def print_help():
    print("python3 as_2_class.py -f YYYYMMDD.as2type.txt", file=sys.stderr)
    print("     File formats accepted: .txt, .gz", file=sys.stderr)
    sys.exit()


# Open the given file and parse each line.
def parse_as_2_types_file():
    global re_txt
    global re_gzp
    global as_2_types_file
    
    # Parse as_2_types_file as an encoded .gz file.
    if re_gzp.search(as_2_types_file):
        with gzip.open(as_2_types_file, "r") as file:
            curr_line = file.readline()
            while curr_line:
                curr_line = curr_line.decode()
                parse_as_2_types_line(curr_line)
                curr_line = file.readline()
    
    # Parse as_2_types_file as a .txt file.
    elif re_txt.search(as_2_types_file):
        with open(as_2_types_file, "r") as file:
            curr_line = file.readline()
            while curr_line:
                parse_as_2_types_line(curr_line)
                curr_line = file.readline()
    
    # Exit if file is neither a .gz or .txt file type.
    else:
        print_help()


# Parse a given line to map the current asn to its values.
def parse_as_2_types_line(curr_line):
    global as_2_data

    # Edge Case: Skip commented out lines.
    if curr_line[0] == "#":
        return

    # Remove any trailing characters.
    curr_line = curr_line.rstrip()

    # Split the current line into its three values.
    asn, source, classification = curr_line.split("|")

    # Updated as_2_data with the current line's values.
    as_2_data[asn] = {
        "asn" : asn,
        "source" : source,
        "class" : classification
    }


# Prints the given asn's json data to STDOUT.
def get_asn(asn):
    global as_2_data
    
    # Edge Case: Print error if asn not in as_2_data.
    if asn not in as_2_data:
        print("{} not in as_2_data".format(asn))
    else:
        print(json.dumps(as_2_data[asn]))


# Given an asn, update as_2_data with the given key and value.
def update_as2data(asn, key, value):
    global as_2_data

    # Edge Case: Insert the asn if it doesn't already exist.
    if asn not in as_2_data:
        as_2_data[asn] = {}
    as_2_data[asn][key] = value


# Run the script given the inputs from the terminal.
main(sys.argv[1:])