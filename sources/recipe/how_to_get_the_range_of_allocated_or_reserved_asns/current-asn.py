#!  /usr/bin/env python3
__author__ = "Nicole Lee"
__email__ = "nlee@zeus.caida.org"
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
import pandas as pd
import argparse
import os

################################# Main Method ##################################
def main():
    parser = argparse.ArgumentParser(description='Returns full and compressed dictionaries of ranges.')
    parser.add_argument('csv1', help='iana 16-bit csv asn file')
    parser.add_argument('csv2', help='iana 32-bit csv asn file')
    args = parser.parse_args()
    print(iana_asn_asignees(args.csv1, args.csv2), iana_asn_compressed(args.csv1, args.csv2))

############################### Helper Methods #################################
def aggregate_ranges(ls):
    """
    Aggregates consecutive lists of ranges into a single range.
    """
    final = []
    i = 0
    if len(ls) == 1:
        return ls
    curr_range = ls[0]
    while i != len(ls)-1:
        i+=1
        current = ls[i]
        if ((curr_range[0] <= current[1]) and (curr_range[0] >= current[0])) or ((curr_range[0] <= current[0]) and (curr_range[1] >= current[0])):
            curr_range = [min([curr_range[0], current[0]]), max([current[1], curr_range[1]])]
            if i == len(ls)-1:
                final.append(curr_range)
                return final
            continue
            current = ls[i]
        if (curr_range[1] + 1 == current[0]) or (curr_range[1] == current[0]):
            curr_range[1] = current[1]
            if i == len(ls)-1:
                final.append(curr_range)
                return final
        else:
            final.append(curr_range)
            if i == len(ls)-1:
                final.append(current)
                return final
            else:
                curr_range = current
    return final

def simplify(x):
    """
    Returns either "reserved", "unassigned", or "allocated"
    """
    if 'reserved' in x:
        return 'reserved'
    if 'unassigned' in x:
        return 'unassigned'
    else:
        return 'allocated'

def clean_designation_names(x):
    """
    Returns either "reserved", "unassigned", or "allocated"
    """
    if 'reserved' in x:
        return 'reserved'
    if 'unassigned' in x:
        return 'unassigned'
    else:
        return x.replace('assigned by', '').strip()


def combine(csv_path16, csv_path32):
    """
    Combines 16-bit and 32-bit csv files.
    """   
    current_16 = pd.read_csv(csv_path16)
    current_32 = pd.read_csv(csv_path32)
    current_32 = current_32.loc[current_32["Number"] != '0-65535']
    return pd.concat([current_16, current_32])

def iana_asn_asignees(csv_path16, csv_path32):
    """
    Takes in two IANA files (one for 32-bit and one for 16-bit asn) and returns a dictionary with ranges by assignee.
    """
    current = combine(csv_path16, csv_path32)
    current["Description"] = current["Description"].apply(lambda x: clean_designation_names(x.lower()))
    current["Number"] = current["Number"].apply(lambda x: [int(x), int(x)] if '-' not in x else [int(x.split('-')[0]), int(x.split('-')[1])])

    asn = (current
    .drop(current.columns.difference(['Number','Description']), axis=1)
    .groupby("Description")["Number"]
    .apply(list)
    .apply(aggregate_ranges)).to_dict()

    try:
        del asn['unallocated']
    except KeyError:
        pass

    return asn

def iana_asn_compressed(csv_path16, csv_path32): 
    """
    Takes in two IANA files (one for 32-bit and one for 16-bit asn) and returns a dictionary with allocated or reserved ranges.
    """
    current = combine(csv_path16, csv_path32)
    current["Description"] = current["Description"].apply(lambda x: simplify(x.lower()))
    current["Number"] = current["Number"].apply(lambda x: [int(x), int(x)] if '-' not in x else [int(x.split('-')[0]), int(x.split('-')[1])])

    asn = (current
    .drop(current.columns.difference(['Number','Description']), axis=1)
    .groupby("Description")["Number"]
    .apply(list)
    .apply(aggregate_ranges)).to_dict()

    try:
        del asn['unallocated']
    except KeyError:
        pass

    return asn


if __name__ == "__main__":
    try:
        main()
    except FileNotFoundError:
        print("File does not exist")


