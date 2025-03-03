#!  /usr/bin/env python3
__author__ = "Donald Wolfson, Bradley Huffaker"
__email__ = "dwolfson@zeus.caida.org, bhuffaker@ucsd.edu"
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
import difflib
import json
import sys
import re
import os
import yaml
import lib.utils as utils

#################################### Header ####################################

"""
    This script will create unique JSON objects based on metadata stored in the
    YAML file, data/data-papers.yaml. Each paper found is parsed for its TOPKEYS
    which map to manually inputted data about the paper. This script produces
    objects for papers, software, and media. Each new object is writted to its
    respective directory with the tag ___externallinks.json.
"""

############################## Global Variables ################################

# Datasets
seen_ids = set()        # Will hold all the current IDs
author_data = {}        # Will map all authors IDs to their JSON.
papers = {}             # Will hold each paper.     

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

alternate_links = ["software:", "media:", "paper:", "presentation:"]
re_yml = re.compile(r".yaml")
re_keys = re.compile(r".keys")
re_jsn = re.compile(r".json")
re_pubdb = re.compile(r"___pubdb")
re_ext = re.compile(r"___externallinks")

# File Paths
data_papers = None
data_papers_keys = "data/data-papers.keys"

################################# Main Method ##################################

def main(argv):
    global seen_papers
    global seen_authors
    global author_data
    global papers
    global topkeys
    global topkey_2_dataset
    global alternate_links
    global data_papers
    global data_papers_keys

    parser = argparse.ArgumentParser()
    parser.add_argument("-d", type=str, default=None, dest="data_papers", help="Path to data-papers.yaml")
    args = parser.parse_args()

    # Edge Case: Exit if no data_papers is given.
    if args.data_papers is None:
        sys.exit()

    data_papers = args.data_papers

    # Add the current set of paper and persons
    add_seen_ids(["sources/paper"])
    add_seen_authors("sources/person")

    # Parse data_papers and create a new file for each paper.
    parse_data_papers()


    # Print all the papers found to their respective JSON files.
    print_papers()

    # Print all the papers found to their respective JSON files.
    print_authors()

############################### Helper Methods #################################

# Add each paper's ID to seen_papers from the source/paper directory.
def add_seen_ids(dirs):
    global seen_ids

    for d in dirs:
        for fname in os.listdir(d):
            # Edge Case: Skip if file is not .json.
            if re_jsn.search(fname) and not re_pubdb.search(fname) and not re_ext.search(fname):
                with open(d+"/"+fname, "r") as opened_file:
                    data = json.load(opened_file)
                
                seen_ids.add(data["id"])

# Add each paper's ID to seen_papers from the source/paper directory.
def add_seen_authors(d):
    for fname in os.listdir(d):
        # Edge Case: Skip if file is not .json.
        if re_jsn.search(fname) and not re_ext.search(fname):
            f = d+'/'+fname
            with open(f, "r") as opened_file:
                person = json.load(opened_file)
                person['already_found'] = True
                utils.person_seen_add(f,person)

# Opens a give .yaml file and parses each paper listed between delimeters.
def parse_data_papers():
    global re_yml
    global data_papers
    global data_papers_keys
    global topkeys

    # Parse data_papers file.
    if re_yml.search(data_papers):
        with open(data_papers, "r") as fin:
            if re_keys.search(data_papers_keys):
                with open(data_papers_keys, "r") as fin2:
                    keys_gen = yaml.load_all(fin2,Loader=yaml.Loader)
                    next(keys_gen) # Skip first document in file
                    dataset_mappings = list(keys_gen)[0]
                    for paper in list(yaml.load_all(fin,Loader=yaml.Loader)):
                        parse_paper(data_papers, dataset_mappings, paper)

    # Edge Case: Exit if a given file couldn't be open.
    else:
        print("File must be a .yaml file to be opened.", file=sys.stderr)
        sys.exit()


