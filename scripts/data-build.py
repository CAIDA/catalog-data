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
#
__author__ = "Bradley Huffaker"
__email__ = "<bradley@caida.org>"
import json
import sys
import os
import re
import time
import datetime
import argparse
import subprocess
import lib.utils as utils
import unidecode
import csv
import copy

import binascii


######################################################################
## Parameters
######################################################################
import argparse
parser = argparse.ArgumentParser(description='Collections metadata of bgpstream users')
parser.add_argument('-s', '--summary', dest='summary_file', help='Summary file to read additional metadata in', required=True)
parser.add_argument('-r', '--redirects', dest='redirects_file', help='lists of redirects')
parser.add_argument("-i", dest="ids_file", help="ids_file", type=str)
parser.add_argument("-c", dest="schema_category_file", help="data schema categories", type=str)
parser.add_argument("-d", dest="schema_dataset_file", help="data schema datasets", type=str)
parser.add_argument("-D", dest="dates_skip", help="doesn't add dates, faster", action='store_true')
parser.add_argument("-R", dest="readable_output", help="indents the output to make it readaable", action='store_true')
args = parser.parse_args()

# used to plural
import nltk
nltk.download('wordnet')
#nltk.download('omw-1.4')
from nltk.stem.wordnet import WordNetLemmatizer
Lem = WordNetLemmatizer()

source_dir="sources"

id_info = {}
id_object = {}
id_paper = {}
id_id_link = {}
organization_ids = {}

# Score weights
# The score encodes that the word exist at a given level.
WORD_SCORE_WEIGHT = {
    "name":32,
    "id":16,
    "category":8,
    "tags":4,
    "other":2,
    "link":1
}
WORD_SCORE_WEIGHT_LINK = WORD_SCORE_WEIGHT["link"]
id_word_score = {}

personName_ids = {}
type_ids = {}

singular_plural = {}

re_tag = re.compile("^tag:")
re_only_white_space = re.compile("^\s*$")

#re_not_word = re.compile("[\s ,\?\.\(\)\:]+")
re_not_word = re.compile("[^a-z^A-Z^0-9]+")
re_word = re.compile("^[a-zA-Z0-9]+$",re.IGNORECASE)

re_html = re.compile("<[^>]+>")
re_id_illegal = re.compile("[^a-z^\d^A-Z]+")
re_type_name = re.compile("([^\:]+):(.+)")
re_readme_md = re.compile("^readme\.md$",re.IGNORECASE)

re_date_key = re.compile("^date",re.IGNORECASE)
re_not_digit = re.compile("[^\d]+")

re_placeholder = re.compile("___")

repo_url_default = "https://github.com/CAIDA/catalog-data"


# Weight used to create id scoring for search
# currently not used.
# id_score_node_weight = 20
# id_score_link_weight = .2

id_object_file = "id_object.json"
id_id_link_file = "id_id_link.json"
word_id_score_file = "word_id_score.json"
id_words_file = "id_words.json"
access_word_id_file = "access_word_id.json"
status_word_id_file = "status_word_id.json"
organization_ids_file = "organization_ids.json"
personName_ids_file = "personName_ids.json"
type_ids_file = "type_ids.json"

# We will be scoring based on the depth
category_id_score_file = "category_id_score.json"

pubdb_links_file = "data/pubdb_links.json"

filename_errors = {}

# Weights used to create word scoring for search
weight_default = 1
temp="""
key_weight = {
    "__typename":0,
    "id":0,
    "name": 10,
    "nameFirst": 10,
    "nameLast": 10,
    "tags": 10,
    "description": 5,
    "content": 3,
    "authors": 3
}
link_weight = {
    "Paper":.3,
    "Dataset":.5,
    "Software":.3,
    "Recipe":.3
}

type_key_w_type_w = {
    "datasets": {
        "key_weights": [
            ["name", 10],
            ["description",1],
            ["tags",.5]
        ],
        "link_weights":[ 
            ["papers",.5],
        ]
    },
    "papers": {
        "key_weights": [
            ["name", 10],
            ["description",8]
        ],
        "type_weights":[ 
            ["tags",.5],
            ["datasets", .5]
        ]
    }
}
"""

##################################
# Enumrated types 
##################################

enum_type_key_values = {
    "_all_":{
        "visibility":["public","links","hidden","private"],
    },
    "Software":{
        "status":["supported","unsupported","deprecated"]
    }
}



if len(sys.argv) > 1 and sys.argv[1] == "-f":
    date_lookup_force = True
else:
    date_lookup_force = False

# id_in_catalog stores the ids that are in catalog
# used if the catalog-data-caida directory is not here
id_in_catalog = set()

################################
# Category to Object Map
################################
category_object = {}

