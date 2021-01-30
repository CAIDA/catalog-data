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
import json
import sys
import re
import os

############################## Global Variables ################################

# Datasets
seen_papers = set()     # Will hold all found paper IDs.
seen_authors = set()    # Will hold all found author IDs.
author_data = {}            # Will map all authors IDs to their JSON.

# Definitions
topkeys = {
    "MARKER",
    "TYPE",
    "AUTHOR",
    "GEOLOC",
    "TITLE",
    "YEAR",
    "TOPKEY",
    "SERIAL",
    "VOLUME",
    "CHAPTER",
    "ARTICLE",
    "PAGE",
    "CTITLE",
    "DOI",
    "URL",
    "ABS",
    "PLACE",
    "PUBLISH",
    "REMARK"
}
type_2_bibtex = {
    "in_proceedings":"INPROCEEDINGS",   # Workshops, conference proceedings.
    "in_journal":"ARTICLE",             # Official published journal, magazine article.
    "online":"?",                       # Online publication (e.g. arxiv, preprint).
    "tech. report":"TECHREPORT",        # Technical reports.
    "tech report":"TECHREPORT",
    "tech_report":"TECHREPORT",
    "in_book":"?",                      # Chapter in a book.
    "BSc thesis":"?",                   # Not so common, bachelors thesis.
    "BA thesis":"?",
    "MSc thesis":"?",                   # Masters thesis.
    "!PhD thesis":"PHDTHESIS",          # PhD thesis.
    "PhD thesis":"PHDTHESIS",
    "class report":"?",                 # Not so common.
    "presentation":"?",                 # Not so common.
    "patent":"?"
}
topkey_2_dataset = {
  # "Anonymized Internet Traces -> traces"
  "passive-stats"                     : "passive-metadata",
  "passive-realtime"                  : "?",
  "passive-generic"                   : "?",
  "passive-ipv6day-and-ipv6launch"    : "passive-ipv6launch-pcap",
  "passive-oc48"                      : "passive-oc48-pcap",
  "passive-2007"                      : "passive-2007-pcap",
  "passive-2008"                      : "passive-2008-pcap",
  "passive_2008"                      : "passive-2008-pcap",
  "passive-2009"                      : "passive-2009-pcap",
  "passive-2010"                      : "passive-2010-pcap",
  "passive-2011"                      : "passive-2011-pcap",
  "passive-2012"                      : "passive-2012-pcap",
  "passive-2013"                      : "passive-2013-pcap",
  "passive-2014"                      : "passive-2014-pcap",
  "passive_2014"                      : "passive-2014-pcap",
  "passive-2015"                      : "passive-2015-pcap",
  "passive-2016"                      : "passive-2016-pcap",
  "passive-2017"                      : "passive-2017-pcap",
  "passive-2018"                      : "passive-2018-pcap",
  "passive-2019"                      : "passive-2019-pcap",

  # "Topology with Archipelago -> ark"
  "topology-generic"                  : "?",
  "topology-ark-ipv4-traceroute"      : "ipv4_routed_24_topology",
  "topology-ark-ipv6-traceroute"      : "ipv6_allpref_topology",
  "topology-ark-itdk"                 : "internet-topology-data-kit",
  "topology-itdk"                     : "internet-topology-data-kit",
  "topology-ark-ipv4-prefix-probing"  : "ipv4_prefix_probing_dataset",
  "topology-ark-ipv4-aslinks"         : "ipv4_routed_topology_aslinks",
  "topology-ark-ipv6-aslinks"         : "ipv6_aslinks",
  "topology-ark-ipv6-routed48"        : "ipv6_allpref_topology",
  "topology-ark-ipv6_traceroute"      : "ipv6_allpref_topology",
  "topology-ark-dnsnames"             : ["ipv4_dnsnames","ipv6_dnsnames"],
  "topology-ark-dns-names"            : ["ipv4_dnsnames","ipv6_dnsnames"], 
  "topology-ark-tod"                  : "?",
  "topology-ark-activity"             : "?",
  "topology-ark-vela"                 : "tool-vela",

  # "Topology with Skitter -> skitter"
  "topology-skitter-ipv4"             : "skitter-traceroute",
  "topology-skitter-itdk"             : "skitter_internet_topology_data_kit",
  "toplogoy-skitter-itdk"             : "skitter_internet_topology_data_kit",
  "topology-skitter-aslinks"          : "skitter_aslinks_dataset",
  "topology-skitter-rlinks"           : "skitter_macroscopic_topology_data",
  "skitter-router-adjacencies"        : "skitter_router_level_topology_measurements",

  # "Topology with BGP -> bgp"
  "topology-as-relationships"         : "as_relationships",
  "topology-as-classification"        : "as_classification",
  "topology-as-organization"          : "as_organization",
  "topology-as-organizations"         : "as_organization",
  "as-organizations"                  : "as_organization",
  "topology-as-rank"                  : "asrank",
  "routeviews-generic"                : "?",
  "routeviews-prefix2as"              : "as-prefix",
  "topology-prefix2as"                : "as-prefix",
  "topology-routeviews-prefix2as"     : "as-prefix",

  # "UCSD Network Telescope -> telescope"
  "telescope-generic"                 : "ucsd_network_telescope",
  "telescope-2days-2008"              : "telescope-anon-twodays",
  "telescope-3days-conficker"         : "telescope-anon-conficker",
  "telescope-sipscan"                 : "telescope-sipsc",
  "telescope-patch-tuesday"           : "corsaro-patch-tuesday",
  "telescope-educational"             : "telescope-educational",
  "telescope-real-time"               : "ucsd_network_telescope",
  "backscatter-generic"               : "?",
  "backscatter-tocs"                  : "backscatter-tocs-originals",
  "backscatter-2004-2005"             : "telescope-backscatter",
  "backscatter-2006"                  : "telescope-backscatter",
  "backscatter-2007"                  : "telescope-backscatter",
  "backscatter-2008"                  : "telescope-backscatter",
  "backscatter-2009"                  : "telescope-backscatter",
  "witty worm"                        : "telescope-witty-worm",
  "code-red worm"                     : "telescope-codered-worm",

  # "Denial of Service Attacks -> ddos"
  "ddos-generic"                      : "?",
  "ddos-20070804"                     : "ddos-attack-2007",
  "ddos-20070806"                     : "ddos-attack-2007",

  # "Other Datasets -> other"
  "dns-rtt-generic"                   : "?",
  "dns-root-gtld-rtt"                 : "dns-root-gtld-rtt",
  "peeringdb"                         : "peeringdb_archive",
  "ixps"                              : "ixps",

  # "Paper Data and Tools -> paper"
  "complex_as_relationships"          : "2014-complex-data-supplement",
  "2006-pam-as-taxonomy"              : "2006-pam-as-taxonomy",
  "2016-periscope"                    : "?",
  "2013-midar"                        : "ark-midar",

  # Software
  "bgpstream"                         : "software:bgpstream",
  "scamper"                           : "software:scamper",
  "iffinder"                          : "software:iffinder",
  "mapnet"                            : "software:mapnet",  # TODO: Add software
  "coralreef"                         : "software:coralreef",
  "datcat"                            : "software:datcat", # TODO: Add software
  "dolphin"                           : "software:dolphin", # TODO: Add software
  "asfinder"                          : "software:asfinder",# TODO: Add software
  "netgeo"                            : "software:netgeo" # TODO: Add software
}
re_yml = re.compile(r".yaml")
re_jsn = re.compile(r".json")
re_pbd = re.compile(r"__pubdb")

