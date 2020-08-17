#!  /usr/bin/env python3
__author__ = "Pooja Pathak"
__email__ = "pmpathak@ucsd.edu"
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
import json
import re
import pyasn
import sys
import gzip

############################## Global Variables ################################

re_multi_origin = re.compile(r"\w+[_]\d+$")

ips  = []
asns = []
asn_db = None

# Files/Filesets
dat_file = None
prefix_2_as6_file = None

################################# Main Method ##################################

def main():
    global re_multi_origin
    global asn_db 
    global ips
    global dat_file
    global prefix_2_as6_file

    parser = argparse.ArgumentParser()
    parser.add_argument("-t", type= str, default=None, dest= "sc_to_json_file", help="Path to a .json file.")
    parser.add_argument("-p", type=str, default=None, dest="prefix_2_as6_file", help="Path to a .prefix2as6 file.")
    parser.add_argument("-d", type=str, default=None, dest="dat_file", help="Name for .dat file used for ipv6 prefix to AS mapping.")
    args = parser.parse_args()

     # Exit if missing the sc_to_json_file.
    if args.sc_to_json_file is None:
        print("sc_to_json_file not found")
        print(sys.argv[0],"-t sc_to_json")
        sys.exit()

    # Exit if missing the prefix_2_as6_file.
    if args.prefix_2_as6_file is None:
        print("prefix_2_as6_file not found")
        print(sys.argv[0],"-p prefix_2_as6_file")
        sys.exit()
    

    # Edge Case: Create a default name for dat_file if none is given.
    if args.dat_file is None or not re.search(r".dat$", args.dat_file):
        dat_file = "ipv6_prefix_2_as.dat"
    else:
        dat_file = args.dat_file
    
    sc_to_json_file = args.sc_to_json_file
    prefix_2_as6_file = args.prefix_2_as6_file

    # Create list of ipv6 addresses
    create_ips(sc_to_json_file)

    # Create a .dat file and pyasn object from the prefix_2_as6_file
    create_asn_db()

    # Create list of asns
    create_asns()

############################### Helper Methods #################################

def create_ips(sc_to_json_file):
    '''
    Parse JSON object and create list of ip addresses. 
    '''
    global ips

    data = []
    for line in open(sc_to_json_file, 'r'):
        data.append(json.loads(line)) 

    for elem in data:
        ips.append(elem['src'])
        hops = elem["hops"]
        for hop in hops:
            ips.append(hop["addr"])
        ips.append(elem['dst'])
    # print(ips)

def create_asn_db_body(curr_line):
    '''
    Parse the given line and either return formatted line or None.
    '''
    if not re_multi_origin.search(curr_line):
        # curr_line Format:     <prefix>\t<length>\t<as> 
        # curr_data Format:     [ <prefix>, <length>, <as> ]
        # return Format:        <prefix>/<length>\t<as>\n
        curr_data = curr_line.split()
        return curr_data[0] + "/" + curr_data[1] + "\t" + curr_data[2] + "\n"
    # Edge Case: Return None if curr_line is neither BGP or necessary data.
    else:
        return None


def create_asn_db():
    '''
    Update asn_db with a pyasn object created from prefix_2_as6_file. 
    '''
    global asn_db

    # Create the dat_file to write parsed data from the prefix_2_as6_file.
    with open(dat_file, "w") as out_file:
        lines = []
            # Open prefix_2_as6_file as an encoded .gz file.
        if re.search(r".gz$", prefix_2_as6_file, re.IGNORECASE):
            with gzip.open(prefix_2_as6_file, "rb") as in_file:
            # Iterate over lines in in_file and append each decoded line
                for line in in_file:
                    lines.append(line.decode())
        else:
            # Else open prefix2as6 file as unzipped .prefix2as6 file
            with open(prefix_2_as6_file, 'r') as in_file:
                # Iterate over lines in in_file and append line
                for line in in_file:
                    lines.append(line)
        
        for line in lines:
            parsed_line = create_asn_db_body(line)
            # Only write to out_file if parsed_line was necessary data.
            if parsed_line is not None:
                out_file.write(parsed_line)

    # Create the asn_db with the dat_file that was just created.
    try:
        asn_db = pyasn.pyasn(dat_file)
    except ValueError as error:
        print("dat_file was not able to be made with given .prefix2as6 file")
        print(str(error))
        
        
def create_asns():
    '''
     Create list of asns from pyasn lookup
    '''
    global ips
    global asn_db 

    asns = []
    for ip in ips:
        try:
            asn, prefix = asn_db.lookup(ip)
        except ValueError:
            print("No corresponding asn for ", ip)
        asns.append(asn)
    print(asns)

main()





