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

############################## Global Variables ################################

# Datasets:
id_2_object = {}
seen_datasets = set()
seen_softwares = set()
seen_urls = set()

# Definitions:
re_json = re.compile(r".json")
re_mkdn = re.compile(r".md")
re_mdta = re.compile(r"~~~metadata")
re_dlim = re.compile(r"~~~")
metadata_path = "data/catalog-data-caida-metadata.json"

# File Paths:
path = None

################################# Main Method ##################################

def main(argv):
    global path

    parser = argparse.ArgumentParser()
    parser.add_argument("-p", type=str, default=None, dest="path", help="Path to catalog-data-caida/sources")
    args = parser.parse_args()

    # Edge Case: Exit if no path given.
    if args.path == None:
        return
    else:
        path = args.path

    # Edge Case: Exit if path given doesn't exist.
    if not os.path.exists(path):
        return

    update_seen_datasets()
    update_seen_softwares()
    parse_catalog_data_caida()
    print_datasets()

############################### Helper Methods #################################

# Map all known dataset ID's to seen_datasets.
def update_seen_datasets():
    global seen_datasets
    global seen_urls

    # Iterate over each dataset JSON and keep track of their IDs.
    for file in os.listdir("sources/dataset"):
        # Edge Case: Skip if file is not a .json file.
        if not re_json.search(file):
            continue
        
        # Open the file to grab the URL.
        with open("sources/dataset/{}".format(file), "r") as curr_file:
            curr_file = json.load(curr_file)
            if "resources" in curr_file:
                for resource in curr_file["resources"]:
                    if "url" in resource:
                        url = resource["url"]
                        if "/active" in url:
                            seen_urls.add(url.replace("/active", ""))
                        seen_urls.add(url)


        seen_datasets.add(file[:file.index(".")])


# Map all known software ID's to seen_softwares.
def update_seen_softwares():
    global seen_softwares
    global seen_urls

    # Iterate over each software JSON and keep track of their IDs.
    for file in os.listdir("sources/software"):
        # Edge Case: Skip if file is not a .json file.
        if not re_json.search(file):
            continue

        # Open the file to grab the URL.
        with open("sources/software/{}".format(file), "r") as curr_file:
            curr_file = json.load(curr_file)
            if "resources" in curr_file:
                for resource in curr_file["resources"]:
                    if "url" in resource:
                        url = resource["url"]
                        if "/active" in url:
                            seen_urls.add(url.replace("/active", ""))
                        seen_urls.add(url)
        
        seen_softwares.add(file[:file.index(".")])


# Parse of all .md objects in catalog-data-caida/sources.
def parse_catalog_data_caida():
    global id_2_object
    global seen_datasets
    global seen_softwares
    global seen_urls
    global re_mkdn
    global re_mdta
    global re_dlim
    global path

    # Iterate over each file in catalog-data-caida/sources.
    for file in os.listdir(path):
        # Edge Case: Skip if file is not a .md file.
        if not re_mkdn.search(file):
            continue

        file_name = file[:file.index(".")].replace("-", "_")
        file_path = "{}{}".format(path, file)

        # Edge Case: Skip files that have already been seen.
        if file_name in seen_datasets or file_name in id_2_object:
            continue     

        # Edge Case: Skip any seen softwares.
        if "tool_" in file_name and file_name[file_name.index("_") + 1 :] in seen_softwares:
                continue

        # Iterate over file and grab all the metadata.
        with open(file_path, "r") as curr_file:
            found_metadata = False
            curr_metadata = ""
            curr_line = curr_file.readline()
            while curr_line:
                # Base Case: Start parsing metadata once starting delim found.
                if re_mdta.search(curr_line):
                    found_metadata = True
                    curr_line = curr_file.readline()
                    continue

                # Base Case: End parsing curr_file once ending delim found.
                if re_dlim.search(curr_line) and not re_mdta.search(curr_line):
                    # Replace Markdown Syntax to human readable.
                    curr_metadata = curr_metadata.replace('\\"', "'")
                    curr_metadata = json.loads(curr_metadata)

                    # Edge Case: Don't add objects with duplicate urls.
                    if "resources" in curr_metadata:
                        for resource in curr_metadata["resources"]:
                            if "url" in resource:
                                if resource["url"] in seen_urls:
                                    found_metadata = False
                                elif "{}/".format(resource["url"]) in seen_urls:
                                    found_metadata = False
                                else:
                                    seen_urls.add(resource["url"]) 
                    break

                # Parse all data within the metadata block.
                if found_metadata:
                    curr_metadata += curr_line.strip()

                curr_line = curr_file.readline()

        # Parse the curr_metadata for JSON object.
        if found_metadata:
            id_2_object[file_name] = curr_metadata


# Print all found datasets to individual JSON objects.
def print_datasets():
    global id_2_object

    # Iterate over each file and make individual JSON objects.
    for file_id in id_2_object:
        # Edge Case: Update path based which software or dataset.
        if "tool_" in file_id:
            file_name = file_id[file_id.index("_") + 1:] 
            file_path = "sources/software/{}__caida.json".format(file_name)
        else:
            file_path = "sources/dataset/{}__caida.json".format(file_id)

        curr_file = json.dumps(id_2_object[file_id], indent=4)
        with open(file_path, "w") as output_file:
            output_file.write(curr_file)
        

# Run the script given the inputs from the terminal.
main(sys.argv[1:])