# Pull out all necessary meta data from the given paper and print a JSON file.
#   @input curr_paper: A string where each \n is another TOPKEY.
def parse_paper(fname, dataset_mappings, key_value):
    global author_data
    global type_2_bibtex
    global papers
    global alternate_links

    # Dictionary that will be printed as a JSON.
    paper = {
        "__typename":"paper",
        "type":"paper",
        "authors":[],
        "bibtexFields":{},
        "links":[],
        "resources":[],
    }

    if "TITLE" in key_value: 
        title = key_value["TITLE"]
        paper["name"] = title


    re_year = re.compile(r"(\d\d\d\d)")
    re_year_month = re.compile(r"(\d\d\d\d).(\d\d)")
    for key, value in key_value.items():
        # Remove any whitespace, and the quotes around the data.
        value = value.rstrip()

        # Check which TOPKEY is used for the current line
        if "MARKER" == key:
            paper["id"] = utils.id_create(fname, "paper", value)
                    
        elif "TYPE" == key:
            paper_type = value
            paper["bibtexFields"]["type"] = paper_type

        elif "AUTHOR" == key:
            # Handle the two seperate ways that authors can be stored.
            authors = []

            # Edge case: author last name has suffix
            suffix = "Jr." in value
            value = value.replace("Jr.", "Jr")
            
            if ";" in value:
                authors = re.split(r"\s*;\s*", value)
            else:
                for author in re.split(r";\s*", re.sub(r"\.\s*,",";",value)):
                    names = re.split(r"\s*,\s*", author)
                    if len(names) == 4:
                        authors.append(names[0]+", "+names[1])
                        authors.append(names[2]+", "+names[3])
                    else:
                        # add the period back to Jr.
                        if suffix: 
                            author = author.replace("Jr", "Jr.")
                        authors.append(author)

            # Iterate over each author and add there an object for them.
            unparseable = []
            for author in authors:
                author = author.strip()
                #author = re.split(r"\W+", author)
                values = re.split(r"\s*,\s*",author)
                if len(values) > 0:
                    if len(values) == 2:
                        last_name, first_name = values
                        if len(first_name) == 1:
                            first_name = first_name + '.'
                    else:
                        unparseable.append(author)
                        continue  
                elif not re.search(r"^[a-z\.]+$", author, re.IGNORECASE):
                    print ("unparseable", '"'+author+'" in "'+title+'"', file=sys.stderr)
                    first_name = ""
                    last_name = author
                else:
                    first_name = ""
                    last_name = author

                author_id = add_author(fname, last_name, first_name);
                
                paper["authors"].append({
                    "person":author_id
                })

            if len(unparseable) > 0: 
                print ("TITLE:",title)
                print ("AUTHOR:", value)
                print ("  unparseable:",unparseable)
                return None 
                    
        elif "YEAR" in key:
            date_str = value
            m = re_year_month.search(date_str)
            date = None
            year = None
            month = None
            if m:
                year = m.group(1)
                month = m.group(2)
                date = year+"."+month
            else:
                m = re_year.search(date_str)
                if m:
                    year = m.group(1)
                    date = year
            if date:
                paper["datePublished"] = date
                paper["date"] = date
                paper["bibtexFields"]["year"] = year
                if month:
                    paper["bibtexFields"]["month"] = month
        
        elif "TOPKEY" in key:
            datasets = value.split(",")

            # Iterate over each dataset and link them to catalog datasets.
            for dataset in datasets:
                # Remove any whitespace.
                dataset = dataset.strip().lower()

                # Try to map the current dataset to a catalog dataset.
                if dataset[:8] == "dataset:":
                    dataset = dataset[8:]
                elif dataset in dataset_mappings:
                    dataset = dataset_mappings[dataset]
                elif len(dataset) == 0:
                    continue
                elif dataset.replace(" ", "-") in dataset_mappings:
                    dataset = dataset_mappings[dataset.replace(" ", "-")]
                elif dataset.replace("_", "-") in dataset_mappings:
                    dataset = dataset_mappings[dataset.replace("_", "-")]
                else:
                    keys = dataset_mappings.keys()
                    closest_match = difflib.get_close_matches(dataset, keys, 1)
                   
                    # Edge Case: Reverse the dataset if no match, then give up.
                    if len(closest_match) == 0:
                        dataset = dataset.replace(" ", "-").replace("_", "-")
                        dataset = dataset.split("-")
                        dataset.reverse()
                        dataset = "-".join(map(str, dataset))
                        if dataset in dataset_mappings:
                            dataset = dataset_mappings[dataset]
                        else:
                            continue
                    else:
                        dataset = dataset_mappings[closest_match[0]]


                # Append link to the dataset.
                alternate_link = False
                for alternate in alternate_links:
                    if alternate in dataset:
                        paper["links"].append({
                            "to":"{}".format(dataset)
                        })
                        alternate_link = True

                # So long as the dataset isn't an alternate link, add it.
                if not alternate_link:
                    # Edge Case: Handles datasets that are mapped to lists.
                    if type(dataset) is list:
                        for data in dataset:
                            paper["links"].append({
                                "to":"dataset:{}".format(data)
                            })
                    else:
                        paper["links"].append({
                            "to":"dataset:{}".format(dataset)
                        })

        elif "TAGS" == key:
            paper["tags"] = re.split(r",\s*",value)

        elif "SERIAL" == key:
            publisher = value
            paper["publisher"] = publisher
            paper["bibtexFields"]["journal"] = publisher

        elif "VOLUME" == key:
            volume = value
            paper["bibtexFields"]["volume"] = volume
        
        elif "CHAPTER" == key or "ARTICLE" == key:
            number = value
            paper["number"] = number

        elif "PAGE" == key:
            pages = value.replace("(", "").replace(")", "")
            paper["pages"] = pages
            paper["bibtexFields"]["pages"] = pages

        elif "CTITLE" == key:
            conference_title = value
            paper["publisher"] = conference_title
            paper["bibtexFields"]["bookTitle"] = conference_title

        elif "DOI" == key and value != "":
            paper["doi"] = value

        elif "URL" == key:
            url = value
            paper["access"] = [{
                "url":url,
                "access":"public",
                # "tags": [
                #     "PDF"
                # ],
                "type": "PDF"
            }]

        elif "ABS" == key:
            paper["description"] = value

        elif "PUBLISH" == key:
            paper["bibtexFields"]["institutions"] = value
        
        elif "REMARK" == key or "PLACE" == key:
            if "annotation" not in paper or len(paper["annotation"]) != 0:
                paper["annotation"] = value
            else:
                paper["annotation"] += " {}".format(value)

    # Only add papers that have ID.
    if "id" in paper:
        papers[paper["id"]] = paper


