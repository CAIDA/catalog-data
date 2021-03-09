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
re_json = re.compile(r".json")
re_mkdn = re.compile(r".md")
re_mdta = re.compile(r"~~~metadata")
re_dlim = re.compile(r"~~~")

# File Paths:
path = None
path_ids = "data/data_id___caida.json"

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

    # store existing ids
    add_seen_ids("sources");

    # Parse all .md file in the given path.
    parse_catalog_data_caida()

    # Print all found JSON objects to individual JSON files.
    print_datasets()

############################### Helper Methods #################################

# Add each paper's ID to seen_papers from the source/paper directory.
def add_seen_ids(source_dir):
    global seen_ids

    re_placeholder = re.compile(r"___")
    for fname in sorted(os.listdir(source_dir)):
        path = source_dir+"/"+fname
        if os.path.isdir(path):
            type_ = fname
            for filename in sorted(os.listdir(path)):
                if re.search("\.json$",filename,re.IGNORECASE):
                    try:
                        info = json.load(open(path+"/"+filename))
                        info["filename"] = path+"/"+filename
                        id = info["id"] = utils.id_create(info["filename"], type_, info["id"])
                        if id in seen_id:
                            print ("duplicate id found in\n   ",filename,"\n   ", seen_id[id])
                        else:
                            seen_id[id] = filename
                    except Exception as e:
                        print ("\nerror",path+"/"+filename)
                        print ("    ",e)
                        sys.exit()


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

    # number skipped with no description
    number_skipped_no_description = 0

    # Iterate over each file in catalog-data-caida/sources.
    for file in os.listdir(path):
        # Edge Case: Skip if file is not a .md file.
        if not re_mkdn.search(file):
            continue

        file_name = file[:file.index(".")].replace("-", "_")
        file_path = "{}{}".format(path, file)

        metadata = parse_metadata(file_path)
        # not including private datasets
        if "visibility" not in metadata or metadata["visibility"] != "private":
            if metadata["id"] in seen_id:
                print ("duplicate id",metadata["id"])
                print ("    ",metadata["id"])
                print ("    ",seen_id["id"])
                continue

            # If it has no description skip it
            if "description" not in metadata or re.search("^\s*$", metadata["description"]):
                number_skipped_no_description += 1
                continue

            # Edge Case: Replace missing names with ID.
            if "name" not in metadata:
                name = metadata["id"].replace("_", " ").upper()
                metadata["name"] = name

            # Edge Case: Remove tool_ from softwares.
            if "tool_" in metadata["id"]:
                new_name = metadata["id"][5::]
                metadata["id"] = new_name

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

            # Store the metadata
            id_ = metadata["id"]
            if id_ in id_2_object:
                print ("duplicate",id_)
                print ("    ",id_2_object["filename"])
                print ("    ",metadata["filename"])
            else:
                id_2_object[metadata["id"]] = metadata

    print ("   number skipped no desc:", number_skipped_no_description)

re_section = re.compile("^~~~([^\n]+)")
def parse_metadata(filename):
    section = None
    buffer = {}
    content = False
    metadata = None
    with open(filename) as f:
        for line in f:
            # everything after '=== content ===' is placed inside content unprocessed
            if content:
                metadata["content"] += line

            if section is not None:
                if "~~~" == line.rstrip():
                    if "metadata" == section:
                        try:
                            metadata = json.loads(buffer)
                            metadata["filename"] = filename
                        except json.decoder.JSONDecodeError as e:
                            print ("json parse error in metadata",filename, e,file=sys.stderr)
                            return None
                    elif metadata is None:
                        print("found section '"+section+"' before '~~~metadata' in",filename, file=sys.stderr)
                        return None
                    else:
                        parts = section.split("~")
                        current = metadata
                        for part in parts[:-1]:
                            if part not in current:
                                current[part] = {}
                            current = current[part]

                        current[parts[-1]] = buffer
                    section = None
                    buffer = None
                else:
                    buffer += line
            elif "=== content ===" == line.rstrip():
                if metadata is None:
                    print("found '=== content ===' before ~~~metadata in",filename, file=sys.stderr)
                    return None
                content = True
                metadata["content"] = ""

            else:
                m = re_section.search(line)
                if m:
                    section = m.group(1)
                    buffer = ""

    return metadata


# Print all found datasets to individual JSON objects.
def print_datasets():
    global id_2_object
    global path_ids

    # Iterate over each file and make individual JSON objects.
    for id_,obj in id_2_object.items():
        # Edge Case: Update path based which software or dataset.
        if "tool_" in id_:
            type_ = "software"
            #id_ = obj["id"] = id_[id_.index("_") + 1:] 
        else:
            type_ = "dataset"
        filename = "sources/%s/%s___caida.json" % (type_, id_)
        obj["filename"] = filename

        # Write the JSON object to the file.
        curr_file = json.dumps(id_2_object[id_], indent=4)
        with open(filename, "w") as output_file:
            output_file.write(curr_file)
    
    # Print a JSON mapping all made files to their IDs.
    with open(path_ids, "w") as output_file:
        ids = sorted(id_2_object.keys())
        output_file.write("[\n")
        for id_ in ids:
            obj = id_2_object[id_]
            strings = []

            for key in ["id","name","filename", "organization", "description", "status", "dateCreated", "dateLastUpdated"]:
                if key in obj:
                    strings.append('    "'+key+'":'+json.dumps(obj[key]))

            for key in ["tags","licenses"]:
                if key in obj:
                    strings.append('    "'+key+'":'+json.dumps(sorted(obj[key])))
                    
            if "resources" in obj:
                r = []
                for res in obj["resources"]:
                    for key in ["name","url"]:
                        if key in res:
                            r.append('"'+key+'":'+json.dumps(res[key]))
                    for k in ["tags"]:
                        if k in res:
                            r.append('"'+k+'":'+json.dumps(sorted(res[k])))
                strings.append('    "resources": [\n'
                        +'       {\n         '
                        +',\n         '.join(r)
                        +'\n       }\n'
                        +'   ]')
            #sys.stdout.write(",\n".join(strings)+"\n")
            #sys.stdout.write("\n")

            output_file.write("  {\n")
            output_file.write(",\n".join(strings)+"\n")
            if id_ == ids[-1]:
                output_file.write("  }\n")
            else:
                output_file.write("  },\n")
        output_file.write("]\n")

# Run the script given the inputs from the terminal.
main(sys.argv[1:])
