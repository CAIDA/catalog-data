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

# Datasets
as_2_data = {}                  # Maps an asn to all of its ITDK data found.
"""
{
    "asn" : {
        "asn" : "...",
        "links" : set(),
        "interfaces" : set(),
        "continent" : "...",
        "country" : "...",
        "region" : "...",
        "city" : "...",
        "latitude" : "...",
        "longitude" : "..."
    }
}
"""
node_id_2_asn = {}            # Maps a node_id to its corresponding asn.
ases_2_print = None           # A list of asns to print to STDOUT.

# Definitions
re_txt = re.compile(r".txt$")
re_bz2 = re.compile(r".bz2$")

# File Paths
links_file = None
nodes_file = None
nodes_geo_file = None
nodes_as_file = None

################################# Main Method ##################################

def main(argv):
    global as_2_data
    global node_id_2_asn
    global ases_2_print
    global re_txt
    global re_bz2
    global links_file
    global nodes_file
    global nodes_geo_file
    global nodes_as_file

    parser = argparse.ArgumentParser()
    parser.add_argument("-a", type=str, dest="nodes_as_file", help="ITDK Nodes AS File.")
    parser.add_argument("-l", type=str, dest="links_file", help="ITDK Links File.")
    parser.add_argument("-n", type=str, dest="nodes_file", help="ITDK Nodes File.")
    parser.add_argument("-g", type=str, dest="nodes_geo_file", help="ITDK Nodes Geolocation File.")
    parser.add_argument("-p", type=str, dest="ases_2_print", help="Comma seperated list of asns to print.")
    args = parser.parse_args()

    # Edge Case: Exit and print help if any file is missing.
    if args.nodes_as_file is None:
        print_help()
    if args.links_file is None:
        print_help()
    if args.nodes_file is None:
        print_help()
    if args.nodes_geo_file is None:
        print_help()

    # Updating all file paths with given files.
    links_file = args.links_file
    nodes_file = args.nodes_file
    nodes_geo_file = args.nodes_geo_file
    nodes_as_file = args.nodes_as_file

    # Update node_id_2_asn with data from Nodes AS file.
    print("Parsing Nodes AS File...", file=sys.stderr)
    parse_nodes_as_file()
    
    # Update as_2_data with each asn's links.
    print("Parsing Links File...", file=sys.stderr)
    parse_links_file()
    
    # Update as_2_data with each asn's interfaces.
    print("Parsing Nodes File...", file=sys.stderr)
    parse_nodes_file()

    # Update as_2_data with each asn's geolocation.
    print("Parsing Nodes Geolocation File...", file=sys.stderr)
    parse_nodes_geo_file()

    print("Number of Nodes found: {}".format(len(as_2_data)), file=sys.stderr)

    # Print the provided ases to STDOUT.
    if args.ases_2_print is not None:
        ases_2_print = args.ases_2_print.split(",")
        for asn in ases_2_print:
            get_as_data(asn)

############################### Helper Methods #################################

def print_help():
    print(sys.argv[0], "-a nodes.as_file.bz2 -l links_file.bz2 -n nodes_file.bz2 -g nodes_geo_file.bz2", file=sys.stderr)
    sys.exit()


# Opens the nodes_as_file and sends each line to a helper method.
def parse_nodes_as_file():
    global re_txt
    global re_bz2
    global nodes_as_file

    # Open file as an encoded .bz2 file.
    if re_bz2.search(nodes_as_file):
        with bz2.open(nodes_as_file, "r") as file:
            curr_line = file.readline()
            while curr_line:
                curr_line = curr_line.decode()
                parse_nodes_as_body(curr_line)
                curr_line = file.readline()
    
    # Open file as a .txt file
    elif re_txt.search(nodes_as_file):
        with open(nodes_as_file, "r") as file:
            curr_line = file.readline()
            while curr_line:
                parse_nodes_as_body(curr_line)
                curr_line = file.readline()
    
    # Edge Case: Exit if a .txt or .bz2 file wasn't given
    else:
        print("All files must be either .bz2 or .txt file types.")
        print_help()


# Parses a given line of the nodes_as_file and updates as_2_data.
def parse_nodes_as_body(curr_line):
    global node_id_2_asn

    # Edge Case: Skip any commented lines.
    if curr_line[0] == "#":
        return

    # Format of curr_line: "node.AS   <node_id>   <AS>   <method>"
    ignore, node_id, asn, method = curr_line.split()

    # Map the node_id to its corresponding asn.
    node_id_2_asn[node_id] = asn


# Opens the links_file and sends each line to a helper method.
def parse_links_file():
    global re_txt
    global re_bz2
    global links_file

    # Open file as an encoded .bz2 file.
    if re_bz2.search(links_file):
        with bz2.open(links_file, "r") as file:
            curr_line = file.readline()
            while curr_line:
                curr_line = curr_line.decode()
                parse_links_body(curr_line)
                curr_line = file.readline()
    
    # Open file as a .txt file
    elif re_txt.search(links_file):
        with open(links_file, "r") as file:
            curr_line = file.readline()
            while curr_line:
                parse_links_body(curr_line)
                curr_line = file.readline()
    
    # Edge Case: Exit if a .txt or .bz2 file wasn't given
    else:
        print("All files must be either .bz2 or .txt file types.")
        print_help()