def main():

    # Load ids from the catalog
    if args.ids_file:
        with open(args.ids_file) as fin:
            for line in fin:
                id_in_catalog.add(line.rstrip())

    id_date_load(id_object_file)

    # valid object types
    object_types = set([
        "dataset",
        "license",
        "person",
        "paper",
        "presentation",
        "software",
        "media",
        "collection",
        "venue",
        "category"
    ])

    #######################
    #######################
    seen_id = {}

    #Goes through all generated objects in source paths
    for fname in sorted(os.listdir(source_dir)):
        path = source_dir+"/"+fname
        if fname == "solution" or fname == "recipe":
            obj = recipe_process(path)
        elif fname in object_types:
            print ("loading",path)
            type_ = fname
            for filename in sorted(os.listdir(path)):
                if re.search("\.json$",filename,re.IGNORECASE):
                    try:
                        info = json.load(open(path+"/"+filename))
                        if "filename" not in info:
                            info["filename"] = path+"/"+filename
                        obj = object_add(type_,info)
                        id = obj["id"]
                        if id in seen_id:
                             utils.warning_add(filename, "duplicate id found in\n "+ seen_id[id])
                        else:
                            seen_id[id] = filename
                        if "name" not in obj or obj["name"] == "":
                            utils.error_add(filename, "no name in oject")
                        if obj is None:
                            print ("parse error   ",path+"/"+filename)
                    except Exception as e:
                        print ("\nerror",path+"/"+filename)
                        print ("    ",e)
                        sys.exit(1)
        else:
            obj = None


    print ("processing obj")
    object_finished = set()
    for obj in list(id_object.values()):
        id_ = obj["id"]
        if id_ not in object_finished:
            object_finish(obj)
            object_finished.add(id_)

    if not args.dates_skip:
        print ("adding dates ( skipping '*___*' )")
        for obj in list(id_object.values()):
            object_date_add(obj)
    else:
        print ("skipping adding dates")

    print ("removing missing ids from id_id_links")
    missing = []
    for id0,id_link in id_id_link.items():
        if id0 not in id_object:
            missing.append(id0)
        else:
            m = []
            for id1 in id_link.keys():
                if id1 not in id_object:
                    m.append(id1)
            for id1 in m:
                del id_link[id1]
    if len(missing) > 0:
        utils.warning_add(f"Missing {len(missing)} ids:", f"{', '.join(str(x) for x in missing)}")
    for id0 in missing:
        del id_id_link[id0]

    ######################
    # tag objects linked to caida_data
    ######################
    tag_caida_data = "tag:used_caida_data"
    tag_obj = id_object[tag_caida_data] = {"__typename":"Tag", "id":"tag:used_caida_data", "name":"used CAIDA data", "filename":sys.argv[0]}
    ids = set()
    for id0,id_link in id_id_link.items():
        obj0 = id_object[id0]
        if obj0["__typename"] == "Dataset" and "tag:caida" in obj0["tags"]:
            for id1 in id_link.keys():
                obj1 = id_object[id1]
                if obj1["__typename"] != "Tag" and "tag:caida_data" not in obj1["tags"]:
                    if "tags" not in obj1:
                        obj1["tags"] = []
                    ids.add(obj1["id"])
                    if tag_caida_data not in obj1["tags"]:
                        obj1["tags"].append(tag_caida_data)

    ######################
    link = {"to":tag_caida_data}
    for id_ in ids:
        link_add(id_object[id_], link)

    #######################
    # Check that the objects are valid
    #######################

    type_checker = {
        "Person":person_add_names,
        "Dataset":object_checker,
        "Software":object_checker,
        "Paper":object_checker,
        "Media":object_checker
    }

    id_failed = []
    # Loop through the names in the id_object json file 
    for id_,obj in id_object.items():
        type_ = obj["__typename"]
        if type_ in type_checker:
            ## I think it is here where the object gets person add names again
            type_checker[type_](obj)
            
            #if message is not None:
            #    id_failed.append({"id":id_,"message":message})
                
    for id_msg in id_failed:
        id_ = id_msg["id"]
        msg = id_msg["message"]
        print ("removing[",msg,"]",id_)
        del id_object[id_]

    #######################
    # Remove keys with None values
    #######################
    print ("removing keys with none values")
    for obj in id_object.values():
        remove_keys_with_none_value(obj["filename"], None,obj)

    #######################
    # checking if collection members are missing
    #######################
    print ("checking collection members ids")
    for obj in id_object.values():
        if obj["__typename"] == "Collection" and "members" in obj:
            ids = []
            for id_ in obj["members"]:
                if id_ in id_object:
                    ids.append(id_)
                else:
                    utils.error_add(obj["filename"], obj["id"]+"'s member "+id_+" not found")

    ####################
    # Add in any redirects (id_old -> id_new)
    # These will all be hidden, ie not searchable
    ####################
    if args.redirects_file:
        print ("adding redirects:",args.redirects_file)
        redirects_add(args.redirects_file)

    ########################
    ## duplicate slide resources
    ########################
    #print ("duplicating slides into paper access")
    #duplicate_slides_in_access()

    #######################
    # Match up Papers with exact name media and presentation that match 
    #######################
    print ("Matching up Papers with media/presentations with the same name")
    papers_access_add_same_name()

    #######################
    # pubdb links
    #######################
    if os.path.exists(pubdb_links_file):
        print ("loading",pubdb_links_file)
        pub_links_load(pubdb_links_file)
    else:
        print("failed to file",pubdb_links_file)
        print("    type 'make links'")

    #######################
    # count none_tab_links
    #######################
    for id, obj in id_object.items():
        num_links = 0
        if id in id_id_link:
            for i in id_id_link[id].keys():
                if id_object[i]["__typename"] != "Tag":
                    num_links += 1
        id_object[id]["num_links_not_tag"] = num_links

    ######################
    # Parse out the access words and status of datasets
    ######################
    access_word_ids = {}
    status_word_ids = {}
    for obj in id_object.values():
        if "access" in obj:
            for access in obj["access"]:
                if "access" in access:
                    word = access["access"]
                else:
                    word = access["url"]
                if word not in access_word_ids:
                    access_word_ids[word] = []
                access_word_ids[word].append(obj["id"])
        if "status" in obj:
            curr_status = obj["status"]
            if curr_status not in status_word_ids:
                status_word_ids[curr_status] = []
            status_word_ids[curr_status].append(obj["id"])
            
                

    ######################
    # Load data schema for categories from file
    ######################
    print ("Adding schema's categories from",args.schema_category_file)
    schema_load_category_from_file(args.schema_category_file)

    ####################
    print ("Build Category Object map")
    category_object_build()

    ######################
    # Load data schema for datasets from file
    ######################
    print ("Adding schemas from",args.schema_dataset_file)
    schema_load_datasets_from_file(args.schema_dataset_file)

    #######################
    # set up category depths
    #######################
    print ("processing categories")
    category_id_score = schema_process()

    #######################
    # parse out the words from the fields
    #######################
    print ("adding words")
    
    for obj in id_object.values():
        word_scoring(obj)
    for id0, id1_link in id_id_link.items():
        if id0 not in id_word_score:
            id_word_score[id0] = {}
        w_s0 = id_word_score[id0]
        for id1 in id1_link.keys():
            if id0 < id1:
                w_s1 = id_word_score[id1]
                word_scoring_link(w_s0, w_s1)
                word_scoring_link(w_s1, w_s0)
    # Add in alternative plural/singlar

    print ("adding plural")
    word_add_plurals()
        
    word_id_score = {}
    for id_,word_score in id_word_score.items():
        for word,score in word_score.items():
            if word not in word_id_score:
                word_id_score[word] = {}
            word_id_score[word][id_] = score;

    #######################
    # Remove empty arrays 
    #######################
    print ("removing empty obj arrays")
    for obj in id_object.values():
        keys = []
        for key, value in obj.items():
            if list == type(value) and len(value) == 0:
                keys.append(key)
        for key in keys:
            del obj[key];

    ######################
    # Convert set to list
    ######################
    for name,obj in personName_ids.items():
        personName_ids[name] = list(obj)

    ######################
    # Create a type index
    ######################
    type_ids = {}
    for obj in id_object.values():
        t = obj["__typename"]
        if t not in type_ids:
            type_ids[t] = []
        type_ids[t].append(obj["id"])

    ######################
    # Load date info into id_object 
    ######################
    print ("Adding dataset date info")
    data_load_from_summary(args.summary_file)
    # Class copies categories to classes
    class_copy_from_category_keys(id_object.values())

    ######################
    # Create a word_id
    ######################
    id_words = {}
    for word, id_score in word_id_score.items():
        for i in id_score.keys():
            if i not in id_words:
                id_words[i] = set()
            id_words[i].add(word)
    for i,words in id_words.items():
        id_words[i] = list(words)

    #######################
    # check dataset status
    #######################
    for obj in id_object.values():
        for t in ["_all_", obj["__typename"]]:
            if t in enum_type_key_values:
                for key,valid_values in enum_type_key_values[t].items():
                    if key in obj and obj[key] not in valid_values:
                        utils.error_add(obj["filename"], f"{obj['id']}'s {key}'s \"{obj[key]}\" not in {', '.join(valid_values)}")
                        del obj[key]
    #######################
    # copy out doi && pull out access tag to access type
    #######################
    print ("Pulling DOIs out of access && pull out access tag to access type")
    count_access_no_tags = 0
    for obj in id_object.values():
        doi_set(obj)
        count_access_no_tags += access_type_from_tag_set(obj)
    if count_access_no_tags > 0:
        utils.error_add("", '%s Objects that are missing a tags and type; please add a type to each access object.' % count_access_no_tags)

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

    print ("writing",personName_ids_file)
    json.dump(personName_ids, open(personName_ids_file,"w"),indent=indent)

    print ("writing",type_ids_file)
    json.dump(type_ids, open(type_ids_file,"w"),indent=indent)

    print ("writing",id_id_link_file)
    json.dump(id_id_link, open(id_id_link_file,"w"),indent=indent)

    print ("writing",id_words_file)
    json.dump(id_words, open(id_words_file,"w"),indent=indent)
    
    print ("writing",word_id_score_file)
    json.dump(word_id_score, open(word_id_score_file,"w"),indent=indent)
    
    print ("writing",access_word_id_file)
    json.dump(access_word_ids, open(access_word_id_file,"w"),indent=indent)

    print ("writing",status_word_id_file)
    json.dump(status_word_ids, open(status_word_id_file,"w"),indent=indent)

    print ("writing",category_id_score_file)
    json.dump(category_id_score, open(category_id_score_file,"w"),indent=indent)

    #################
    for org,ids in organization_ids.items():
        organization_ids[org] = list(ids)
    print ("writing",organization_ids_file)
    json.dump(organization_ids, open(organization_ids_file,"w"),indent=indent)

########################### 
# Date
########################### 
mon_index={"jan":"01","feb":"02","mar":"03","apr":"04","may":"05","jun":"06"
          ,"jul":"07","aug":"08","sep":"09","oct":"10","nov":"11","dec":"12"}

id_date = {}
def id_date_load(filename):
    
    global id_date
    if os.path.exists(filename):
        try:
            id_date = json.load(open(filename,"r"))
        except ValueError as e:
            utils.error_add(filename, e.__str__())