# File Paths
data_papers = None

################################# Main Method ##################################

def main(argv):
    global seen_papers
    global seen_authors
    global author_data
    global topkeys
    global topkey_2_dataset
    global re_yml
    global re_jsn
    global re_pbd
    global data_papers

    parser = argparse.ArgumentParser()
    parser.add_argument("-d", type=str, default=None, dest="data_papers", help="Path to data-papers.yaml")
    args = parser.parse_args()

    # Edge Case: Exit if no data_papers is given.
    if args.data_papers is None:
        sys.exit()

    data_papers = args.data_papers

    # Update seen_papers with papers currently in sources/paper/
    update_seen_papers()

    # Update seen_authors with all authors found in sources/person/
    update_seen_authors()

    # Parse data_papers and create a new file for each paper.
    parse_data_papers()

############################### Helper Methods #################################

# Add each paper's ID to seen_papers from the source/paper directory.
def update_seen_papers():
    global seen_papers

    for file in os.listdir("sources/paper"):
        # Edge Case: Skip if file is not .json and excludes __pubdb from name.
        if not re_jsn.search(file) and not re_pbd.search(file):
            continue

        file = file.split("__")[0]
        seen_papers.add(file)


# Add each author's ID to seen_authors, and their JSON data to author_data.
def update_seen_authors():
    global seen_authors
    global author_data

    for file in os.listdir("sources/person"):
        # Edge Case: Skip if file is not .json.
        if not re_jsn.search(file):
            continue

        # Open the file and save its data.
        file = "sources/person/{}".format(file)
        with open(file, "r") as opened_file:
            data = json.load(opened_file)
        
        # Store the author's data.
        author_name = data["id"].split(":")[1]
        seen_authors.add(author_name)
        author_data[author_name] = data


