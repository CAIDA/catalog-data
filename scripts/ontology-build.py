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
import copy
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

re_caida = re.compile(r"caida:")
re_json = re.compile(r".json$")
re_markdown = re.compile(r".md$")

types_valid = set(["rdf:Property","rdfs:Class","caida:Namespace"])

def main():
    directory = args.directory[0]
    context = {} 
    id_object = {}
    nodes = []
    # Create the main objects and unified context
    # and store other nodes for later processing
    for fname in sorted(os.listdir(directory)):
        path = f"{directory}/{fname}"
        if re_json.search(fname) or re_markdown.search(fname): 
            file_load(path, context, id_object, nodes)

    # Create Objects that are not the main object of the files
    for node in nodes:
        id_ = node["@id"]
        if id_ not in id_object and "caida:" == id_[:6]: 
            id_unknown_add(node["filename"], f"CAIDA context object without individual file {id_}")
            continue 

        obj = object_build(node)
        if obj is not None:
            if id_ not in id_object:
                print ("creating external",id_)
                id_object[id_] = obj
            else:
                object_merge(id_object[id_],obj)

    # set everything to the unified 
    for obj in id_object.values():
        # everything gets the same context
        obj["context"] = context

        # Namespaces are added to thier classes 
        if obj["__typename"] == "Namespace":
            for class_property in obj["properties"]:
                for key in ["class","property"]:
                    list_add(id_object[class_property[key]]["namespaces"], obj["id"])

    # Create LInks between classes and properties 
    link_classes = {} 
    for node in nodes:
        if node["@type"] == "rdf:Property":
            link_build(id_object, link_classes, node)

    # add the links to classes
    for link, classes in link_classes.items():
        id_object[link.class_id][link.type].append({
            "property":link.property_id,
            "classes":list(classes)
        })

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
    json.dump(id_object, open(id_object_file,"w"),indent=indent)

id_unknown = set() 
def id_unknown_add(filename, id_):
    if id_ not in id_unknown:
        id_unknown.add(id_)
        utils.error_add(filename, f"Unknown id {id_}")

def file_load (filename, context, id_object, nodes):
    print ("loading",filename)
    domain_range_keys = set(["schema:domainIncludes","schema:rangeIncludes"])

    if re_markdown.search(filename):
        context_graph = utils.parse_markdown(filename)
    else:
        with open(filename) as fin: 
            try:
                context_graph = json.load(fin)
            except Exception as e:
                print (f"\nERROR: {filename}")
                print ("    ",e)
                sys.exit(1)

    for key, value in context_graph["@context"].items():
        context[key] = value

    if "@graph" in context_graph:
        node = context_graph["@graph"][-1]
    else:
        node = context_graph

    node["filename"] = filename
    id_ = node["@id"]
    c,label = id_.split(":")
    if c in context:
        node["schema:isPartOf"] =  {
            "@id": context[c]
        }
    if id_ in id_object:
        utils.error_add(filename,f"Duplicate {id_} in {id_object[id_]['filename']}")
    else:
        obj = object_build(node)
        if obj is not None:
            id_object[id_] = obj

            if "@graph" in context_graph:
                for node in context_graph["@graph"][:-1]:
                    node["filename"] = filename
                    if node["@type"] in types_valid:
                        nodes.append(node)
                        for key in ["schema:rangeIncludes","schema:domainIncludes"]: 
                            if key in node: 
                                for n in convert_list(node[key]):
                                    nodes.append({
                                        "@id":n["@id"],
                                        "@type":"rdfs:Class",
                                        "filename":filename
                                    })
                        if "caida:properties" in node:
                            for class_property in node["caida:properties"]:
                                for key in ["caida:classUrl","caida:propertyUrl"]:
                                    nodes.append({
                                        "@id":class_property[key],
                                        "@type":"rdfs:Class",
                                        "filename":filename
                                    })
                    else:
                        utils.error_add(filename,f"Unknown @type {node['@type']}")


def object_build(node):
    id_ = node["@id"]
    key,name = id_.split(":")

    obj = {
        "filename":node["filename"],
        "keyValues":{}
    }
    t = node["@type"]
    if t == "rdf:Property":
        obj["__typename"] = "Property"
        obj["domainIncludes"] = []
        obj["rangeIncludes"] = []
        obj["namespaces"] = []
    elif t == "rdfs:Class":
        obj["__typename"] = "Class"
        obj["domainPropertyClasses"] = []
        obj["rangePropertyClasses"] = [] 
        obj["namespaces"] = []
    elif t == "caida:Namespace":
        obj["__typename"] = "Namespace"
        obj["properties"] = []
    else:
        utils.error_add(node["filename"],f"Unknown @type {t}")
        return None

    # Place in the now label and comment, skip domain/range/type
    # copy everything else into key_values
    for key,value in node.items():
        if key == "@id":
            obj["id"] = value
        elif key == "rdfs:label" or key == "schema:name":
            obj["name"] = value
        elif key == "rdfs:comment" or key == "schema:description":
            obj["description"] = value
        elif key == "schema:url":
            obj["url"] = value
        elif key == "caida:properties":
            for class_property in convert_list(node["caida:properties"]):
                obj["properties"].append({
                    "class":class_property["caida:classUrl"],
                    "property":class_property["caida:propertyUrl"]
                })
        elif key in ["schema:domainIncludes","schema:rangeIncludes"
            ,"@context", "@type","filename"]:
            pass 
        else:
            obj["keyValues"][key] = value
    if "name" not in node:
        obj["name"] = name

    return obj

def object_merge(obj_old, obj_new):
    for key,value in obj_new.items():
        if key not in obj_old:
            obj_old[key] = value
        elif key == "keyValues":
            k_v = obj_old[key]
            for k,v in value.items():
                if k not in k_v:
                    k_v[k] = v

class Link: 
    def __init__(self, class_id, property_id, type_):
        self.class_id = class_id
        self.property_id = property_id
        self.type = type_
    def __hash__(self):
        return hash((self.class_id, self.property_id, self.type))
    def _eq__(self, other):
        return self.class_id == other.class_id and self.property_id == other.property_id and self.type == other.type

unknown_ids = set()
def link_build(id_object, link_classes, node):
    prop_id = node["@id"]
    prop = id_object[prop_id]
    keys =  ["schema:rangeIncludes", "schema:domainIncludes"]
    types = ["rangePropertyClasses", "domainPropertyClasses"]
    for i in [0,1]:
        j = (i+1)%2
        i_key = keys[i]
        j_key = keys[j]
        type_ = types[i]
        prop_key = i_key.split(":")[1]
        if i_key not in node:
            continue 
        classes = convert_list(node[i_key])
        for c in classes: 
            class_id = c["@id"]

            if class_id in id_object:

                list_add(prop[prop_key], class_id)

                link = Link(class_id, prop_id, type_)
                if link not in link_classes:
                    link_classes[link] = set()

                if j_key in node:
                    for c in convert_list(node[j_key]):
                        i = c["@id"]
                        if i in id_object:
                            link_classes[link].add(i)
                        else:
                            print (node)
                            print ("missing id",i)
# Utils 
def convert_list(values):
    if type(values) != list:
        values = [values]
    return values

def list_add(values, value):
    if value not in values:
        values.append(value)


main()
