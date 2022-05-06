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
# supplied "as is", without any accompanying services from The Regents. The
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
# SOFTWARE PROVIDED HEREUNDER IS ON AN "AS IS" BASIS, AND THE UNIVERSITY OF
# CALIFORNIA HAS NO OBLIGATIONS TO PROVIDE MAINTENANCE, SUPPORT, UPDATES,
# ENHANCEMENTS, OR MODIFICATIONS.
#
import argparse
import sys
import os.path
import requests
import time

#URL = "https://api.catalog.caida.org/v2/graphql"

#method to print how to run script
def print_help():
    print (sys.argv[0],"-u as-rank.caida.org/api/v1")
    
######################################################################
## Parameters
######################################################################
parser = argparse.ArgumentParser()
parser.add_argument("-f", dest="force", help="forcing download", action='store_true')
parser.add_argument("-O", dest="output", help="saves to output", type=str)
parser.add_argument("url",nargs=1, type=str,help="url")
args = parser.parse_args()

# get the 
if not args.force and os.path.exists(args.output):
    ti_m = time.time() - os.path.getmtime(args.output)
    if ti_m < 23*60*60:
        print ("   ",args.output,"is fresh (less then 23 hours) not downloading")
        sys.exit()
print ("   downloadings",args.output)

# Open the output file
try:
    fout = open(args.output,"w")
except Exception as e: 
    print(e,file=sys.stderr)
    sys.exit()

######################################################################
## Query
######################################################################
query = """
# Write your query or mutation here
{
  search (query:"") {
    totalCount
    edges {
      node {
        id
      }
    }
  }
}"""
request = requests.post(args.url[0],json={'query':query})
if request.status_code != 200:
    print ("Query failed to run returned code of %d " % (request.status_code))
    sys.exit()

data = request.json()
current = data
for key in ["data","search","edges"]: 
    if key in current:
        current = current[key]
    else:
        print ("Failed to parse:",data,file=sys.stderr)
        sys.exit()
for edge in current:
    fout.write(edge["node"]["id"]+"\n")
