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
from collections import OrderedDict

parser = argparse.ArgumentParser()
parser.add_argument("files", nargs="+", type=str, help="single json object file")
args = parser.parse_args()

re_json = re.compile("json$")
re_markdown = re.compile("md$")
re_id_illegal = re.compile("[^\d^a-z^A-Z]+")
re_type_id = re.compile("[^\:]+:(.+)")
re_access = re.compile('^\s+"access":\s*\[')

re_start = re.compile('^\s*"resources":\s*\[')
re_end = re.compile('^\s*\],$')

def main():
    match = False
    for fname in args.files:
        #print (fname)
        with open (fname) as fin:
            obj = None
            state = "before"
            content = {
                "before":"",
                "after":""
            }
            access_created = False
            access_found = False
            buffer = ""
            depth = 0
            for line in fin:
                buffer += line
            obj = json.loads(buffer)
            if "access" in obj:
                print (fname,"skipping ------ access_found")
            else:
                obj = obj_update(obj)
                if obj and "access" in obj:
                    o = OrderedDict()
                    for key in ["id","name","type","image","description","date","dateStart","dateEnd","links","tags","access","resources","presenters","licenses","tabs"]:
                        if key in obj:
                            o[key] = obj[key]
                    for key,value in obj.items():
                        if key not in o:
                            o[key] = value
                    print(fname)
                    #fout = sys.stdout
                    #if fout:
                    with open (fname,"w") as fout:
                        encoded = json.dumps(o,indent=4)
                        print (encoded)
                        fout.write(encoded)
                else:
                    print (fname,"skipping ------")
                    print (buffer)


def tags_add(tags, value):
    if value not in tags:
        tags.append(value)

def obj_update(obj):
    if "resources" in obj:
        resources = []
        accesses = []
        for resource in obj["resources"]:
            if "tags" not in resource:
                resource["tags"] = []
            if resource["name"] == "public" or resource["name"] == "restricted" or resource["name"] == "commercial":
                resource["access"] = resource["name"]
                resource.pop('name', None)
                accesses.append(resource)
            elif resource["name"] == "PDF" or resource["name"] == "web page":
                resource["access"] = "public"
                tags_add(resource["tags"],resource["name"])
                resource.pop('name', None)
                accesses.append(resource)
            elif resource["name"].lower() == "video":
                resource["access"] = "public"
                tags_add(resource["tags"],"video")
                resource.pop('name', None)
                accesses.append(resource)
            elif resource["name"][:3] == "PNG" or resource["name"][:3] == "GIF":
                resource["access"] = "public"
                tags_add(resource["tags"],resource["name"][:3])
                if len(resource["name"]) == 3:
                    resource.pop('name', None)
                accesses.append(resource)
            elif resource["name"].lower() == "url":
                resource["access"] = "public"
                resource.pop('name', None)
                accesses.append(resource)
            elif "file" in resource["tags"]:
                resource["access"] = "public"
                accesses.append(resource)
            else:
                if len(resource["tags"]) < 1:
                    resource.pop("tags", None)
                resources.append(resource)
        if len(resources) > 0:
            obj["resources"] = resources
        else:
            obj.pop("resources",None)
        if len(accesses):
            obj["access"] = accesses
        return obj
    return None

main()
