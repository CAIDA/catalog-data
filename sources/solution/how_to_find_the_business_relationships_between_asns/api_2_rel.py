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
pair_2_rel = {}
"""
{
    "asn0 asn1" : -1/0/1
}
"""

# Definitions:
rel_2_key = {
    "provider" : 1,
    "peer" : 0,
    "customer" : -1
}

# API values:
api_url = "https://api.asrank.caida.org/v2/graphql"
PAGE_SIZE = 10000
decoder = json.JSONDecoder()
encoder = json.JSONEncoder()

################################# Main Method ##################################

def main(argv):
    global pair_2_rel
    global rel_2_key
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
            print ("Failed to parse:", data, file=sys.stderr)
            sys.exit()
        
        data = data["data"][type]
        for node in data["edges"]:
            update_pair_2_rel(node["node"])

        print ("    ",offset,"of",data["totalCount"], " ",time.time()-start,"(sec)",file=sys.stderr)
        start = time.time()

        hasNextPage = data["pageInfo"]["hasNextPage"]
        offset += data["pageInfo"]["first"]
    print("Done", file=sys.stderr)

    # Helpful way to debug asns/get asns from pair_2_rel.
    # Highly recommend making multiple print statements due to long runtime.
    # print(get_relationship(3356, 3))

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
def update_pair_2_rel(curr_line):
    global pair_2_rel
    global rel_2_key

    # Get the values from the current line.
    relationship = rel_2_key[curr_line["relationship"]]
    asn0 = int(curr_line["asn0"]["asn"])
    asn1 = int(curr_line["asn1"]["asn"])

    # Place both related AS's in par_2_rel based on value of ASes.
    if (asn0 > asn1):
        temp = asn0
        asn0 = asn1
        asn1 = temp
        relationship = -1 * relationship

    key = str(asn0) + " " + str(asn1)

    # Add the pair's relationship if doesn't already exist.
    if key not in pair_2_rel:
        pair_2_rel[key] = relationship


# Helper Method to return the relationship of two given asns. 
def get_relationship(asn0, asn1):
    global pair_2_rel

    # Format keys by value.
    if (asn0 > asn1):
        temp = asn0
        asn0 = asn1
        asn1 = temp

    key = str(asn0) + " " + str(asn1)

    if key in pair_2_rel:
        rel = pair_2_rel[key]
        # return rel
        return str(asn0) + "'s " + str(rel) + " is " + str(asn1)
    else:
        return None

# Run the script given the inputs from the terminal.
main(sys.argv[1:])