# Helper function add an author to author_data.
#   @input author_id: The formatted ID for the current author.
def add_author(fname, last_name, first_name):
    #print(fname)
    global author_data
    person = utils.person_seen_check(last_name, first_name)

    if person is None:
        type_,author_id = utils.id_create(fname, "person", last_name+"__"+first_name).split(":")
        if author_id not in author_data:
            file_path = "sources/person/{}___externallinks.json".format(author_id)
            author_data[author_id] = {
                "id":"person:{}".format(author_id),
                "__typename":"person",
                "filename":file_path,
                "nameLast":last_name,
                "nameFirst":first_name,
                "organizations":[]
            }

    else:
        author_id = person["id"]

    return author_id


# Print each paper to their respective JSON files.
def print_papers():
    global author_data
    global papers

    # Iterate over each paper and print their JSON.
    for paper_id, paper in papers.items():
        
        # Create a new file for each paper.
        if paper_id not in seen_ids:
            id_ = paper_id.split(":")[1]
            file_path = "sources/paper/{}___externallinks.json".format(id_)
            with open(file_path, "w") as paper_file:
                print(json.dumps(paper, indent=4), file=paper_file)


# Print each author to their respective JSON files.
def print_authors():
    global author_data

    # Iterate over each author and print their JSON.
    for author in author_data.values():
        if "already_found" not in author:
            if "filename" in author:
                file_path = author["filename"]
            else:
                file_path = "sources/person/{}___externallinks.json".format(author_id).split(":")

            # Create a new file, or update the current file for each paper.
            with open(file_path, "w") as author_file:
               print(json.dumps(author, indent=4), file=author_file)
        else:
            print ("skipping", author)

# Run the script given the inputs from the terminal.
main(sys.argv[1:])
