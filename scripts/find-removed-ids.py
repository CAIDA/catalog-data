#!/usr/bin/env python3
__author__ = "Bradley Huffaker", "Victor Ren"
__email__ = "<bradley@caida.org>", "<vren@ucsd.edu>"
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

# PREREQUISITES:
# Generate list of removed ids in the catalog in the format of type:name (no spacing)

# USAGE:
# ./find-removed-ids.py <deleted ids> > <output file>
# We recommend outputting to a file for efficiency
# This script reads all ids that has been deleted from the catalog. It takes the input file of
# deleted ids and outputs all ids that has been removed but not in current CAIDA catalog api.

# imports
import requests
import sys

# Read input file
with open(sys.argv[1]) as fin:
    deleted = set()
    for line in fin:
        # Strip spaces
        deleted.add(line.rstrip())

# Set to store each unique id
ids_current = set()
query = """{
  search {
    edges {
       node {
          id
       }
    }
  }
}"""

# Request from CAIDA catalog api
request = requests.post("https://api.catalog.caida.org/", json={'query': query})
if request.status_code == 200:
    response = request.json()

# Iterate over all nodes from response and
for nodeDict in response["data"]["search"]["edges"]:
    ids_current.add(nodeDict['node']['id'])

# Iterate over deleted and find those NOT in catalog API
for obj_id in deleted:
    if obj_id not in ids_current:
        print(obj_id)
