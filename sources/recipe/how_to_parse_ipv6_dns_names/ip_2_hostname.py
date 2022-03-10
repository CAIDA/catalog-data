#!  /usr/bin/env python3
__author__ = "Donald Wolfson"
__email__ = "dwolfson@zeus.caida.org"
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
import sys
import os
import gzip
import re

############################## Global Variables ################################

# Datasets:
ip_2_hostname = {}
ips = None

# Definitions:
re_gzp = re.compile(r".gz$")
re_txt = re.compile(r".txt$")

# File Paths:
dns_names_file = None

################################# Main Method ##################################

def main(argv):
    global ip_2_hostname
    global re_gzp
    global re_txt
    global dns_names_file

    parser = argparse.ArgumentParser()
    parser.add_argument("-d", type=str, default=None, dest="dns_names_file", help="Path to an IPv6 dns-names file.")
    parser.add_argument("-i", type=str, default=None, dest="ips", help="Comma seperated list of IP Address to search for.")
    args = parser.parse_args() 

    # Create IPv4 ip_2_hostname dataset if .ppdc-ases file is given.
    if args.dns_names_file is not None:
        dns_names_file = args.dns_names_file
        parse_dns_names_file()

    # Edge Case: Print help and exit if prior conditions weren't met.
    else:
        print_help()

    # Print hostnames of ips if given.
    if args.ips is not None:
        ips = args.ips.split(",")
        # Iterate over each IP given and print their hostname to STDOUT.
        for ip in ips:
            print_hostname(ip)

############################### Helper Methods #################################

def print_help():
    sys.stderr.write("python3 as-customer-cone.py -d dns-names.18.20200101.txt.gz")
    sys.exit()

# Open the given file and send each line to a helper method to be parsed.
def parse_dns_names_file():
    global dns_names_file 
    global re_gzp
    global re_txt

    # Parse dns_names_file as an encoded .gz file.
    if re_gzp.search(dns_names_file):
        with gzip.open(dns_names_file, "r") as file:
            curr_line = file.readline()
            while curr_line:
                curr_line = curr_line.decode()
                parse_dns_names_line(curr_line)
                curr_line = file.readline()
    
    # Parse dns_names_file as a .txt file.
    elif re_txt.search(dns_names_file):
        with open(dns_names_file, "r") as file:
            curr_line = file.readline()
            while curr_line:
                parse_dns_names_line(curr_line)
                curr_line = file.readline()
    
    # Exit if file is neither a .gzp or .txt file type.
    else:
        sys.stderr.write("dns_names_file must be a .txt or encoded .gz file.")
        print_help()


# Given a line of a DNS Names File, map this line's ip address to its hostname.
def parse_dns_names_line(curr_line):
    global ip_2_hostname

    # Edge Case: Skip any commented lines.
    if curr_line[0] == "#":
        return

    # Try to pull all the data out of the current line.
    try:
        timestamp, ip_address, router_name = curr_line.split()
        
        # Map the current ip address to its hostname.
        ip_2_hostname[ip_address] = router_name
    except:
        pass    # Do nothing. Likely caused by a line missing all three columns.


# Helper method to print a hostname for a given ip address.
def print_hostname(ip_address):
    global ip_2_hostname

    if ip_address in ip_2_hostname:
        hostname = ip_2_hostname[ip_address]
        print("IP Address: {}, Hostname: {}".format(ip_address, hostname))
    else:
        print("No hostname found for: {}".format(ip_address))

# Run the script given the inputs from the terminal.
main(sys.argv[1:])