def object_date_add(obj):
    today = datetime.date.today().strftime("%Y-%m")

    if obj["__typename"] == "Venue":
        if "dates" in obj and len(obj['dates']) >= 1:
            for date_url in obj["dates"]:
                if "date" not in obj or obj["date"] < date_url["date"]:
                    obj["date"] = utils.date_parse(date_url["date"])
        else:
            if "date" not in obj:
                if "deprecated" not in obj:
                    utils.error_add(obj["filename"], "missing date(s), please add date(s)")
    else:
        for key, value in obj.items():
            if key[:4] == "date" and type(value) == str:
                if obj[key].lower() == "ongoing":
                    obj[key] = today
                else:       
                    obj[key] = utils.date_parse(obj[key])
            

    ## Get github file modified dates 
    for key in ["dateObjectCreated", "dateObjectModified"]:
        if not date_lookup_force and obj["id"] in id_date and key in id_date[obj["id"]]:
            obj[key] = utils.date_parse(id_date[obj["id"]][key])
        else:
            # if the file is not a placeholder
            if not re_placeholder.search(obj["filename"]):
                if key == "dateObjectCreated":
                    cmd = "git log --diff-filter=A --follow --format=%aD -1 -- "
                else:
                    cmd = "git log --format=%aD -1 -- "

                result = subprocess.check_output(cmd+" "+obj["filename"],shell=True)
                values = result.decode().lower().split(" ")
            else:
                values = []
            date = today
            # if there was a date found, use as date (would not be found if placeholder)
            if len(values) >= 4:
                if values[2] in mon_index:
                    date = utils.date_parse(values[3]+"-"+mon_index[values[2]])
            obj[key] = date
            if obj["id"] not in id_date:
                id_date[obj["id"]] = {}
    
    # change date start to dateCreated for software
    #if obj["__typename"] == "Software":
    #    if "dateCreated" not in obj and "dateModified" not in obj:
    #        if "deprecated" in obj:
    #            utils.warning_add(obj["filename"], "missing dateCreated and dateModified, but is deprecated")
    #        else:
    #            utils.error_add(obj["filename"], "missing dateCreated and dateModified, please add dateCreated or dateModified")
    
    if "presenters" in obj:
        for person_venue in obj["presenters"]:
            if "date" in person_venue:
                obj["date"] = utils.date_parse(person_venue["date"])
        if "date" not in obj:
            if "deprecated" not in obj:
                utils.error_add(obj["filename"], "missing date, please add date")
    else:
        if "date" not in obj:
            obj["date"] = None
        type_key = {
            "Dataset":["dateEnd", "dateStart"], 
            "Paper":["datePublished"],
            "Software":["dateCreated","dateModified"],
            "Recipe":["dateObjectModified","dateObjectCreated"],
            "Tag":["dateObjectModified","dateObjectCreated"],
            "Collection":["dateObjectModified", "dateObjectCreated"]
        }
        type_ = obj["__typename"]
        if type_ in type_key:
            for key in type_key[type_]:
                if key in obj:
                    obj["date"] = obj[key]
                    break
            if obj["date"] is None:
                if "deprecated" not in obj:
                    utils.error_add(obj["filename"], "missing " + ", ".join(type_key[type_]) + ", please add " + ", ".join(type_key[type_]))
    

    #for dst,src in [["dateCreated","dateObjectCreated"], ["dateLastModified","dateObjectModified"]]:
    #    if dst not in obj:
    #        obj[dst] = obj[src]
    #if obj["__typename"] == "Dataset":
        #if "dateStart" in obj:
            #obj["date"] = obj["dateStart"]
        #else:
            #utils.warning_add(obj["filename"],"dataset requires dateStart")
            #obj.pop("date",None)
    #else:
        #if "date" not in obj:
            #obj["date"] = obj["dateLastUpdated"]
        #obj["date"] = utils.date_parse(obj["date"])

###########################

def data_print(): 
    for type,data in type_data.items():
        fname = data_dir+"/"+type+".json"
        print ("writing",fname)
        with open (fname,"w") as f:
            objects = []
            for object in data.values():
                objects.append(object)
            f.write(json.dumps(objects,indent=4, sort_keys=True))

        fname = data_dir+"/id_"+type+".json"
        print ("writing",fname)
        with open (fname,"w") as f:
            f.write(json.dumps(data,indent=4, sort_keys=True))

#############################
def remove_keys_with_none_value(filename, path, obj):
    t = type(obj)
    if t == dict:
        iter_ = obj.items()
    elif t == list:
        iter_ = enumerate(obj)
    else:
        iter_ = None 

    if iter_ is not None:
        nones = []
        nested = []
        for key, value in iter_:

            if path is None:
                path_key = key
            else:
                if t == dict:
                    path_key = path+"->"+key
                else:
                    path_key = path+"["+str(key)+"]"

            if value is None:
                nones.append([path_key, key])
            elif type(value) is dict or type(value) is list:
                nested.append([path_key, value])

        for path_key, key in nones:
            if path_key is not None and path_key != "date":
                utils.warning_add(filename, "none value for "+path_key)
            if t == dict:
                del obj[key]
            else:
                del obj[key:key+1]

        for path_key,child in nested:
            remove_keys_with_none_value(filename, path_key, child)

#############################


def object_add(type_, info): 
    info["__typename"] = type_ = type_.title()

    error = False
    if type_ == "Person":
        person_add_names(info)

    if "name" in info:
        info["__typename"] = type_.title()
        if "id" not in info:
            info["id"] = utils.id_create(info["filename"], info["__typename"],info["name"])
        else:
            info["id"] = utils.id_create(info["filename"], info["__typename"],info["id"])
    else:
        utils.error_add(info["filename"], "failed to find name:"+json.dumps(info))
        error = True
    
    if type_ == "Paper":
        if "datePublished"  in info:
            info["date"] = info["datePublished"]
        else:
            utils.error_add(info["filename"], "failed to find paper's date")
            error = True

        m = re.search("^paper:(\d\d\d\d)_(.+)", info["id"])
        if m:
            date,id_short = m.groups()
            id_paper[id_short] = info
        else:
            info["id"] = utils.id_create(info["filename"], info["__typename"],info["id"])

    elif type_ == "Category":
        if "id_short" not in info:
            info["id_short"] = info["id"]
        if "category_keys" in info:
            for cat in info["category_keys"]:
                if "id_short" not in cat:
                    cat["id_short"] = cat["id"]

    if not error:
        id_object[info["id"]] = info
        if "id_short" in info:
            id_short = utils.id_create(info["filename"], info["__typename"], info["id_short"])
            if id_short != info["id"]:
                if id_short not in id_object:
                    id_object[id_short] = info 
                else:
                    utils.error_add(info["filename"], f'{id_object["id"]}\'s id_short "{id_short}" already used')
                    del info["id_short"]
        elif type_ == "category":
            info["id_short"] = info["id"]

        return info
    print("line 611, error in object add for ", info["id"])
    return None

# Helper function 
re_third_party = re.compile("third party",re.IGNORECASE)
third_party_found = False
def organization_ids_add(org, id_):
    if re_third_party.search(id_):
        if not third_party_found:
            print ('ignoring organization "third party"', file=sys.stderr)
            third_party_found  = True
        return

    if org not in organization_ids:
        organization_ids[org] = set()
    organization_ids[org].add(id_)

