#!  /usr/bin/env python3
# This software is Copyright (C) 2018 The Regents of the University of
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
import lib.utils as utils
import json
import sys

######################################################################
## Parameters
######################################################################
import argparse
parser = argparse.ArgumentParser(description='Checks suggestions json format')
parser.add_argument("-o", dest="output_file", help="output file", type=str, required=True)
parser.add_argument("suggestions_file", nargs=1, help="suggestions file")
args = parser.parse_args()

fname = args.suggestions_file[0]
try:
    suggestions = json.load(open(fname))
except Exception as e:
    utils.error_add(fname, "JSON "+e.__str__())
    utils.error_print()
    sys.exit(1)
    
clean = []
for suggestion in suggestions:
    missing = []
    for key in ["query","description"]:
        if key not in suggestion:
            missing.append(key)
    if len(missing) > 0: 
        utils.error_add(fname, "'"+"','".join(missing)+"' not in "+json.dumps(suggestion))
    else:
        clean.append(suggestion)
if len(clean) > 0: 
    with open(args.output_file,"w") as fout:
        fout.write(json.dumps(clean,indent=4))

#######################
# printing errors
#######################
utils.error_print()

