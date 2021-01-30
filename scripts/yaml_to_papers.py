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
    "PUBLISH"
}
type_2_value = {
    "in_proceedings",   # Workshops, conference proceedings.
    "in_journal",       # Official published journal, magazine article.
    "online",           # Online publication (e.g. arxiv, preprint).
    "tech. report",     # Technical reports.
    "in_book",          # Chapter in a book.
    "BSc thesis",       # Not so common, bachelors thesis.
    "MSc thesis",       # Masters thesis.
    "!PhD thesis",      # PhD thesis.
    "class report",     # Not so common.
    "presentation"      # Not so common.
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
    global re_yml
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

    # Dictionary that will be printed as a JSON.
    paper = {}

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
            # TODO: Unsure what to do for this TOPKEY
            pass

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
            paper["name"] = line[1].replace('"',"")

        elif "YEAR" in line[0]:
            paper["datePublished"] = line[1].replace('"',"")
        
        elif "TOPKEY" in line[0]:
            # TODO:
            pass

        elif "SERIAL" in line[0]:
            # TODO:
            pass

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
            # TODO:
            pass

        elif "PLACE" in line[0]:
            # TODO:
            pass

        elif "PUBLISH" in line[0]:
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