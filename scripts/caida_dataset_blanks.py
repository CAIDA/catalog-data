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
import re
import os

#################################### Header ####################################

"""
    This script will produce blank JSON objects (datasets, software, etc) based
    on data/data_id__caida.json which is a JSON mapping a file paths to an ID of
    an object that needs to be made. The optional input -i overrides the path to
    a different JSON list of paths and IDs. For each key:value pair, a new JSON
    file is made at the given path with the ID and name with the extension 
    __caida.json.
"""

############################## Global Variables ################################

# File Paths:
path_ids = "data/data_id___caida.json"

################################# Main Method ##################################

def main(argv):
    global path_ids

    parser = argparse.ArgumentParser()
    parser.add_argument("-i", type=str, default=None, dest="path_ids", help="Path to a json file to map file paths to IDs.")
    args = parser.parse_args()

    # Assign a given path_ids value, else use the default.
    if args.path_ids != None:
        path_ids = args.path_ids
    
    # Print all datasets listed to their paths with just IDs.
    print_datasets()

############################### Helper Methods #################################

# Print all found datasets to individual JSON objects.
def print_datasets():
    global path_ids

    # Load the JSON file into a dictionary.
    with open(path_ids, "r") as id_file:
        path_2_id = json.load(id_file)

    # Iterate over each path and make a blank JSON file for them.
    for path in path_2_id:
        data = { 
            "id":path_2_id[path],
            "name":path_2_id[path].upper().replace("_", " ")
        }

        with open(path, "w") as output_file:
            output_file.write(json.dumps(data, indent=4))


# Run the script given the inputs from the terminal.
main(sys.argv[1:])
