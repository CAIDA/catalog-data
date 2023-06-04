#!  /usr/bin/env python3
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
__author__ = "Bradley Huffaker"
__email__ = "<bradley@caida.org>"
import argparse
import json
import sys
import os
import re
import editdistance

#parser = argparse.ArgumentParser()
#parser.add_argument("json", nargs="+", type=str, help="single json object file")
#args = parser.parse_args()

id_object_file = "id_object.json"
id_id_link_file = "id_id_link.json"

with open(id_object_file,"r") as fin:
    id_object = json.load(fin)
    for i,obj in id_object.items():
        if "date" not in obj:
            obj["date"] = "202401"
        else:
            obj["date"] = "".join(obj["date"].split("-"))
with open(id_id_link_file,"r") as fin:
    id_id_link = json.load(fin)

print (f"exe:{sys.argv[0]}")
print ("""issue:[Put related objects in access](https://github.com/CAIDA/catalog-data/issues/565)
This is analysis of using edit distance on the names of the original paper and related
papers, media, and presentations.

The questions is how many false positives we generated .
Here is a list of papers that match.

**dist**: edit distance
**length**: length of the original paper
**ratio**: 100* distance / length
**name**: the first name is the paper, all following names are from related objects
""")

papers = []
k = 0
for obj in sorted( id_object.values(), key=lambda o: o["date"], reverse=True):
    i = obj["id"]
    if obj["__typename"] == "Paper":
        p_largest = None
        if i in id_id_link:
            l = len(obj["name"])
            close = []
            for j in id_id_link[i].keys():
                if i not in id_object:
                    continue 
                t = id_object[j]["__typename"]
                if t == "Paper" or t == "Media" or t == "Presentation":
                    d = editdistance.eval(obj["name"].lower(), id_object[j]["name"].lower())
                    p = int(100*d/l)
                    if p < 40:
                        close.append([j,d,p])
                        if p_largest is None or p_largest > p:
                            p_largest = p
            if len(close) > 0: 
                papers.append([p_largest, len(close),k, obj, close])
                k += 1

print ("<span sytel='font-size:-1'>")
print ("")
print ("| dist/length | ratio  | name  | date | type |")
print ("|----|---|----|-----|----|")
for p, l, k, obj, close in sorted(papers, reverse=True):
    print (p)
    print (f"| ----- | -- | **{obj['name']}** | {obj['date']} | {obj['__typename']}|")
    for j,d,p in close:
        o = id_object[j]
        print (f"| {d:2}/{l:2} | {p:2}% | {o['name']} | {o['date']} | {o['__typename']}|")
