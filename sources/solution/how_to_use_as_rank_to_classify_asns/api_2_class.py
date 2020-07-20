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
import time
from graphqlclient import GraphQLClient

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

# API Link:
api_url = "https://api.asrank.caida.org/v2/graphql"
PAGE_SIZE = 100000
decoder = json.JSONDecoder()
encoder = json.JSONEncoder()

################################# Main Method ##################################

def main(argv):
    global as_2_class
    global as_2_data
    global api_url
    global PAGE_SIZE
    global decoder
    global encoder

    hasNextPage = True
    first = PAGE_SIZE
    offset = 0

    page = 0

    # Used by nested calls
    start = time.time()
    print("Downloading asn relationships with as_links_query", file=sys.stderr)
    while hasNextPage:
        type,query = as_links_query(first, offset)

        data = download_query(api_url, query)
        if not ("data" in data and type in data["data"]):
            print("Failed to parse:",data,file=sys.stderr)
            sys.exit()
        
        data = data["data"][type]
        for node in data["edges"]:
            update_as_2_data(node["node"])

        print("Page: ", page, file=sys.stderr)
        page += 1

        hasNextPage = data["pageInfo"]["hasNextPage"]
        offset += data["pageInfo"]["first"]
    print("Done", file=sys.stderr)

    update_classifications()
    print_classifications()

############################### Helper Methods #################################

# Helper method that calls the query.
def download_query(url, query):
    client = GraphQLClient(url)
    return decoder.decode(client.execute(query))


# Helper method of the formatted query.
def as_links_query(first, offset):
    return [
        "asnLinks",
        """{
        asnLinks(first:%s, offset:%s) {
            totalCount
            pageInfo {
                first
                hasNextPage
            }
            edges {
                node {
                    relationship
                    asn0 {
                        asn
                    }
                    asn1 {
                        asn
                    }
                    numberPaths
                }
            } 
        }
    }"""  % (first, offset)
    ]


# Helper method that takes in a dict to create a pair relationship.
def update_as_2_data(curr_line):
    global as_2_data

    # Get the values from the current line.
    relationship = curr_line["relationship"]
    asn0 = curr_line["asn0"]["asn"]
    asn1 = curr_line["asn1"]["asn"]

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
    if relationship == "provider":
        as_2_data[asn0]["providers"].add(asn1)
        as_2_data[asn1]["customers"].add(asn0)
    # Else if asn0's customer is asn1.
    elif relationship == "customer":
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


# Helper method that prints all as_2_class to STDOUT
def print_classifications():
    global as_2_class

    for asn in as_2_class:
        sys.stdout.write(json.dumps(as_2_class[asn]) + "\n")

# Run the script given the inputs from the terminal.
main(sys.argv[1:])