# Opens a give .yaml file and parses each paper listed between delimeters.
def parse_data_papers():
    global re_yml
    global data_papers
    global topkeys

    # Parse data_papers as an encoded .bz2 file.
    if re_yml.search(data_papers):
        with open(data_papers, "r") as file:
            # Will store all the data for the current paper.
            curr_paper = ""
            curr_line = file.readline()
            while curr_line:
                # Edge Case: Skip commented lines.
                if curr_line[0] == "#":
                    curr_line = file.readline()
                    continue

                # Base Case: Parse current paper once delimeter is found.
                if "---" in curr_line:
                    if len(curr_paper) != 0:
                        parse_paper(curr_paper)
                    curr_paper = ""
                    curr_line = file.readline()
                    continue
                
                # Check if the current line has one of the TOPKEY values.
                topkey_in_line = False
                for topkey in topkeys:
                    if topkey in curr_line:
                        topkey_in_line = True
                
                # Strip newline characters from lines without TOPKEY values.
                if not topkey_in_line:
                    curr_paper = curr_paper.rstrip()
                    curr_paper += curr_line.strip()
                else:
                    curr_paper += curr_line.lstrip()
                curr_line = file.readline()

    # Edge Case: Exit if a given file couldn't be open.
    else:
        print("File must be a .yaml file to be opened.", file=sys.stderr)
        sys.exit()