# Given a string of a line from a Links File, update as_2_data.
def parse_links_body(curr_line):
    global as_2_data
    global node_id_2_asn

    # Edge Case: Skip any commented lines.
    if curr_line[0] == "#":
        return

    # Format of curr_line: "link <link_id>: <N1>:i1 <N2>:i2 [ <N3>:[i3] ... ]"
    curr_line = curr_line.split()
    
    # Skip any lines that don't have any data.
    if len(curr_line) < 4:
        return

    # Format of curr_line: [ "link", link_id, [ N1, Interface ], N2, ... ]
    curr_line[2] = curr_line[2].split(":")
    node_id = curr_line[2][0]
    
    # Edge Case: Skip this line if the node_id doesn'st map to an asn.
    if node_id in node_id_2_asn:
        asn = node_id_2_asn[curr_line[2][0]]
    else:
        return
    
    # Create the current asn's object.
    as_2_data[asn] = {
        "asn" : asn,
        "links" : set(),
        "interfaces" : set(),
        "continent" : None,
        "country" : None,
        "region" : None,
        "city" : None,
        "latitude" : None,
        "longitude" : None
    }

    # Add the current interface if it exists.
    if len(curr_line[2]) == 2:
        interface = curr_line[2][1]
        as_2_data[asn]["interfaces"].add(interface)

    # Iterate over N2 to Nm and add all asns to the current link interface.
    for node in curr_line[3:]:
        # Split the node_id from the interface.
        node_data = node.split(":")
        node_id = node_data[0]
        
        # Add the link between the asn and node if the node has a mappable asn.
        if node_id in node_id_2_asn:
            curr_asn = node_id_2_asn[node_id]

            # Add the current asn to the parent asn's links set.
            as_2_data[asn]["links"].add(curr_asn)


# Opens the links_file and sends each line to a helper method.
def parse_nodes_file():
    global re_txt
    global re_bz2
    global nodes_file

    # Open file as an encoded .bz2 file.
    if re_bz2.search(nodes_file):
        with bz2.open(nodes_file, "r") as file:
            curr_line = file.readline()
            while curr_line:
                curr_line = curr_line.decode()
                parse_links_body(curr_line)
                curr_line = file.readline()
    
    # Open file as a .txt file
    elif re_txt.search(nodes_file):
        with open(nodes_file, "r") as file:
            curr_line = file.readline()
            while curr_line:
                parse_links_body(curr_line)
                curr_line = file.readline()
    
    # Edge Case: Exit if a .txt or .bz2 file wasn't given.
    else:
        print("All files must be either .bz2 or .txt file types.")
        print_help()


# Parses a given line of the nodes_file and updates as_2_data.
def parse_nodes_body(curr_line):
    global as_2_data
    global node_id_2_asn
    
    # Edge Case: Skip any commented lines. 
    if curr_line == "#":
        return

    # Format of curr_line: "node <node_id>: <i1> <i2> ... <in>"
    curr_line = curr_line.split()
    # Format of curr_line: [ "node", "<node_id>:", "<i1>", "<i2>", ..., "<in>" ]
    node_id = curr_line[2].replace(":","")

    # Skip line if node_id isn't mappable to an asn.
    if node_id not in node_id_2_asn:
        return

    asn = node_id_2_asn[node_id]

    # Skip line if asn not in as_2_data.
    if asn not in as_2_data:
        return

    # Iterate over interfaces on the current line, and add them to as_2_data.
    for interface in curr_line[2:]:
        as_2_data[asn]["interfaces"].add(interface)


# Opens the nodes_geo_file and sends each line to a helper method.
def parse_nodes_geo_file():
    global re_txt
    global re_bz2
    global nodes_geo_file

    # Open file as an encoded .bz2 file.
    if re_bz2.search(nodes_geo_file):
        with bz2.open(nodes_geo_file, "r") as file:
            curr_line = file.readline()
            while curr_line:
                curr_line = curr_line.decode()
                parse_nodes_geo_body(curr_line)
                curr_line = file.readline()
    
    # Open file as a .txt file
    elif re_txt.search(nodes_geo_file):
        with open(nodes_geo_file, "r") as file:
            curr_line = file.readline()
            while curr_line:
                parse_nodes_geo_body(curr_line)
                curr_line = file.readline()
    
    # Edge Case: Exit if a .txt or .bz2 file wasn't given
    else:
        print("All files must be either .bz2 or .txt file types.")
        print_help()


# Parses a given line of the nodes_geo_file and updates as_2_data.
def parse_nodes_geo_body(curr_line):
    global as_2_data
    global node_id_2_asn

    # Edge Case: Skip any commented lines. 
    if curr_line == "#":
        return
    
    curr_line = curr_line.split()
    node_id = curr_line[1].replace(":","")

    # Skip line if node_id isn't mappable to an asn.
    if node_id not in node_id_2_asn:
        return

    asn = node_id_2_asn[node_id]

    # Skip line if asn not in as_2_data.
    if asn not in as_2_data:
        return

    # Depending on length of curr_line update data with what is given.
    if len(curr_line) == 8:
        as_2_data[asn]["continent"] = curr_line[2]
        as_2_data[asn]["country"] = curr_line[3]
        as_2_data[asn]["region"] = curr_line[4]
        as_2_data[asn]["city"] = curr_line[5]
        as_2_data[asn]["latitude"] = curr_line[6]
        as_2_data[asn]["longitude"] = curr_line[7]
    elif len(curr_line) == 5:
        as_2_data[asn]["latitude"] = curr_line[2]
        as_2_data[asn]["longitude"] = curr_line[3]

# Print a given asn to STDOUT.
def get_as_data(asn):
    global as_2_data
    
    # Edge Case: Print error if asn not in as_2_data.
    if asn not in as_2_data:
        print("{} not in as_2_data".format(asn))
    else:
        print(as_2_data[asn])

# Run the script given the inputs from the terminal.
main(sys.argv[1:])