re_caida = re.compile("caida",re.IGNORECASE)
re_caida_long = re.compile("Center for Applied Internet Data Analysis",re.IGNORECASE)
def object_finish(obj):

    ############
    # links 
    ############
    if "links" in obj:
        for link in obj["links"]:
            link_add(obj,link)
        del obj["links"]

    if "tags" not in obj:
        obj["tags"] = []

    # Add if CAIDA is organization
    is_caida = False
    if "organization" in obj:
        org = obj["organization"]
        organization_ids_add(org, obj["id"])
        if re_caida.search(org) or re_caida_long.search(org):
            is_caida = True

    for key in ["authors", "presenters"]:
        if key in obj:
            for person_org in obj[key]:
                if "organizations" in person_org:
                    for org in person_org["organizations"]:
                        organization_ids_add(org, obj["id"])
                        if re_caida.search(org) or re_caida_long.search(org):
                            is_caida = True

    if is_caida and "caida":
        organization_ids_add("CAIDA", obj["id"])
        if "caida" not in obj["tags"]:
            obj["tags"].append("caida")

    for key,value in obj.items():
        if (key == "tags" or key == "access") and obj[key]:
            objects = []
            filename = obj["filename"]
            if key == "tags":
                objects = [obj]
            else:
                for i, access in enumerate(obj["access"]):
                    if 'access' not in access:
                        utils.error_add(obj["filename"], "access requires an access field")
                    if 'url' not in access:
                        utils.error_add(obj["filename"], "access requires an url field")
                    if "tags" in access:
                        objects.append(access)
            for o in objects:
                for i,tag in enumerate(o["tags"]):
                    t = object_lookup_type_name(filename, "tag",tag)
                    if t is not None:
                        tid = o["tags"][i] = t["id"]
                        link_add(obj,tid)
        elif key == "access":
                    o = object_lookup_type_name(obj["filename"], "tag",tag)
                    if o is not None:
                        tag = obj["tags"][i] = o["id"]
                        link_add(obj,tag)
                    else:
                        utils.error_add(obj["filename"],"No object for access tag")
        elif key == "resources":
            for resource in value:
                if "name" not in resource:
                    utils.error_add(obj["filename"], "resources require a name field")
        #elif key == "resources":
        #    for resource in obj["resources"]:
        #        for i,tag in enumerate(resource[key]):
        #            resource["tags"][i] = object_lookup_type_name("tag",tag)["id"]

        elif re_date_key.search(key) and type(obj[key]) == str:
            date = utils.date_parse(obj[key])
            if date:
                obj[key] = date
            #values = re_not_digit.split(obj[key])
            #digits = ["1990","01","01","00","00","00"]
            #for i,value in enumerate(values):
                #digits[i] = value
            ##dt = datetime.datetime.strptime(" ".join(digits), "%Y %m %d %H %M %S")
            #date = int(time.mktime(dt.timetuple()))
            #obj[key] = "%s/%s/%s %s:%s:%s" % (digits[0],digits[1],digits[2],digits[3],digits[4],digits[5])

        #elif obj["__typename"] == "Venue" and key == "dates":
        #    for date_url in obj[key]:
        #        venue_add_date_url(obj,date_url["date"],date_url["url"])

        elif key == "persons" or key == "venues" or key == "presenters" or key == "authors":
                dirty = []
                i = 0
                persons = set()
                while i < len(obj[key]):
                    person_org = obj[key][i]
                    error = False
                    if type(person_org) == dict:
                        caida = False
                        if "organizations" in person_org:
                            for org in person_org["organizations"]:
                                if re.search("caida", org, re.IGNORECASE):
                                    caida = True
                        for k in ["person","presenter"]:
                            if k in person_org:
                                person = person_lookup_id(obj["filename"],person_org[k])
                                persons.add(person["id"])
                                if person is not None:
                                    if caida:
                                        if "tags" not in person:
                                            person["tags"] = []
                                        if "tag:caida" not in person["tags"]:
                                            person["tags"].append("tag:caida")
                                    person_org[k] = person["id"]
                                else:
                                    error = True

                        # For now we are not suppporting venues as objects, so replace with just # string name
                        if "venue" in person_org and "venue" == person_org["venue"][:5]:
                            vid = person_org["venue"]
                            if vid in id_object:
                                person_org["venue"] = id_object[vid]["name"]
                            else:
                                utils.error_add(obj["filename"], f'missing venue: {person_venue["venue"]}')
                                del person_org["venue"]
                    # if the people are in a list of person ids
                    elif type(person_org) == str and person_org[:7] == "person:":
                        person = person_lookup_id(obj["filename"], person_org)
                        persons.add(person["id"])
                        # link the object to the person as a author or presenter
                        if person is not None:
                            obj[key][i] = dict({"person": person["id"]})

                        else:
                            utils.error_add(obj["filename"], "person is none ${person_org}")
                            error = True
                    if error:
                        del obj[key][i]
                    else:
                        i += 1
                # add each person as a object and not a person:id link
                for person_id in persons:
                    # add links from the person to the obj
                    link_add(obj, person_id)
                    # add person id to the personName_ids.json
                    personName_add(obj, person_id)
        
        elif key == "licenses":
            licenses = list(obj[key])
            for i,id_ in enumerate(licenses):
                id_2 = utils.id_create(obj["filename"],"license",id_)
                if id_2 not in id_object:
                    name = id_[8:]
                    object_add("License", {
                        "id":id_2,
                        "name":id_[8:],
                        "filename":obj["filename"]
                    })
                obj[key][i] = id_object[id_2]["id"]
        else:
            obj[key] = tag_convert(obj["filename"], obj[key])

def person_lookup_id(filename, id_):
    if (type(id_) != str):
        utils.error_add(filename, "person id wrong type found:"+str(type(id_))+" wanted str : "+json.dumps(id_))
        return None

    id_ = id_.lower()
    if ":" in id_:
        if "person:" in id_:
            person = object_lookup_id(filename, id_)
        else:
            utils.error_add(filename, "expected person found "+id_)
            return None
    else:
        person = object_lookup_id(filename, "person:"+id_)
    if person is None:
        person = { 
            "id":id_, 
            "filename": filename
        }
        person = object_add("Person", person_add_names(person))
    return person

def object_lookup_type_name(filename, type_,name):
    if type_ == name[0:(len(type_)+1)]:
        name = name[(len(type_)+1):]
    id_ = utils.id_create(filename, type_,name)
    return object_lookup({
        "id":id_,
        "filename":filename, 
        "__typename":type_,
        "name":name
    })

def object_lookup_id(filename, id_):
    id_ = utils.id_create(filename,None,id_)
    if id_ in id_object:
        return id_object[id_]

    m = re_type_name.search(id_)
    if m:
        type_,name = m.groups()
        if type_ == "Person":
            return None

        return object_lookup({
            "id":id_,
            "filename":filename,
            "__typename":type_.title(),
            "name":name.replace("_"," ").title()
        })
    else:
        print ("failed to parse id",id_)
        sys.exit()

def object_lookup(info):
    type_ = info["__typename"] = info["__typename"].lower()
    info["__typename"] = type_.title()
    if "id" not in info:
        print("no id in info, : ", info)
        if "name" in info and "__typename" in info:
            id_ = utils.id_create(info["__typename"],info["name"])
            info["id"] = id_
        else:
            print ("no id or name,_typename",info)
            sys.exit()
    else:
        if not re.search("^"+type_,info["id"]):
            info["id"] = info["__typename"]+":"+info["id"]
    id_ = info["id"]
    if id_ not in id_object:
        obj = object_add(info["__typename"], info)
        if obj is not None:
            object_finish(obj)
            return obj
    else:
        return id_object[id_]

def tag_convert(filename, obj,padding=""):
    type_ = type(obj)
    if type_ == dict:
        for key,value in obj.items():
            if "tags" == key and type(value) == list:
                for i,tag in enumerate(obj["tags"]):
                    obj["tags"][i] = object_lookup_type_name(filename, "tag",tag)["id"]
            else:
                obj[key] = tag_convert(filename, value,padding + " ")

    elif type_ == list:
        for i,value in enumerate(obj):
            obj[i] = tag_convert(filename, value,padding + " ")

    return obj

# add a person to the person id file
def personName_add(obj, person_id):
    names = person_id.split(":")[1].split("__")
    if len(names) == 2:
        first_name, last_name = names
    else:
        utils.error_add(obj["filename"],"failed to parse person `"+person_id+"'")
        last_name = names[0]
        first_name = ""
    i = obj["id"]
    for name in [first_name, last_name]:
        if name not in personName_ids:
            personName_ids[name] = set()
        personName_ids[name].add(i)

