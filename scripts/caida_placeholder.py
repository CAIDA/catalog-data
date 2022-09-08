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
import lib.utils as utils

#################################### Header ####################################

"""
    This script will produce blank JSON objects (datasets, software, etc) based
    on the local directory, catalog-data-caida/sources which holds metadata of
    caida datasets and software in markdown files.
    
    The script will first check for all currently available softwares and 
    datasets prior to finding new ones in catalog-data-caida to avoid 
    duplicates. The metadata included will help produce unique JSON objects for
    each file based on what's given. The file also produces a JSON mapping each
    new file path to its ID with extension __caida.json.
"""


############################## Global Variables ################################

# Datasets:
id_2_object = {}
seen_id = {} # stores the id to filename of current ids
seen_datasets = set()
seen_softwares = set()
seen_urls = set()

# Definitions:
re_json = re.compile(r"\.json$", re.IGNORECASE)
re_mkdn = re.compile(r"\.md$", re.IGNORECASE)
re_json = re.compile(r"\.json$", re.IGNORECASE)
re_mdta = re.compile(r"~~~metadata")
re_dlim = re.compile(r"~~~")

################################# Main Method ##################################

def main(argv):
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", type=str, default=None, dest="path", help="Path to catalog-data-caida/sources")
    args = parser.parse_args()

    # Edge Case: Exit if no path given.
    if args.path == None:
        return
    else:
        source_dir = args.path

    # Edge Case: Exit if path given doesn't exist.
    if not os.path.exists(source_dir):
        return

    # store existing ids
    add_seen_ids("sources");

    # Parse all .md file in the given path.
    parse_catalog_data_caida(source_dir)

    utils.error_print()

    # Print all found JSON objects to individual JSON files.
    print_datasets()

############################### Helper Methods #################################

## add to utils as separate funciton
# Add each paper's ID to seen_papers from the source/paper directory.
def add_seen_ids(source_dir):
    global seen_ids

    re_placeholder = re.compile(r"___caida")
    for fname in sorted(os.listdir(source_dir)):
        path = source_dir+"/"+fname
        if os.path.isdir(path):
            type_ = fname
            for filename in sorted(os.listdir(path)):
                file_path = path+"/"+filename
                if re.search("\.json$",filename,re.IGNORECASE) and not re_placeholder.search(filename):
                    try:
                        info = json.load(open(file_path))
                        info["filename"] = file_path
                        id = info["id"] = utils.id_create(info["filename"], type_, info["id"])
                        ids = [id]
                        
                        if type_ == "person" and "names" in info:
                            for name in info["names"]:
                                ids.append(utils.id_create(info["filename"], type_, name["nameLast"]+"__"+name["nameFirst"]))
                        for id in ids:
                            if id in seen_id:
                                print ("1. duplicate id found in\n   ",filename,"\n   ", seen_id[id])
                            else:
                                seen_id[id] = file_path
                    except Exception as e:
                        print ("\nerror",path+"/"+filename)
                        print ("    ",e)
                        sys.exit()


# Parse of all .md objects in catalog-data-caida/sources.
def parse_catalog_data_caida(source_dir):
    global id_2_object
    global seen_datasets
    global seen_softwares
    global seen_urls
    global re_mkdn
    global re_mdta
    global re_dlim

    # number skipped with no description
    number_skipped_no_description = 0

    re_md = re.compile("\.md$", re.IGNORECASE)

    # Iterate over each file in catalog-data-caida/sources.
    for type_ in sorted(os.listdir(source_dir)):
        path = source_dir+type_+"/"
        if os.path.isdir(path):
            for file in sorted(os.listdir(path)):

                file_name = file[:file.index(".")].replace("-", "_")
                file_path = path+file

                # Edge Case: Skip if file is not a .md file.
                if re_mkdn.search(file):
                    metadata = utils.parse_markdown(file_path)
                    if metadata is None:
                        print ("\nerror: failed to parse",file_path)
                        sys.exit(1)
                elif re_json.search(file):
                    try:
                        with open(file_path) as f:
                            metadata = json.load(f)
                            metadata["filename"] = file_path
                    except Exception as e:
                        print ("\nerror:",file_path)
                        print ("    ",e)
                        sys.exit(1)
                else:
                    print ("   skipping",file)
                    continue

                # Edge Case: Replace missing names with ID.
                if "name" not in metadata:
                    name = metadata["id"].replace("_", " ").upper()
                    metadata["name"] = name

                id_ = metadata["id"] = utils.id_create(file_path, type_, metadata["id"])
                # not including private datasets
                if id_ in seen_id:
                    print ("duplicate id",id_)
                    print ("    ",file_path)
                    print ("    ",seen_id[id_])
                    continue
                if id_ in id_2_object:
                    print ("duplicate",id_)
                    print ("    ",id_2_object[id_]["filename"])
                    print ("    ",metadata["filename"])
                    continue 
                else:
                    id_2_object[metadata["id"]] = metadata

                # If it has no description skip it
                if ("description" not in metadata or re.search("^\s*$", metadata["description"]))  \
                   and "deprecated" not in metadata:
                    utils.warning_add(file_path, "no description")
                    number_skipped_no_description += 1

                # Edge Case: Add CAIDA as organization if missing key.
                if "organization" not in metadata:
                    metadata["organization"] = "CAIDA"

                # Edge Case: Add CAIDA as a tag to all datasets.
                if "tags" not in metadata:
                    metadata["tags"] = []
                if "CAIDA" in metadata["organization"]:
                    if "caida" not in metadata["tags"]:
                        metadata["tags"].append("caida")

                # Edge Case: Remove 0 length lists from objects.
                keys = []
                for key,value in metadata.items():
                    if type(value) == str and re.search("^\s*$", value):
                        keys.append(key)
                for key in keys:
                    del metadata[key]
    utils.warning_add("", f"Skipped: {number_skipped_no_description} resources with no description")


# Print all found datasets to individual JSON objects.
def print_datasets():
    global id_2_object

    # Iterate over each file and make individual JSON objects.
    for type_id,obj in id_2_object.items():
        type_,id_ = type_id.split(":")

        type_dir = "sources/%s" % (type_)
        if not os.path.isdir(type_dir):
            os.mkdir(type_dir)
        # Edge Case: Update path based which software or dataset.
        filename = "%s/%s___caida.json" % (type_dir, id_)

        # Write the JSON object to the file.
        curr_file = json.dumps(id_2_object[type_id], indent=4)
        with open(filename, "w") as output_file:
            output_file.write(curr_file)
    
# Run the script given the inputs from the terminal.
main(sys.argv[1:])
