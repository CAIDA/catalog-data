#!  /usr/bin/env python3
__author__ = "Bradley Huffaker"
__email__ = "bhuffaker@ucsd.edu"
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
import yaml
import csv 
import re
import json
import sys

parser = argparse.ArgumentParser()
parser.add_argument("-c", type=str, dest="csvfile", required=True)
parser.add_argument("yamlfile", nargs=1,type=str)
args = parser.parse_args()

id_tags = {}
with open(args.csvfile) as fin:
    spamreader = csv.reader(fin, delimiter=',', quotechar='"')
    for i,row in enumerate(spamreader):
        id = row[0][1:]
        tags = row[4]
        if not re.search("^\s*$", tags):
            tags = re.split("\s*,\s*", tags)
            for i,tag in enumerate(tags):
                tags[i] = re.sub("\.$","",tag.rstrip())
            id_tags[id] = tags

keys = ["MARKER","TYPE","AUTHOR","TITLE","SERIAL","YEAR","VOLUME","PAGE","DOI","URL","TOPKEY"
        ,"GEOLOC","ABS","TAGS"]

with open(args.yamlfile[0]) as fin:
    papers = list(yaml.load_all(fin,Loader=yaml.Loader))
    for paper in papers:
        id = "paper:"+paper["MARKER"]
        if id in id_tags:
            paper["TAGS"] = ", ".join(id_tags[id])
        print ("---")
        for key in keys:
            if key in paper:
                #print ('%-7s: "%s"' %(key,re.sub('"','\\"',paper[key])))
                value = paper[key].rstrip()
                value = re.sub("\n\.\.\.\n","",yaml.dump(value))
                value = re.sub("\n","",value)
                print ('%-7s: %s' %(key, value))
        print ("")