def link_add(obj,link,p=False):

    a = []
    for k in ["from","to"]:
        if type(link) == str:
            a = [link]
        else:
            if k in link:
                a.append(link[k])
    
    if type(link) == str:
        id_original = link
        id_new = utils.id_create(obj["filename"],None,link)
        link = { "from":obj["id"], "to":id_new }
    else:
        if "to" in link:
            link["from"] = obj["id"]
            id_original = link["to"]
            id_new = link["to"] = utils.id_create(obj["filename"],None,link["to"])
        elif "from" in link:
            link["to"] = obj["id"]
            id_original = link["from"]
            id_new = link["from"] = utils.id_create(obj["filename"],None,link["from"])
        else:
            utils.error_add(obj["filename"],"link has no from or to"+json.dumps(link))
            return None

    if id_new is None:
        utils.error_add(obj["filename"],"invalid id "+id_original)
        return None

    if id_new not in id_object:
        if id_new not in id_in_catalog:
            utils.error_add(obj["filename"], "can't find id "+id_new)
        return None


    if link["from"] == link["to"]:
        utils.warning_add(obj["filename"], "can't link to itself: "+link["from"])
        return None

    links = []
    for a_b in [["from","to"],["to","from"]]:
        a,b = a_b
        a_id = link[a]
        b_id = link[b]

        # Don't add links from objects to categories, instead add id_short 
        # from categories to objects.  ie we want them to be searchable 
        if b_id[:8] == "category":
            if b_id in id_object and "id_short" in id_object[b_id]:
                a = b
                if a == "from":
                    b = "to"
                else:
                    b = "from"
                b = "from"
                b_obj = id_object[b_id]
                b_id = a_id
                a_id = "category:"+b_obj["id_short"]
            else:
                continue
        l = {
            "from":a_id,
            "to":b_id
            }
        if a+"_label" in link:
            l["from_label"] = link[a+"_label"]
        if b+"_label" in link:
            l["to_label"] = link[b+"_label"]
        if "label" in link:
            l["label"] = link["label"]
        links.append([a_id, b_id, l])

        if a_id not in id_id_link:
            id_id_link[a_id] = {}
        if b_id in id_id_link[a_id]:
            for key,value in link.items():
                if key not in id_id_link[a_id][b_id]:
                    id_id_link[a_id][b_id][key] = value
        else:
            id_id_link[a_id][b_id] = l
    return True

#############################

def recipe_process(path):
    rep_url = get_url()+"/blob/master/"
    recipe_dir = set()
    skipped = []
    obj = None
    for root, dirs, files in os.walk(path):
        error = False
        if re.search(path+"/[^/]+$",root):
            tabs = []
            info = None
            for fname in files:
                assets_dir = re.sub("^sources","/assets",root)
                filename = root +"/"+fname
                if re_readme_md.search(fname):
                    with open(filename) as f:
                        inside = False
                        data = None
                        for line in f:
                            # process content after JSON 
                            if info is not None:
                                line = replace_markdown_urls(assets_dir,line)
                                #line = replace_markdown_urls(rep_url+root, line)
                                #if re_markdown_url.search(line):
                                info["content"] += line

                            # process JSON 
                            elif re.search("~~~",line):
                                if inside:
                                    if data == "":
                                        break
                                    try:
                                        info = json.loads(data)
                                        if "id" not in info:
                                            info["id"] = root.split("/")[-1]
                                        info["id"] = "recipe:"+info["id"]
                                        info["filename"] = filename
                                        info["__typename"] = "Recipe"
                                        info["content"] = ""
                                        data = None
                                    except ValueError as e:
                                        error = True
                                        utils.error_add(filename, e.__str__())
                                        break
                                else:
                                    data = ""
                                inside = not inside
                            elif data is not None:
                                data += line
                        
                        #if "content" in info:
                        #    info["content"] = markdown.markdown(info["content"])
                    errors = []
                    if info is None:
                        info = {}

                    if not error: 
                        object_add("Recipe", info)
                elif os.path.isfile(filename) and fname[0] != ".":
                    extention = filename.split(".")[-1].lower()
                    if extention in ["py","pl","txt","md"]:
                        with open(filename,"r") as fin:
                            tab_content = None
                            for line in fin:
                                if tab_content is None:
                                    tab_content = line
                                else:
                                    tab_content += line
                            if extention == "md":
                                f = "md"
                            else:
                                f = "text"
                            tabs.append({
                                "name":fname,
                                "format":f,
                                "content":tab_content
                            })
            if len(tabs) > 0 and info is not None:
                if "tabs" in info:
                    info["tabs"].extend(tabs)
                else:
                    info["tabs"] = tabs

re_markdown_url = re.compile("^(.*)(\[[^\]]+\]\()([^\)]+\))([\s\S]*)", re.IGNORECASE)
re_html_url = re.compile("^(.*)(<\s*a[^<]+href=[\'\"])([^\'^\"]+)([\s\S]*)",re.IGNORECASE)
re_image_url = re.compile("^(.*)(<\s*img[^<]+src=[\'\"])([^\'^\"]+)([\s\S]*)",re.IGNORECASE)
re_url_absolute = re.compile("^https?:")
re_mailto = re.compile("^mailto:")

def replace_markdown_urls(assets_dir,line):
    temp = line
    for regex in [re_markdown_url, re_html_url, re_image_url]:
        found = True
        index_code = []
        while found:
            m = regex.search(line)
            if m:
                before, label, url, after = m.groups()
                url = url.strip()
                if not re_url_absolute.search(url) and not re_mailto.search(url):
                    url = f"{assets_dir}/{url}"
                index = "\0"+str(len(index_code))+":"
                index_code.append([index,label+url])
                line = before+index+after
                found = True
            else:
                found = False
        for index,code in reversed(index_code):
            line = re.sub(index,code,line)

    if "asrank-download-asn" in line:
        print (line)
    return line


def get_url():
    filename = ".git/config"
    if os.path.exists(filename):
        re_remote = re.compile('^\[([^\s]+) "([^"]+)"')
        re_url = re.compile("\s+url = ([^\s]+)")
        url = None
        with open(filename) as f:
            origin_found = False
            for line in f:
                m = re_remote.search(line)
                if m:
                    type_, source = m.groups()
                    if "remote" == type_ and "origin" == source:
                        origin_found = True
                    else:
                        origin_found = False
                else:
                    m = re_url.search(line)
                    if origin_found and m:

                        url = m.group(1).replace(":","/")
                        url = re.sub('.+\@','https://', re.sub(".git$","",url ))
                        break
        if url is None:
            url = repo_url_default
            utils.error_add(filename, "failed to find origin url, using "+url)
    else:
        url = repo_url_default
        utils.warning_add(filename, "does not exist (this is normal for a submodule)")

    return url

#############################

def person_add_names(person):
    if "name" in person and ", " in person["name"]:
        names = person["name"].split(", ")
        person["nameLast"] = names[0]
        person["nameFirst"] = names[1]

    else:
        if "nameFirst" not in person or "nameLast" not in person:
            if "person:" in person["id"][:7]:
                names = person["id"][7:].split("_")
            else:
                names = person["id"].split("_")
            person["nameLast"] = names[0].title()
            person["nameFirst"] = " ".join(names[1:]).title()
    person["name"] = person["nameLast"]+", "+person["nameFirst"]
    unidecoded_person = unidecode.unidecode(person["id"])
    
    if unidecoded_person != person["id"]:
        ## add non-unidecoded name in names array
        utf8_names = { 'first': person["nameFirst"], 'last': person['nameLast'] }

        # Add special character names to the names array 
        if 'names' in person:
            if utf8_names not in person['names']:
                person['names'] = person['names'] + [utf8_names]
        else:
            person['names'] = [utf8_names]
        
        # update names to be non special characters
        person["nameLast"] = unidecode.unidecode(person["nameLast"])
        person["nameFirst"] = unidecode.unidecode(person["nameFirst"])
        person["name"] = person["nameLast"]+", "+person["nameFirst"]
        
        
    for key in ["nameFirst","nameLast"]:
        if key not in person or person[key] is None:
            person[key] = ""
            print ("failed to find",key,person)
    
    return True


