#!  /usr/bin/env python3
# This software is Copyright (C) 2023 The Regents of the University of
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
__author__ = "Bradley Huffaker"
__email__ = "<bradley@caida.org>"
import json
import sys
import os
import re
import argparse
import lib.utils as utils


######################################################################
## Parameters
######################################################################
import argparse
parser = argparse.ArgumentParser(description='Parses the ontology objects.')
parser.add_argument("-R", dest="readable_output", help="indents the output to make it readaable", action='store_true', default=True)
parser.add_argument("directory", nargs=1, type=str, help="ontology directory")
args = parser.parse_args()

id_object_file = "ontology_id_object.json"
id_object = {} 

re_caida = re.compile("caida:")
re_json = re.compile(".json$")

context = {}

def main():
    directory = args.directory[0]
    for fname in sorted(os.listdir(directory)):
        if re_json.search(fname): 
            path = f"{directory}/{fname}"
            file_load(path)

    for obj in id_object.values():
        if "@graph" in obj: 
            for prop in obj["@graph"][:-1]:
                if prop["@type"] == "rdf:Property":
                    property_add_classes(obj["filename"], prop)

    ontology_id_object = ontology_id_object_build()

    #######################
    # printing errors
    #######################
    utils.error_print()

    #######################
    # print files
    #######################

    if args.readable_output:
        indent = 4
    else:
        indent = None

    print ("writing",id_object_file)
    json.dump(ontology_id_object, open(id_object_file,"w"),indent=indent)

def ontology_id_object_build():
    i_o = {} 
    for i, obj in id_object.items(): 
        if "@graph" in obj:
            node = obj["@graph"][-1]
        else:
            node = obj
        context = {} 
        for key,url in obj["@context"].items():
            context[key] = url

        i_o[i] = object_build(obj["filename"], context, node, obj, obj["@graph"])
    return i_o

def object_build(filename, context, node, encoded=None, graph=None):
    key,id_ = node["@id"].split(":")
    url = context[key]+id_

    o = {
        "id":node["@id"],
        "__typename":node["@type"].split(":")[1],
        "url":url
    }

    if "@label" in node:
        o["name"] = node["@label"]
    else:
        o["name"] = node["@id"].split(":")[1]

    if "rdfs:comment" in node:
        o["description"] = node["rdfs:comment"]


    if o["__typename"] == "Property":
        for key in ["schema:domainIncludes", "schema:rangeIncludes"]:
            if key not in o:
                continue 

            to = key.split(":")[1]
            classes = node[key]
            if type(classes) == dict: 
                classes = [classes]

            class_urls = []
            for c in classes:
                key,name = c["@id"].split(":")
                if key in context:
                    class_urls.append({
                        "id":c["@id"],
                        "name":name,
                        "url":context[key]+name
                    })
                else:
                    utils.error_add(filename, f"Failed to context {key}")
            o[to] = class_urls
    elif graph is not None:
        props = []
        for prop in graph[:-1]:
           props.append(object_build(filename, context, prop))
        o["properties"] = props

    if encoded is not None:
        o["json"] = encoded

    return o



def file_load (fname):
    print ("loading",fname)
    with open(fname) as fin: 
        try:
            info = json.load(fin)
        except Exception as e:
            print (f"\nERROR: {fname}")
            print ("    ",e)
            sys.exit(1)

        info["filename"] = fname

        if "@graph" in info:
            node = info["@graph"][-1]
        else:
            node = info["@id"]

        node["schema:isPartOf"] =  {
            "@id": info["@context"]["caida"]
        }
        id_object[node["@id"]] = info

def property_add_classes(filename, prop): 
    id_ = prop["@id"]
    c = id_.split(":")[0]
    if c == "caida":
        if id_ not in id_object:
            utils.error_add(filename, f"Failed to find '{id_}'")
            return False

        obj = id_object[id_]
        for key in ["schema:domainIncludes", "schema:rangeIncludes"]:
            if key in prop:
                if key not in obj:
                    obj[key] = prop[key]
                else:
                    if type(obj) == dict:
                        obj[key] = [obj[key]]
                    obj[key].append(prop[key])

main()