# Pull out all necessary meta data from the given paper and print a JSON file.
def parse_paper(curr_paper):
    global author_data
    global type_2_bibtex

    # Dictionary that will be printed as a JSON.
    paper = {
        "__typename":"paper",
        "bibtextFields":{}
    }

    # Split the current paper into each line.
    curr_paper = curr_paper.split("\n")
    
    # Iterate over each line of the current paper.
    for line in curr_paper:
        # Split the current line between the TOPKEY, and its value.
        line = line.split(":")

        # Edge Case: Skip empty lines.
        if len(line) <= 0:
            continue

        # Check which TOPKEY is used for the current line.
        if "MARKER" in line[0]:
            paper["id"] = line[1].replace('"',"")
                    
        elif "TYPE" in line[0]:
            type = line[1].replace('"',"").strip()
            paper["bibtextFields"]["type"] = type_2_bibtex[type]

        elif "AUTHOR" in line[0]:
            # Create a list of authors.
            if "authors" not in paper:
                paper["authors"] = []

            # Handle the two seperate ways that authors can be stored.
            authors = line[1].replace('"',"")

            # Author's are either split by semicolon, or last name initial.
            if ";" in line[1]:
                authors = authors.split(";")
            else:
                authors = authors.split(".,")

            # Iterate over each author and add there an object for them.
            for author in authors:
                author = author.strip()
                author = re.split(r"\W+", author)
                
                # Format author's name into ID format.
                author_id = ""
                for name_part in author:
                    if len(name_part) >= 1:
                        author_id += "{}__".format(name_part)
                author_id = author_id[:-2]

                paper["authors"].append({
                    "person":"person:{}".format(author_id)
                })
                    
        elif "GEOLOC" in line[0]:
            locations = line[1].replace('"',"").split(";")

            # Edge Case: Apply the single location to all authors.
            if len(locations) != len(paper["authors"]):
                for author in paper["authors"]:
                    author_id = author["person"].split(":")[1]
                    author_orgs = update_author_data(author_id, locations[0])
                    author["oganizations"] = author_orgs
                continue
            
            # Iterate over each location and author object.
            for location, author in zip(locations, paper["authors"]):
                author_id = author["person"].split(":")[1]
                author_orgs = update_author_data(author_id, location)
                author["oganizations"] = author_orgs

        elif "TITLE" in line[0]:
            title = line[1].replace('"',"")
            paper["name"] = title

        elif "YEAR" in line[0]:
            date = line[1].replace('"',"").replace("-",".")
            paper["datePublished"] = date
            paper["date"] = date
        
        elif "TOPKEY" in line[0]:
            datasets = line[1].replace('"',"").split(",")
            # Edge Case: Add list for links if missing.
            if "links" not in paper:
                paper["links"] = []
            
            # Iterate over each dataset and link them to catalog datasets.
            for dataset in datasets:
                # Remove any whitespace.
                dataset = dataset.strip().lower()

                # Map the topkey_dataset to a catalog-data dataset.
                try:
                    dataset = topkey_2_dataset[dataset]
                except:
                    if len(dataset) == 0:
                        continue
                    dataset = topkey_2_dataset[dataset.replace(" ", "-")]

                # Append link to the dataset.
                if "software:" in dataset:
                    paper["links"].append({
                        "to":"{}".format(dataset)
                    })
                else:
                    # Edge Case: Handles datasets that are mapped to lists.
                    if isinstance(dataset, list):
                        for data in dataset:
                            paper["links"].append({
                                "to":"dataset:{}".format(dataset)
                            })
                    else:
                        paper["links"].append({
                            "to":"dataset:{}".format(dataset)
                        })

        elif "SERIAL" in line[0]:
            publisher = line[1].replace('"',"") 
            paper["publisher"] = publisher
            paper["bibtextFields"]["journal"] = publisher

        elif "VOLUME" in line[0]:
            # TODO:
            pass
        
        elif "CHAPTER" in line[0]:
            # TODO:
            pass

        elif "ARTICLE" in line[0]:
            # TODO:
            pass

        elif "PAGE" in line[0]:
            # TODO:
            pass

        elif "CTITLE" in line[0]:
            # TODO:
            pass

        elif "DOI" in line[0]:
            # TODO:
            pass

        elif "URL" in line[0]:
            # TODO:
            pass

        elif "ABS" in line[0]:
           paper["description"] = line[1].replace('"',"")

        elif "PLACE" in line[0]:
            # TODO:
            pass

        elif "PUBLISH" in line[0]:
            paper["bibtextFields"]["institutions"] = line[1].replace('"',"")
        
        elif "REMARK" in line[0]:
            # TODO:
            pass


# Helper function to update author_data.
#   @input author_id: The formatted ID for the current author.
#   @input location: The organization that will be added.
#   @return author_orgs: The list of this author's organizations.
def update_author_data(author_id, organization):
    global author_data

    # Add author from author_data, else the current location.
    if author_id in author_data and"organization" in author_data[author_id]:
        # Edge Case: Add the current or to org if missing.
        if organization not in author_data[author_id]["organization"]:
            author_obj = author_data[author_id]
            author_obj["organization"].append(organization)
    else:
        # Add the author to author_data
        name = author_id.split("__")
        first_name = name[-1]
        last_name = " ".join(map(str, name[:-1]))
        file_path = "sources/person/{}.json".format(author_id)

        # Add the author object to the author_data.
        author_data[author_id] = {
            "id":"person:{}".format(author_id),
            "__typename":"person",
            "filename":file_path,
            "nameLast":first_name,
            "nameFirst":last_name,
            "organization":[
                organization
            ]
        }
        author_orgs = author_data[author_id]["organization"]
        return author_orgs

# Run the script given the inputs from the terminal.
main(sys.argv[1:])