def object_checker(obj):
    if "name" not in obj:
        if "Person" == obj["__typename"]:
            obj["name"] = obj["nameLast"]+", "+obj["nameFirst"]
        else:
            values = obj["id"].split(":")
            obj["name"] = ":".join(values[1:]).replace("_"," ")

    return True

#############################
## TODO: Searches through the alias if there is a person (get ascii and non ascii )
## Could also check for aliases // add alias to dictionary here 
def word_scoring(obj, recursive=False):
    global singlar_plural
    word_weights = []
    word_score = {}
    
    ## Adding words and their weights from each key 
    for key,value in obj.items():
        word_freq = word_freq_get(value)
        if key in WORD_SCORE_WEIGHT:
            weight = WORD_SCORE_WEIGHT[key]
        else:
            weight = WORD_SCORE_WEIGHT["other"]
        for word_original, freq in word_freq.items():
            word_weights.append([word_original, weight])

    ## Adding categories from the schema
    if "schema" in obj:
        cat_words = set()
        for table in obj["schema"]:
            word_scoring_category_key(table,cat_words)
        for word in cat_words:
            word_weights.append([word, WORD_SCORE_WEIGHT["category"]],)

    ## Checking aliases in person and adding weights for the names
    if obj["id"].split(":")[0] == "person" and "names" in obj:
        for name in obj["names"]:
            for key in ["nameFirst", "nameLast"]:
                if key in WORD_SCORE_WEIGHT:
                    word_weights.append([name[key], WORD_SCORE_WEIGHT[key]])

    ## score up the weights for all the words
    for word_original, weight in word_weights:
        ## Add additional word, additional to LEM, add UNIDECODED version 
        if word_original is not None: 
#            for word in [word_original, Lem.lemmatize(word_original), unidecode.unidecode(word_original)]:
            for word in [word_original]:
                if word not in word_score:
                    word_score[word] = weight
                else:
                    word_score[word] = word_score[word] | weight
    id_word_score[obj["id"]] = word_score

def word_scoring_category_key(info,cat_words):
    if "category" in info:
        cat_words.add(info["category"])

    if "category_keys" in info:
        for cat_key in info["category_keys"]:
            for key in ["category","category_key"]:
                if key in cat_key:
                    cat = cat_key[key]
                    if type(cat) is dict:
                        for k in ["id","id_short","name"]:
                            if k in cat:
                                w = cat[k]
                                if "category:" in w:
                                    w = w[9:]
                                cat_words.add(w)
        
def word_scoring_link(w_s0, w_s1):
    for word, score in w_s1.items():
        # If the weight comes from more then a link, and it already is included in the object 
        if score > WORD_SCORE_WEIGHT_LINK and word in w_s0:
            w_s0[word] = w_s0[word] | WORD_SCORE_WEIGHT_LINK

        # word_freq = word_freq_get(value)
        # 
        # for word_original,freq in word_freq.items():
        #    if len(word_original) > 1:
        #        word_original = word_original.lower()
        #        first = True
        #        for word in [word_original, Lem.lemmatize(word_original)]:
        #            if word and (first or word != word_original):
        #                first = False
        #                if word != word_original:
        #                    singular_plural[word] = word_original
        #                if word not in word_score:
        #                    word_score[word] = weight*freq
        #                else:
        #                    word_score[word] += weight*freq 

seen_value = set()
re_not_letter = re.compile("[^a-z^A-z]+")
re_not_empty = re.compile("[^\s]")
def word_freq_get(value):
    word_freq = {}
    type_ = type(value)
    if str == type_:
        if value in id_object:
            obj = id_object[value]
            t = obj["__typename"]
            keys = []
            if t == "Person":
                keys  = ["nameFirst","nameLast"]
            elif t == "Tag":
                keys = ["name"]
            #else:
                #if t not in seen_value:
                    #print (t)
                    #seen_value.add(t)

            for key in keys:
                if key in obj:
                    word_freq[obj[key].lower()] = 1.0/len(keys)
        else:
            words = re_not_word.split(re_html.sub("",unidecode.unidecode(value.lower()) ))
            total = len(words)
            for word in words:
                if len(word) > 0 and re_word.search(word): 
                    if word in word_freq:
                        word_freq[word] += 1/total
                    else:
                        word_freq[word] = 1/total
                #else:
                #    print (word)

    elif list == type_ or dict == type_:
        if list == type_:
            values = value
        else:
            values = value.values()
        num_elements = len(values)
        for val in values:
            w_f = word_freq_get(val)
            for w,f in w_f.items():
                if w in word_freq:
                    word_freq[w] += 1
                else:
                    word_freq[w] = 1
    #print (json.dumps(word_freq,indent=4))

    # additoinal words
    words = list(word_freq.keys())
    for word in words:
        if re_not_letter.search(word):
            for w in re_not_letter.split(word):
                if len(w) > 1 and re_not_empty.search(w):
                    if w in word_freq:
                        word_freq[w] += word_freq[word]
                    else:
                        word_freq[w] = 1

    return word_freq


# Couldn't find a package that converted to singular to plural
# So used this method to record that information
def word_add_plurals():
    for id_,word_score in id_word_score.items():
        plural_score = {}
        for word,score in word_score.items():
            if word in singular_plural:
                plural = singular_plural[word]
                if plural in plural_score:
                    plural_score[plural] += score
                else:
                    plural_score[plural] = score
        for plural,score in plural_score.items():
            if plural in word_score:
                plural_score[plural] += score
            else:
                word_score[plural] = score


#############################

def category_object_build():
    for obj in id_object.values():
        if obj["__typename"] == "Category":
            category_object[obj["id"][9:]] = obj
            category_object[obj["id_short"]] = obj

def schema_process():
    category_id_depth = {}
    depth_max = 0

    for id_,obj in id_object.items():
        if False and "schema" in obj:
            print (obj["id"],"schema  ------------------------")
            for i, table in enumerate(obj["schema"]):
                table_name = f"table[{i}]"

                keys = []
                properties = set()
                table_build_keys_properties(obj["filename"], table_name, table, keys, properties)

                table["keys"] = []
                for key in keys:
                    if "_source" in key:
                        source = key["_source"]
                        del key["_source"]
                    else:
                        source = table_name+'["keys"]'

                    if key_update(obj["filename"], source, key, properties):
                        link_add(obj, { "to":key["category"]["id"]})
                        category_keys_add(table, "keys", key)
                        key = key.copy()
                        category_keys_add(obj, "category_keys", key)

                if len(table["keys"]) < 1:
                    del table["keys"]

        #for dataset in datasets:
        #    if "category_keys" in dataset:
        #        dataset["category_keys"] \
        #                    = sorted(dataset["category_keys"],key=lambda c:[c["category"]["id"],c["category_key"]["id"]])

        if obj["__typename"] != "Category" and "category_keys" in obj:
            for key in obj['category_keys']:
                cats = key["category"]["id"][9:].split(".")
                name = None
                depth = len(cats)
                name_depths = []
                for cat in cats:
                    if name is None: 
                        name = cat
                    else:
                        name += "."+cat
                    name_depths.append([name, depth])
                    depth -= 1
                name_depths.append([key['category']['id_short'], 1])
                    
                for name, depth in name_depths:
                    if name not in category_id_depth:
                        category_id_depth[name] = {}
                    if id_ not in category_id_depth[name] or category_id_depth[name][id_] > depth:
                        category_id_depth[name][id_] = depth

                    if depth_max < depth:
                        depth_max = depth

    category_id_score = {}
    num_cats = len(category_id_depth)   
    for category, id_depth in category_id_depth.items():
        category_id_score[category] = {}
        for id_,depth in id_depth.items():
            category_id_score[category][id_] = pow(num_cats+1,depth_max-depth)
    
    return category_id_score


def table_build_keys_properties(filename, table_name, table, keys, properties):
    if "properties" in table:
        for n,prop in table["properties"].items():
            table_build_keys_properties_helper(filename, table_name, [n], prop, keys, properties)

