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
import json
import sys
import os
import re
import time
import datetime
import subprocess
import lib.utils as utils

import binascii

# used to plural
import nltk
nltk.download('wordnet')
from nltk.stem.wordnet import WordNetLemmatizer
Lem = WordNetLemmatizer()

source_dir="sources"

id_info = {}
id_object = {}
id_paper = {}
id_id_link = {}

# Score weights
# The score encodes that the word exist at a given level.
SCORE_WEIGHT = {
    "name":16,
    "id":8,
    "tags":4,
    "other":2,
    "link":1
}
SCORE_WEIGHT_LINK = SCORE_WEIGHT["link"]
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
access_word_id_file = "access_word_id.json"
pubdb_links_file = "data/pubdb_links.json"
personName_ids_file = "personName_ids.json"
type_ids_file = "type_ids.json"

filename_errors = {}

# Weights used to create word scoring for search
weight_default = 1
key_weight = {
    "__typename":0,
    "id":0,
    "name": 10,
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

id_missing = {}

if len(sys.argv) > 1 and sys.argv[1] == "-f":
    date_lookup_force = True
else:
    date_lookup_force = False

def main():

    id_date_load(id_object_file)

    # valid object types
    object_types = set([
        "dataset",
        "license",
        "person",
        "paper",
        "software",
        "media",
        "group",
        "venue"
    ])

    #######################
    #######################
    seen_id = {}
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
                        info["filename"] = path+"/"+filename
                        obj = object_add(type_,info)
                        id = obj["id"]
                        if id in seen_id:
                            print ("duplicate id found in\n   ",filename,"\n   ", seen_id[id])
                        else:
                            seen_id[id] = filename
                        if obj is None:
                            print ("parse error   ",path+"/"+filename)
                    except Exception as e:
                        print ("\nerror",path+"/"+filename)
                        print ("    ",e)
                        sys.exit(1)
        else:
            obj = None


    print ("processing obj")
    for obj in list(id_object.values()):
        object_finish(obj)

    print ("adding dates ( skipping '*___*' )")
    for obj in list(id_object.values()):
        object_date_add(obj)

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
    for id_,obj in id_object.items():
        type_ = obj["__typename"]
        if type_ in type_checker:
            type_checker[type_](obj)
            #if message is not None:
            #    id_failed.append({"id":id_,"message":message})
                
    for id_msg in id_failed:
        id_ = id_msg["id"]
        msg = id_msg["message"]
        print ("removing[",msg,"]",id_)
        del id_object[id_]

    #######################
    # printing errors
    #######################
    error_print()

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
    # Parse out the access words 
    ######################
    access_word_ids = {}
    for obj in id_object.values():
        if "access" in obj:
            for access in obj["access"]:
                word = access["access"]
                if word not in access_word_ids:
                    access_word_ids[word] = []
                access_word_ids[word].append(obj["id"])


    #######################
    # parse out the words from the fields
    #######################
    print ("adding words")
    for obj in id_object.values():
        word_scoring(obj)
    for id0, id1_link in id_id_link.items():
        w_s0 = id_word_score[id0]
        for id1 in id1_link.keys():
            if id0 < id1:
                w_s1 = id_word_score[id1]
                word_scoring_link(w_s0, w_s1)
                word_scoring_link(w_s1, w_s0)
    # Add in alternative plural/singlar
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

    # Removing the private objects
    print ("removing private")
    remove_private(id_object, id_id_link)

    #######################
    # print files
    #######################
    print ("writing",id_object_file)
    json.dump(id_object, open(id_object_file,"w"),indent=4)

    print ("writing",personName_ids_file)
    json.dump(personName_ids, open(personName_ids_file,"w"),indent=4)

    print ("writing",type_ids_file)
    json.dump(type_ids, open(type_ids_file,"w"),indent=4)

    print ("writing",id_id_link_file)
    json.dump(id_id_link, open(id_id_link_file,"w"),indent=4)

    print ("writing",word_id_score_file)
    json.dump(word_id_score, open(word_id_score_file,"w"),indent=4)
    
    print ("writing",access_word_id_file)
    json.dump(access_word_ids, open(access_word_id_file,"w"),indent=4)

###########################
def error_add(filename, message):
    if filename not in filename_errors:
        filename_errors[filename] = []
    filename_errors[filename].append(["  error",message])

def warning_add(filename, message):
    if filename not in filename_errors:
        filename_errors[filename] = []
    filename_errors[filename].append(["warning",message])

def error_print():
    if len(filename_errors) > 0:
        print ("")

    for filename,type_messages in filename_errors.items():
        print (filename)
        for t,m in type_messages:
            if "error" in t:
                color_code = "31" # red
            else:
                color_code = "1" # black
            print ("    \033["+color_code+"m",t+":",m,"\033[0m")

    if len(filename_errors) > 0:
        print ("")

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
            error_add(filename, e.__str__())

def object_date_add(obj):
    today = datetime.date.today().strftime("%Y-%m")

    for key in ["dateCreated","dateLastUpdated"]:
        if not date_lookup_force and obj["id"] in id_date and key in id_date[obj["id"]]:
            obj[key] = id_date[obj["id"]][key]
        else:
            if not re_placeholder.search(obj["filename"]):
                if key == "dateCreated":
                    cmd = "git log --diff-filter=A --follow --format=%aD -1 -- "
                else:
                    cmd = "git log --format=%aD -1 -- "

                result = subprocess.check_output(cmd+" "+obj["filename"],shell=True)
                values = result.decode().lower().split(" ")
            else:
                values = []
            date = today
            if len(values) >= 4:
                if values[2] in mon_index:
                    date = values[3]+"."+mon_index[values[2]]
            obj[key] = date
            if obj["id"] not in id_date:
                id_date[obj["id"]] = {}

    if obj["__typename"] == "Media" and "presenters" in obj:
        for person_venue in obj["presenters"]:
            if "date" in person_venue:
                obj["date"] = person_venue["date"]
            if "venue" in person_venue and "venue" == person_venue["venue"][:5]:
                vid = person_venue["venue"]
                if vid in id_object:
                    person_venue["venue"] = id_object[vid]["name"]
                else:
                    print ("    missing venue:",person_venue["venue"])
    else:
        for type_key in [["Dataset","dateStart"], ["Paper","datePublished"]]:
            type_,key = type_key
            if obj["__typename"] == type_ and key in obj:
                date = utils.date_parse(obj[key])
                if date:
                    obj["date"] = date
                    obj[key] = date
    key = "dateEnd"
    if key in obj:
        if obj[key].lower() == "ongoing":
            obj[key] = obj["date"] = today
        else:
            date = utils.date_parse(obj[key])
            if date:
                obj[key] = date

    if obj["__typename"] == "Dataset":
        if "dateStart" in obj:
            obj["date"] = obj["dateStart"]
        else:
            warning_add(obj["filename"],"dataset requires dateStart")
            obj.pop("date",None)
    else:
        if "date" not in obj:
            obj["date"] = obj["dateLastUpdated"]
        obj["date"] = utils.date_parse(obj["date"])

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
        error_add(info["filename"], "failed to find name:"+json.dumps(info))
        error = True
    
    if type_ == "paper":
        if "datePublished"  in info:
            info["date"] = info["datePublished"]
        else:
            error_add(info["filename"], "failed to find paper's date")
            error = True

        m = re.search("^paper:(\d\d\d\d)_(.+)", info["id"])
        if m:
            date,id_short = m.groups()
            id_paper[id_short] = info
        else:
            info["id"] = utils.id_create(filename, info["__typename"],info["id"])

    if not error:
        id_object[info["id"]] = info
        return info
    return None

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


    for key,value in obj.items():
        if (key == "tags" or key == "access") and obj[key]:
            objects = []
            filename = obj["filename"];
            if key == "tags":
                objects = [obj]
            else:
                for i, access in enumerate(obj["access"]):
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
                                            person["tags"] = ["caida"]
                                        else:
                                            person["tags"].append("caida")
                                    person_org[k] = person["id"]
                                else:
                                    error = True
                    elif type(person_org) == str and person_org[7:] == "person:":
                        person = person_lookup_id(obj["filename"],person_org)
                        persons.add(person["id"])
                        if person is not None:
                            obj[key][i] = person["id"]
                        else:
                            error = True
                    if error:
                        del obj[key][i]
                    else:
                        i += 1
                for person_id in persons:
                    link_add(obj, person_id)
                    personName_add(obj, person_id)
        elif key == "licenses":
            licenses = list(obj[key])
            for i,id_ in enumerate(licenses):
                id_2 = utils.id_create(obj["filename"],"license",id_);
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
        error_add(filename, "person id wrong type found:"+str(type(id_))+" wanted str : "+json.dumps(id_))
        return None

    id_ = id_.lower()
    if ":" in id_:
        if "person:" in id_:
            person = object_lookup_id(filename, id_)
        else:
            error_add(filename, "expected person found "+id_)
            return None
    else:
        person = object_lookup_id(filename, "person:"+id_)
    if person is None:
        person = { 
            "id":id_, 
            "filename":obj["filename"] 
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
    #print (len(padding),padding,obj)

    return obj

def personName_add(obj, person_id):
    #print (json.dumps(obj))
    names = person_id.split(":")[1].split("__")
    if len(names) == 2:
        first_name, last_name = names
    else:
        error_add(obj["filename"],"failed to parse person `"+person_id+"'")
        last_name = names[0]
        first_name = ""
    i = obj["id"]
    for name in [first_name, last_name]:
        if name not in personName_ids:
            personName_ids[name] = set()
        personName_ids[name].add(i)

def link_add(obj,info,p=False):

    if type(info) == str:
        to_original = info
        to = utils.id_create(obj["filename"],None,info)
        info = { "to":to }
    else:
        if "to" in info:
            to_original = info["to"]
            to = info["to"] = utils.id_create(obj["filename"],None,info["to"])
        else:
            error_add(obj["filename"],"link has no to"+json.dumps(info))
            return None


    if to is None:
        error_add(obj["filename"],"invalid id "+to_original)
        return None

    if to not in id_object:
        error_add(obj["filename"], "can't find id "+to)
        return False

    info["from"] = obj["id"]
    for a_b in [["from","to"],["to","from"]]:
        a,b = a_b
        a_id = info[a]
        b_id = info[b]
        link = {
            "from":a_id,
            "to":b_id
            }
        if a+"_label" in info:
            link["from_label"] = info[a+"_label"]
        if b+"_label" in info:
            link["to_label"] = info[b+"_label"]
        if "label" in info:
            link["label"] = info["label"]

        if a_id not in id_id_link:
            id_id_link[a_id] = {}
        if b_id in id_id_link[a_id]:
            for key,value in link.items():
                if key not in id_id_link[a_id][b_id]:
                    id_id_link[a_id][b_id][key] = value
        else:
            id_id_link[a_id][b_id] = link
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
                filename = root +"/"+fname
                if re_readme_md.search(fname):
                    with open(filename) as f:
                        inside = False
                        data = None
                        for line in f:
                            # process content after JSON 
                            if info is not None:
                                #line = replace_markdown_urls(rep_url+root, line)
                                #if re_markdown_url.search(line):
                                    #print (line.rstrip())
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
                                        error_add(filename, e.__str__())
                                        #print (e)
                                        #print ("parse failure",data)
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
                    #if "visibility" not in info or "public" != info["visibility"].lower():
                        #errors.append("invisible")

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
re_markdown_url = re.compile("^(.*\[[^\]]+\]\(\s*)([^\)]+)(\).*)")
def replace_markdown_urls(repo_url, line):
    m = re_markdown_url.search(line)
    if m:
        before,url,after = m.groups()
        #print (before, "|", url, "|", after)
        if url[0:4] != "http":
            url = repo_url +"/"+url
        return replace_markdown_urls(repo_url, before)+url+replace_markdown_urls(repo_url, after)
    else:
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
            error_add(filename, "failed to find origin url, using "+url)
    else:
        url = repo_url_default
        error_add(filename, "does not exist")

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
    for key in ["nameFirst","nameLast"]:
        if key not in person or person[key] is None:
            person[key] = ""
            print ("failed to find",key,person)
    #print (person["id"])
    #print ("    ",person["nameLast"]+", "+person["nameFirst"])
    return True


def object_checker(obj):
    if "name" not in obj:
        if "Person" == obj["__typename"]:
            obj["name"] = obj["nameLast"]+", "+obj["nameFirst"]
        else:
            values = obj["id"].split(":")
            obj["name"] = ":".join(values[1:]).replace("_"," ")
            print ("creating name for",obj["name"])

    return True

#############################


def word_scoring(obj, recursive=False):
    global singlar_plural
    word_score = {}
    for key,value in obj.items():
        if key in key_weight:
            weight = key_weight[key]
        else:
            weight = weight_default

        if weight == 0:
            continue

        for key,value in obj.items():
            word_freq = word_freq_get(value)
            if key in SCORE_WEIGHT:
                weight = SCORE_WEIGHT[key]

            else:
                weight = SCORE_WEIGHT["other"]

            for word_original, freq in word_freq.items():
                for word in [word_original, Lem.lemmatize(word_original)]:
                    if word not in word_score:
                        word_score[word] = weight
                    else:
                        word_score[word] = word_score[word] | weight
                    #print (key,weight, word, format(word_score[word],'b'))
    id_word_score[obj["id"]] = word_score

def word_scoring_link(w_s0, w_s1):
    for word, score in w_s1.items():
        # If the weight comes from more then a link, and it already is included in the object 
        if score > SCORE_WEIGHT_LINK and word in w_s0:
            w_s0[word] = w_s0[word] | SCORE_WEIGHT_LINK

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
            obj = id_object[value];
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
            words = re_not_word.split(re_html.sub("",value.lower() ))
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

###########################

def is_private(obj):
    return "visibility" in obj and obj["visibility"] == "private"

def remove_private(id_object, id_id_link):
    private = []
    for id0,id_link in id_id_link.items():
        obj = id_object[id0]
        if is_private(obj):
            private.append(id0)
        else:
            p = []
            for id1 in id_link.keys():
                obj = id_object[id1]
                if is_private(obj):
                    p.append(id1)
            for id1 in p:
                del id_link[id1]
    for id in private:
        del id_id_link[id]

    private = []
    for id, obj in id_object.items():
        if is_private(obj):
            private.append(id)
    for id in private:
        del id_object[id]

###################
#
###################
def id_lookup(id_):
    if id_ in seen:
        return id_

    yearless = id_yearless(id_)
    print ("looking from",yearless)
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

main()
