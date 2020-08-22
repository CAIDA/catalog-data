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
import json
import bz2
import re

############################## Global Variables ################################

# Dataset:
as_2_class = {}                     # The finalized dataset of classifications.
"""
{
    "asn0" : "transit free",        # asn0 has zero providers.
    "asn1" : "middle",              # asn1 has both providers and customers.
    "asn2" : "edge"                 # asn2 has zero customers.
}
"""
as_2_data = {}                      # Dataset that is updated during API calls.
"""
{
    "asn0" : {
        "providers" : set(),        # Set of asns that are providers to asn0.
        "customers" : set()         # Set of asns that are customers to asn0.
    }
}
"""

# Definitions:
re_bz2 = re.compile(r".bz2$")
re_txt = re.compile(r".txt$")
rel_2_name = {
    -1 : "customer",
    0: "peer",
    1: "provider"
}

# File Path:
as_rel_file = None                  # Path to a local .as-rel file.

################################# Main Method ##################################

def main(argv):
    global as_2_class
    global as_2_data
    global as_rel_file

    parser = argparse.ArgumentParser()
    parser.add_argument("-r", type=str, default=None, dest="as_rel_file", help="Path to a AS Relationship (.as-rel) file.")
    args = parser.parse_args()

    # Edge Case: Exit if no .as-rel file was given to be found.
    if args.as_rel_file is None:
        print("     Must provide a .as-rel file:", sys.argv[0], " -r 20200101.as-rel.txt", file=sys.stderr)
        sys.exit()

    as_rel_file = args.as_rel_file

    parse_as_rel_file()
    update_classifications()
    print_classifications()

############################### Helper Methods #################################

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
        print("as_rel_file must be in a .txt or encoded .bz2 file.", file=sys.stderr)
        sys.exit()


# Helper method that takes in a line from the .as-rel file to update as_2_data.
def parse_as_rel_line(curr_line):
    global as_2_data
    global rel_2_name

    # Edge Case: Skip any commented lines.
    if curr_line[0] == "#":
        return

    # curr_line format: <asn0>|<asn1>|<relationship>
    asn0, asn1, relationship = curr_line.split("|")

    # Edge Case: Create objects for asn0 or asn1 if they are not in as_2_data.
    if asn0 not in as_2_data:
        as_2_data[asn0] = {
            "providers" : set(),
            "customers" : set()
        }
    if asn1 not in as_2_data:
        as_2_data[asn1] = {
            "providers" : set(),
            "customers" : set()
        }
    
    # If asn0's provider is asn1 add to asn0's customers, and asn1's providers.
    if rel_2_name[int(relationship)] == "provider":
        as_2_data[asn0]["providers"].add(asn1)
        as_2_data[asn1]["customers"].add(asn0)
    # Else if asn0's customer is asn1.
    elif rel_2_name[int(relationship)] == "customer":
        as_2_data[asn0]["customers"].add(asn1)
        as_2_data[asn1]["providers"].add(asn0)


# Helper method use to update as_2_class with data from as_2_data.
def update_classifications():
    global as_2_class
    global as_2_data

    # Iterate over each asn in as_2_data.
    for asn in as_2_data:
        # Edge Case: Create a dictionary for the asn if it doesnn't exist.
        if asn not in as_2_class:
            as_2_class[asn] = {
                "asn" : asn,
                "class" : None
            }
        # If asn has no providers, then it is transit free.
        if len(as_2_data[asn]["providers"]) == 0:
            as_2_class[asn]["class"] = "transit free" 
        # Else if asn has no customers. then it is an edge.
        elif len(as_2_data[asn]["customers"]) == 0:
            as_2_class[asn]["class"] = "edge"
        # Else asn has some providers and customers, then it is a middle.
        else:
            as_2_class[asn]["class"] = "middle"


# Helper method that prints all of as_2_class to STDOUT
def print_classifications():
    global as_2_class

    # Iterate over as_2_class and print out each classification.
    for asn in as_2_class:
        sys.stdout.write(json.dumps(as_2_class[asn]) + "\n")

# Run the script given the inputs from the terminal.
main(sys.argv[1:])