def table_build_keys_properties_helper(filename, table_name, names, prop, keys, properties,depth=""):
    depth += ">"
    
    if type(prop) == dict:
        if "properties" in prop:
            for n,p in prop["properties"].items():
                names_copy = names.copy()
                names_copy.append(n)
                table_build_keys_properties_helper(filename, table_name, names_copy, p, keys, properties, depth)
        else:
            name = ">".join(names)
            properties.add(name)
            if "key" in prop:
                key = prop["key"]
                key["property"] = name
                key["_source"] = f"{table_name}>{name}"
                keys.append(key)
                del prop["key"]

def category_keys_add(obj, field_name, key):

    if field_name not in obj:
        obj[field_name] = []
    else:
        for k in obj[field_name]:
            if k["category"]["id"] == key["category"]["id"] and k["category_key"]["id"] == key["category_key"]["id"]:
                return
    # clean up 
    key = copy.deepcopy(key)
    if "category_keys" in key["category"]:
        del key["category"]["category_keys"]
    if "properties" in key["category_key"]:
        del key["category_key"]["properties"]
    if "category_keys" == field_name and "properties" in key:
        del key["properties"]

    if "__typename" in obj:
        link_add(obj, {"to":key["category"]["id"]})
    obj[field_name].append(key)

def key_replace_ids(filename, source, key, properties= None):
    missing = []
    for k in ["category","category_key"]:
        if k not in key:
            missing.append(k)

    if len(missing) > 0:
        utils.error_add(filename, f'{source} must have {", ".join(missing)}')
        return False 

    # Find and replace the category
    cat_id = key["category"]
    if cat_id not in category_object:
        utils.error_add(filename, f"{source} {cat_id} not found")
        return False 
        
    cat = key["category"] = category_object[cat_id]

    # Find and replace the category
    found = False
    category_key = key["category_key"]
    if "category_keys" in cat:
        for c_k in cat["category_keys"]:
            if c_k["id"] == category_key or c_k["id_short"] == category_key:
                key["category_key"] = c_k
                found = True
                break

    if not found:
        utils.error_add(filename, f"{source}'s in {cat_id}'s category_key, '{category_key}' not found")
        return False

    if properties is not None and not key_check_properties(filename, source, key, properties):
        return False
    return True

def key_check_properties(filename, source, key, properties):

    key_id = key["category"]["id"]+"+"+key["category_key"]["id"]

    if "property" in key:
        props = key["category_key"]["properties"]
        if len(props) != 1:
            utils.error_add(filename, f'{source} key {key_id} has property, but found {",".join(props)}')
            return  False 
        key["properties"] = {
            key["property"]:props[0]
        }
        del key["property"]

    # must have both category and columns 
    if "properties" not in key:
        utils.error_add(filename, f'{source} {key_id} missing properties')
        return  False 

    # Check all the properties exist
    col_key= "table.properties"
    attr_key = "category,properties"
    missing = {
        col_key:[],
        attr_key:[]
    }
    for prop,attr in key["properties"].items():
        if prop not in properties:
            missing[col_key].append(prop)

        if attr not in key["category_key"]["properties"]:
            missing[attr_key].append(attr)
    if len(missing[col_key]) > 0 or len(missing[attr_key]):
        for k in [col_key, attr_key]:
            if len(missing[k]) > 0:
                utils.error_add(filename, f'{k} unmatched columns: {", ".join(missing[k])}')
        return False 

    return True


###################
# Duplicate slide resources in access
# Currently UNUSED
###################
def duplicate_slides_in_access():
    objs = []
    for obj in id_object.values():
        if obj["__typename"] == "Paper":
            id_ = obj["id"]
            if id_ in id_id_link:
                objs.append(obj)

    for obj in objs:
        for i in id_id_link[obj["id"]].keys():
            o = id_object[i]
            if o["__typename"] == "Presentation":
                for o1, o2,label in [[obj, o, "slides"], [o, obj, "paper"]]:
                    if "access" not in o1:
                        o1["access"] = [ ]
                    t,n = o2["id"].split(":")
                    o1["access"].append(tag_convert(o1["filename"], {
                        "access":"public",
                        "url":f"https://catalog.caida.org/{t}/{n}",
                        "tags":[label] 
                    }))
                if "access" in o: 
                    for a in o["access"]:
                        for tag in a["tags"]:
                            if "video" in tag:
                                if "access" not in obj:
                                    obj["access"] = [ ]
                                obj["access"].append({
                                    "access":"public",
                                    "url":a["url"],
                                    "tags":a["tags"]
                                })


            
###################
#
###################
def id_lookup(id_):
    if id_ in seen:
        return id_

    yearless = id_yearless(id_)
    if id_yearless in name_id:
        return name_id[id_yearless]

    print ("failed to find", id_)
    return None

def id_yearless(id_):
    m = re.search("(.+):(\d\d\d\d)_(.+)",id_)
    if m:
        type_,date,name = m.groups()
        return type_+":"+name
    return id_

def pub_links_load(filename):
    for link in json.load(open(filename,"r")):
        if link[0] in id_object and link[1] in id_object:
            obj = {
                "filename":filename,
                "id":link[0]
                }
            link_add(obj,link[1])

def data_load_from_summary(filename):
    with open(filename,"r") as fin:
        for line in fin:
            if len(line) == 0 or line[0] == "#":
                continue
            metadata = json.loads(line)
            metadata["filename"] = filename
            catalog_id = metadata["catalog_id"]
            if catalog_id in id_object:
                obj = id_object[catalog_id]
                # Overwrites the following fields, if found in dataset summary file
                for key in ["dateStart","dateEnd","status", "doi"]:
                    if key in metadata:
                        if key in ["dateStart","dateEnd"]:
                            # FIXME: Quick fix; Need to normalize data format to YYYYMMDD
                            if (len(metadata[key]) == 8):
                                obj[key] = datetime.datetime.strptime(metadata[key], "%Y%m%d").strftime("%Y-%m-%d")
                        elif key != "" or key is not None:
                            obj[key] = metadata[key]

                    if "size_total" in metadata:
                        if "size" in metadata["size_total"]:
                            obj["size"] = metadata["size_total"]["size"]
            else:
                utils.error_add(filename, "no matching id for {}".format(catalog_id))

def redirects_add(filename):
    re_empty = re.compile("^\s*$")
    with open ("data/redirects.csv") as fin:
        keys = None
        for row in csv.reader(fin, delimiter=',',quotechar='"'):
            if len(row) < 0 or row[0][0] == '#':
                continue
            row = list(map(str.strip, row)) 
            if keys == None:
                keys = row
                for i,key in enumerate(keys): 
                    if key == "old_id" or key == "id_old":
                        keys[i] = "id"
            else:
                deprecated = {}
                id_ = row[0]
                for i,v in enumerate(row):
                    if i == 0 or re_empty.search(v):
                        continue
                    if keys[i] == "autoredirect":
                        deprecated[keys[i]] = True
                    else:
                        deprecated[keys[i]] = v

                if id_ in id_object:
                    utils.error_add(filename, "deprecated "+id_+" duplicate of "+id_object[id_]["filename"])
                else:
                    values = id_.split(":")
                    if len(values) == 2:
                        t,n = values
                        id_object[id_] = {
                            "__typename":t.capitalize(),
                            "id":id_,
                            "name": "redirect",
                            "deprecated":deprecated,
                            "visibility":"hidden"
                        }
                    else:
                        utils.error_add(filename,"failed to parse id: "+id_)
            

