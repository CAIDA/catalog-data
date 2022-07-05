#!  /usr/bin/env python3
__author__ = "Bradley Huffaker"
__email__ = "<bradley@caida.org>"
# This software is Copyright (C) 2022 The Regents of the University of
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
# supplied â€œas isâ€, without any accompanying services from The Regents. The
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
# SOFTWARE PROVIDED HEREUNDER IS ON AN â€œAS ISâ€ BASIS, AND THE UNIVERSITY OF
# CALIFORNIA HAS NO OBLIGATIONS TO PROVIDE MAINTENANCE, SUPPORT, UPDATES,
# ENHANCEMENTS, OR MODIFICATIONS.
#
import re
import argparse
import sys
import json
import requests
import time

URL = "https://api.asrank.caida.org/v2/graphql"

#method to print how to run script
def print_help():
    print (sys.argv[0],"-u as-rank.caida.org/api/v1")
    
######################################################################
## Parameters
######################################################################
parser = argparse.ArgumentParser()
parser.add_argument("-v", dest="verbose", help="prints out lots of messages", action="store_true")
parser.add_argument("-d", dest="debug_limit", help="print only the first debug_limit", type=int)
parser.add_argument("-f", dest="asns_file", help="loads asn from file", type=str)
parser.add_argument("asns",nargs="*", type=str,help="ASNs we are looking up")
args = parser.parse_args()

######################################################################
## Main code
######################################################################
def main():
    #if args.asn is None:
    #    parser.print_help()
    #    sys.exit()
    hasNextPage = True

    first = 500
    offset = 0
    start = time.time()
    asns = set()
    for asn in args.asns:
        asns.add(asn)
    if args.asns_file:
        with open(args.asns_file) as fin:
            for asn in fin:
                asns.add(asn.rstrip())
    if len(asns) < 1:
        parser.print_help()
        print ("You must provide at least one ASN:")
        print ("    ",sys.argv[0], "-f asn_file")
        print ("    ",sys.argv[0], "195")
        sys.exit()

    while hasNextPage:
        query = AsnLinksQuery(first, offset, asns)
        request = requests.post(URL,json={'query':query})
        if request.status_code != 200:
            print ("Query failed to run returned code of %d " % (request.status_code))

        data = request.json()
        if not ("data" in data and "asnLinks" in data["data"]):
            print ("Failed to parse:",data,file=sys.stderr)
            sys.exit()

        data = data["data"]["asnLinks"]
        for node in data["edges"]:
            print (json.dumps(node["node"]))

        hasNextPage = data["pageInfo"]["hasNextPage"]
        offset += len(data["edges"])

        if args.verbose:
            print ("    ",offset,"of",data["totalCount"], " ",time.time()-start,"(sec)",file=sys.stderr)
            start = time.time()

        if args.debug_limit and args.debug_limit < offset:
            hasNextPage = False

######################################################################
## Queries
######################################################################

def AsnLinksQuery(first,second, asns): 
    asns_string = '"'+"\",\"".join(asns)+'"'
    return """{
    asnLinks(first:%s, offset:%s, asns:[%s]) {
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
                   organization {
                    orgName
                  }
                }
                asn1 {
                    asn
                  organization {
                    orgName
                  }
                }
                numberPaths
            }
        }
    }
}""" % (str(first), str(second), asns_string)
#run the main method
main()
