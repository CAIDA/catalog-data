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

def main():
    directory = args.directory[0]
    for fname in sorted(os.listdir(directory)):
        if re_json.search(fname): 
            path = f"{directory}/{fname}"
            file_load(os.path.splitext(fname)[0], path)

    for obj in id_object.values():
        node = obj["@graph"][-1]
        if node["@type"] == 'rdf:Property':
            classes = node["schema:domainIncludes"]
            if type(classes) != list: 
                classes = [ classes ]
            
            for c in classes: 
                if re_caida.search(c["@id"]): 
                    class_add_property(obj["filename"], c["@id"], node)

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


def file_load (id_,fname):
    print ("loading",fname)
    with open(fname) as fin: 
        try:
            info = json.load(fin)
            info["filename"] = fname
            id_object["caida:"+id_] = info
        except Exception as e:
            print (f"\nERROR: {fname}")
            print ("    ",e)
            sys.exit(1)

def class_add_property(filename, i, node): 
    if i not in id_object:
        utils.error_add(filename, f"Failed to find {i}")
        return False
    graph = id_object[i]["@graph"]
    graph.append(graph[-1])
    graph[-2] = node
    return True
    

main()