######################################33
# Load Schema and Categories from file
def schema_load_category_from_file(fname):
    re_category_key = re.compile("category_key",re.IGNORECASE)
    re_empty = re.compile("^\s*$")
    with open(fname) as fin:
        keys = None
        category_key_index = None
        category = None
        linenum = 0
        for line in fin:
            linenum += 1
            values = line.rstrip().split("\t")
            if category_key_index is None:
                for i, value in enumerate(values):
                    if re_category_key.search(value):
                        category_key_index = i
                        break
                if category_key_index is None:
                    utils.error_add(f'{fname}[{linenum}]', "Failed to find category_key on first line")
            elif keys is None:
                keys = values
            else:
                if re_empty.search(values[0]):
                    i = category_key_index
                else:
                    i = 0
                while i < len(values):
                    if i == 0:
                        if category is not None:
                            object_add("category", category)
                            category_key = None
                        category = {
                            "filename":f'{fname}[{linenum}]',
                            "category_keys":[]
                        }

                    key = keys[i]
                    value = values[i]
                    if not re_empty.search(value):
                        if i < category_key_index:
                            category[key] = value
                        else:
                            if i == category_key_index:
                                category_key = {}
                                category["category_keys"].append(category_key)
                            if key == "properties":
                                value = re.split("\s*;\s*", value)
                            category_key[key] = value
                    i += 1
        if category is not None:
            object_add("category",category)

def schema_load_datasets_from_file(filename):
    re_empty = re.compile("^\s*$")
    with open(filename) as fin:
        keys = None
        dataset = None
        datasets = []
        seen = set()

        temp="""

        linenum = 0
        for line in fin:
            linenum += 1
            values = line.rstrip().split("\t")
            if keys is None:
                keys = values
            else:
                if not re_empty.search(values[0]):
                    i = values[0]
                    if i in id_object:
                        dataset = id_object[i]
                        datasets.append(dataset)
                        seen = set()
                    else:
                        utils.error_add(f'{filename}[{linenum}]', f"failed to find dataset {i}")
                        dataset = None
                if dataset is not None:
                    cat_nam  = None
                    for i,value in enumerate(values):
                        if keys[i] == "category" and not re_empty.search(value) and i+1 < len(values) and not re_empty.search(values[i+1]):
                            cat = value
                            nam = values[i+1]
                            if cat in category_object:
                                cat = category_object[cat]
                                found = False
                                for n in cat["category_keys"]:
                                    if n["id"] == nam or ("id_short" in n and n["id_short"] == nam):
                                        nam = n
                                        found = True
                                        break
                                if found:
                                    id_ = cat["id"]+"+"+nam["id"]
                                    if id_ not in seen:
                                        seen.add(id_)
                                        cat_nam = {
                                            "category":cat,
                                            "category_key":nam
                                        }
                                        if i+2 < len(values) and not re_empty.search(values[i+2]):
                                            cat_nam["type"] = "self"
                                        category_keys_add(dataset, "category_keys", cat_nam)
                                else:
                                    utils.error_add(f"{filename}[{linenum}]",f"failed to find {cat['id']}'s category_key {nam}")
                            else:
                                utils.error_add(f"{filename}[{linenum}]",f"failed to find category {cat}")
"""
        linenum = 0
        for line in fin:
            linenum += 1
            values = line.rstrip().split("\t")
            if keys is None:
                keys = values
            else:
                if not re_empty.search(values[0]):
                    i = values[0]
                    if i in id_object:
                        dataset = id_object[i]
                        datasets.append(dataset)
                        seen = set()
                    else:
                        utils.error_add(f'{filename}[{linenum}]', f"failed to find dataset {i}")
                        dataset = None
                if dataset is not None:
                    cat_nam  = None
                    for i,value in enumerate(values):
                        if keys[i] == "category" and not re_empty.search(value) and i+1 < len(values) and not re_empty.search(values[i+1]):
                            key = {
                                "category":value,
                                "category_key":values[i+1]
                            }
                            if key_replace_ids(filename, f"line [{linenum}", key):
                                category_keys_add(dataset, "category_keys", key)

def class_copy_from_category_keys(objects):
    for obj in objects:
        if "category_keys" in obj and obj["__typename"] != "Category":
            obj["class_namespaces"] = []
            for cat_name in obj["category_keys"]:
                missing = False 
                for k in ["category","category_key"]: 
                    if k not in cat_name:
                        missing = True
                        break
                    if "name" not in cat_name[k]:
                        cat_name[k]["name"] = cat_name[k]["id_short"]
                if missing:
                    del obj["class_namespaces"]
                    continue 

                cat = cat_name["category"]
                key = cat_name["category_key"]
                obj["class_namespaces"].append({
                    "class":{
                        "id":"class"+cat["id"][8:],
                        "shortName":cat["id_short"],
                        "__typename":"Class"
                    },
                    "namespace":{
                        "id":key["id"],
                        "name":key["name"],
                        "shortName":key["id_short"],
                    }
                })

# The goal is to have a "good" doi at the end of the code.
def doi_set(obj):
    # If doi is not set, but there is a doi link in resources,
    # set doi to that link 
    if ("doi" not in obj or obj["doi"] is None) and "resources" in obj:
        index = None
        for i,info in enumerate(obj["resources"]):
            if "name" in info and info["name"].lower() == "doi":
                index = i
                break
        if index is not None:
            obj["doi"] = obj["resources"][index]["url"]
            del obj["resources"][index]
            if len(obj["resources"]) < 1:
                del obj["resources"]

    # If there is a doi set, fix it to the doi.org format
    if ("doi" in obj):
        obj["doi"] = obj["doi"].strip()
        doi_norm = "https://doi.org/"
        # drop "dx" from domain
        if ("dx.doi.org" in obj["doi"] or "www.doi.org" in obj["doi"]):
            obj["doi"] = doi_norm + obj["doi"].split("doi.org/")[1]
        # normalize alphanumeric forms to full URL
        elif ("doi:" in obj["doi"]):
            obj["doi"] = doi_norm + obj["doi"].replace("doi:", "")
        # determine if only the doi number is provided
        elif (obj["doi"][:3] == "10."):
            obj["doi"] = doi_norm + obj["doi"]
        # normalize empty string DOIs to null
        elif (obj["doi"] == ""):
            obj["doi"] = None
        elif (doi_norm not in obj["doi"]):
            utils.warning_add(obj["filename"], "doi not normalized to the url format with " + doi_norm + ': '+ obj['doi'])

## Helper function pulls out first access tag and creates access type
def access_type_from_tag_set(obj):
    curr_id = obj["id"]
    count = 0
    if "access" not in obj:
        return count
    else:
        # for each access in an object
        for curr_access in obj["access"]:
            # ignore if no tags
            if "tags" not in curr_access or "type" in curr_access:
                if "tags" not in curr_access and "type" not in curr_access:
                    utils.error_add(obj['filename'], "access does not have tags or type")
                    count += 1
                continue
                
            else:
                new_type = curr_access["tags"][0]
                if len(new_type.split(':')) != 2:
                    utils.error_add(obj['filename'], "access tag is not in correct format tag:<tag>")
                else:
                    # remove the "tag:" from the tag
                    curr_access["type"] = curr_access["tags"][0].split(':')[1].replace("_", " ")
                    # remove the first tag from tags field
                    if len(curr_access["tags"]) == 1:
                        # print("deleting", curr_access)
                        del curr_access["tags"]
                    else:
                        curr_access["tags"] = curr_access["tags"][1:]
        return count
        

def papers_access_add_same_name():
    # add the tags video and slide (with test filename)
    for tag in ["tag:video", "tag:slides"]:
        if tag not in id_object:
            object_add("Tag", {
                "id":tag,
                "name":tag[4:],
                "filename": "test"
            })
    for obj in id_object.values():
        i = obj["id"]
        if obj["__typename"] == "Paper":
            # check if the current obj is linked to anything 
            if i in id_id_link:
                for j in id_id_link[i].keys():
                    # get the linked object
                    o_j = id_object[j]
                    # get the type of the linked object
                    t = o_j["__typename"]
                    if t == "Media" or t == "Presentation":
                        if t == "media":
                            tag = "tag:video"
                            access_type = "video"
                        else:
                            tag = "tag:slides"
                            access_type = "slides"
                        if obj["name"].lower() == o_j["name"].lower():
                            if "access" in o_j:
                                for access in o_j["access"]:
                                    if "url" in access:
                                        if "access" not in obj:
                                            obj["access"] = []
                                        obj["access"].append({
                                            "url":access["url"],
                                            "access":access["access"],
                                            # "tags": [tag],
                                            "type": access_type
                                            })
                                        break


main()
