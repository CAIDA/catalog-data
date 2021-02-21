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
    on the local directory, catalog-data-caida/sources which holds metadata of
    caida datasets and software in markdown files.
    
    The script will first check for all currently available softwares and 
    datasets prior to finding new ones in catalog-data-caida to avoid 
    duplicates. The metadata included will help produce unique JSON objects for
    each file based on what's given. The file also produces a JSON mapping each
    new file path to its ID.
"""


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

# File Paths:
path = None
path_ids = "data/data_id__caida.json"

################################# Main Method ##################################

def main(argv):
    global path
    global path_ids

    parser = argparse.ArgumentParser()
    parser.add_argument("-p", type=str, default=None, dest="path", help="Path to catalog-data-caida/sources")
    parser.add_argument("-i", type=str, default=None, dest="path_ids", help="Path to a json file to map file paths to IDs.")
    args = parser.parse_args()

    # Edge Case: Exit if no path given.
    if args.path == None:
        return
    else:
        path = args.path

    # Edge Case: Exit if path given doesn't exist.
    if not os.path.exists(path):
        return

    # Assign a given path_ids value, else use the default.
    if args.path_ids != None:
        path_ids = args.path_ids

    # Keep track of all existing datasets.
    update_seen_datasets()
    # Keep track of all existing sofwares.
    update_seen_softwares()
    # Parse all .md file in the given path.
    parse_catalog_data_caida()
    # Print all found JSON objects to individual JSON files.
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
                    curr_metadata["id"] = curr_metadata["id"].replace("-", "_")

                    # Edge Case: Replace missing names with ID.
                    if "name" not in curr_metadata:
                        name = curr_metadata["id"].replace("_", " ").upper()
                        curr_metadata["name"] = name

                    # Edge Case: Remove broken tags.
                    for i in range(0, len(curr_metadata["tags"])):
                        if " )" in curr_metadata["tags"][i]:
                            del curr_metadata["tags"][i]

                    # Edge Case: Remove 0 length lists from objects.
                    remove_keys = set()
                    for key in curr_metadata:
                        if len(curr_metadata[key]) == 0:
                            remove_keys.add(key)
                    
                    for key in remove_keys:
                        del curr_metadata[key]
                            
                    break

                # Parse all data within the metadata block.
                if found_metadata:
                    # Don't add lines with messed up metadata.
                    if "Series([]" not in curr_line and "NaN" not in curr_line:
                        curr_metadata += curr_line.strip().replace("\\n", "")

                curr_line = curr_file.readline()

        # Parse the curr_metadata for JSON object.
        if found_metadata:
            id_2_object[file_name] = curr_metadata


# Print all found datasets to individual JSON objects.
def print_datasets():
    global id_2_object
    global path_ids

    # Will map a file_path to its ID.
    path_2_id = {}

    # Iterate over each file and make individual JSON objects.
    for file_id in id_2_object:
        # Edge Case: Update path based which software or dataset.
        if "tool_" in file_id:
            file_name = file_id[file_id.index("_") + 1:] 
            file_path = "sources/software/{}__caida.json".format(file_name)
        else:
            file_path = "sources/dataset/{}__caida.json".format(file_id)

        path_2_id[file_path] = file_id

        # Write the JSON object to the file.
        curr_file = json.dumps(id_2_object[file_id], indent=4)
        with open(file_path, "w") as output_file:
            output_file.write(curr_file)
        
    # Print a JSON mapping all made files to their IDs.
    with open(path_ids, "w") as output_file:
        output_file.write(json.dumps(path_2_id, indent=4))

# Run the script given the inputs from the terminal.
main(sys.argv[1:])
