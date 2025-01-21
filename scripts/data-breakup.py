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

parser = argparse.ArgumentParser()
parser.add_argument("json", nargs="+", type=str, help="single json object file")
args = parser.parse_args()

re_front = re.compile(r"^_")
re_end = re.compile(r"_$")
re_id_illegal = re.compile(r"[^\d^a-z^A-Z]+")
re_type_id = re.compile(r"[^\:]+:(.+)")

def main():

    for fname in args.json:
        type_ = fname.split(".")[0].lower()
        if not os.path.exists(type_):
            os.mkdir(type_)
        data = json.load(open(fname))
        for obj in data:
            if "id" in obj:
                id_ = re_type_id.search(obj["id"]).group(1)
            else:
                id_ = obj["name"]
            id_ = re_end.sub("",re_front.sub("",re_id_illegal.sub("_",id_.lower())))

            obj["id"] = id_
            obj_fname = type_+"/"+id_+".json"
            print (obj_fname)
            if "__typename" in obj:
                del obj["__typename"]
            json.dump(obj,open(obj_fname,"w"),indent=4)
        # json.dump(word_score_id, open(word_score_id_file,"w"),indent=4)

main()


