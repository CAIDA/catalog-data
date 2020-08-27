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
import argparse
import json
import sys
import os
import copy
import re
import time
import datetime
#import markdown2
import subprocess
import lib.utils as utils

source_dir="sources"

id_info = {}
id_object = {}
id_paper = {}
id_id_link = {}

id_word_score = {}

re_tag = re.compile("^tag:")
re_only_white_space = re.compile("^\s*$")

re_not_word = re.compile("[\s ,\?\.\(\)\:]+")
re_word = re.compile("^[a-z]+$",re.IGNORECASE)

re_html = re.compile("<[^>]+>")
re_id_illegal = re.compile("[^a-z^\d^A-Z]+")
re_type_name = re.compile("([^\:]+):(.+)")
re_readme_md = re.compile("^readme\.md$",re.IGNORECASE)

re_date_key = re.compile("^date",re.IGNORECASE)
re_not_digit = re.compile("[^\d]+")

# Weight used to create id scoring for search
# currently not used.
# id_score_node_weight = 20
# id_score_link_weight = .2

id_object_file = "id_object.json"
id_id_link_file = "id_id_link.json"
word_score_id_file = "word_score_id.json"
pubdb_links_file = "data/pubdb_links.json"

filename_errors = {}

# Weights used to create word scoring for search
weight_default = 1
key_weight = {
    "__typename":0,
    "id":0,
    "name": 10,
    "tags": 10,
    "description": 5,
    "content": 3
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
        "group"
    ])

    #######################
    #######################
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
                        if obj is None:
                            print ("parse error   ",path+"/"+filename)
                    except ValueError as e:
                        print (path+"/"+filename)
        else:
            obj = None


    for obj in list(id_object.values()):
        object_finish(obj)

    print ("adding dates")
    for obj in list(id_object.values()):
        object_date_add(obj)

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

    print ("checking objects")
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
    # pubdb links
    #######################
    if os.path.exists(pubdb_links_file):
        print ("loading",pubdb_links_file)
        pub_links_load(pubdb_links_file)
    else:
        print("failed to file",pubdb_links_file)
        print("    type 'make links'")

    #######################
    # ca
    #######################
    for i in range(0,10):
        for obj in id_object.values():
            object_score_update(obj)
        
    print ("adding words")
    word_score_id = {}
    for id_,word_score in id_word_score.items():
        for word,score in word_score.items():
            if word not in word_score_id:
                word_score_id[word] = []
            word_score_id[word].append([score,id_])
    for word,score_ids in word_score_id.items():
        word_score_id[word] = sorted(score_ids,reverse=True)

    #for score_id in word_score_id["rank"]:
        #print ("   ",score_id)



    #######################
    # print files
    #######################
    print ("writing",id_object_file)
    json.dump(id_object, open(id_object_file,"w"),indent=4)

    print ("writing",id_id_link_file)
    json.dump(id_id_link, open(id_id_link_file,"w"),indent=4)

    print ("writing",word_score_id_file)
    #json.dump(word_score_id, open(word_score_id_file,"w"),indent=4)
    json.dump(word_score_id, open(word_score_id_file,"w"))

###########################
def error_add(filename, message):
    print ("error",filename,message)
    if filename not in filename_errors:
        filename_errors[filename] = []
    filename_errors[filename].append(message)

def error_print():
    for filename,errors in filename_errors.items():
        print ("error",filename)
        for error in errors:
            print ("    ",error)


########################### 
# Date
########################### 
mon_index={"jan":"01","feb":"02","mar":"03","apr":"04","may":"05","jun":"06"
          ,"jul":"07","aug":"08","sep":"09","oct":"10","nov":"11","dec":"12"}

id_date = {}
def id_date_load(filename):
    global id_date
    if os.path.exists(filename):
        id_date = json.load(open(filename,"r"))

def object_date_add(obj):
    for key in ["dateCreated","dateLastUpdated"]:
        if not date_lookup_force and obj["id"] in id_date and key in id_date[obj["id"]]:
            obj[key] = id_date[obj["id"]][key]
        else:
            if key == "dateCreated":
                cmd = "git log --diff-filter=A --follow --format=%aD -1 -- "
            else:
                cmd = "git log --format=%aD -1 -- "

            result = subprocess.check_output(cmd+" "+obj["filename"],shell=True)
            values = result.decode().lower().split(" ")
            date = datetime.date.today().strftime("%Y.%m")
            if len(values) >= 4:
                if values[2] in mon_index:
                    date = values[3]+"."+mon_index[values[2]]
            obj[key] = date
            if obj["id"] not in id_date:
                id_date[obj["id"]] = {}

    if obj["__typename"] == "media" and "presenters" in obj:
        for person_venue in obj["presenters"]:
            if "date" in person_venue:
                obj["date"] = person_venue["date"]
    else:
        for type_key in [["Dataset","dateStart"], ["Paper","datePublished"]]:
            type_,key = type_key
            if obj["__typename"] == type_ and key in obj:
                obj["date"] = obj[key]

    if "date" not in obj:
        obj["date"] = obj["dateLastUpdated"]

    parts = re.split("[^\d]+",obj["date"])
    if len(parts) < 2:
        parts[2] = "01"
    obj["date"] = parts[0]+"."+parts[1]

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

    for key,value in obj.items():
        if key == "tags":
            for i,tag in enumerate(obj["tags"]):
                o = object_lookup_type_name(obj["filename"], "tag",tag)
                if o is not None:
                    tag = obj["tags"][i] = o["id"]
                    link_add(obj,tag)

        #elif key == "resources":
        #    for resource in obj["resources"]:
        #        for i,tag in enumerate(resource[key]):
        #            resource["tags"][i] = object_lookup_type_name("tag",tag)["id"]

        elif re_date_key.search(key) and type(obj[key]) == str:
            values = re_not_digit.split(obj[key])
            digits = ["1990","01","01","00","00","00"]
            for i,value in enumerate(values):
                digits[i] = value
            #dt = datetime.datetime.strptime(" ".join(digits), "%Y %m %d %H %M %S")
            #date = int(time.mktime(dt.timetuple()))
            obj[key] = "%s/%s/%s %s:%s:%s" % (digits[0],digits[1],digits[2],digits[3],digits[4],digits[5])

        #elif obj["__typename"] == "Venue" and key == "dates":
        #    for date_url in obj[key]:
        #        venue_add_date_url(obj,date_url["date"],date_url["url"])

        elif key == "persons" or key == "venues" or key == "presenters" or key == "authors":
                for person_org in obj[key]:
                    if type(person_org) == dict:
                        for k in ["person","presenter"]:
                            if k in person_org:
                                person = person_lookup_id(obj["filename"],person_org[k])
                                person_org[k] = person["id"]
                    elif type(person_org) == str and person_org[7:] == "person:":
                        person = person_lookup_id(obj["filename"],person_org)
                        obj[key][i] = person["id"]
        elif key == "licenses":
            licenses = list(obj[key])
            for i,id_ in enumerate(licenses):
                id_2 = utils.id_create(obj["filename"],None,id_);
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
    id_ = id_.lower()
    person = object_lookup_id(filename, id_)
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

def link_add(obj,info):

    if type(info) == str:
        to_original = info
        to = utils.id_create(None,None,info)
        info = { "to":to }
    else:
        if "to" in info:
            to_original = info["to"]
            to = info["to"] = utils.id_create(None,None,info["to"])
        else:
            error_add(obj["filename"],"link has no to"+json.dumps(info))
            return None


    if to is None:
        error_add(obj["filename"],"invalid id "+to_original)
        return None

    if to not in id_object:
        error_add(obj["filename"], "missing id "+to)
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
    recipe_dir = set()
    skipped = []
    obj = None
    for root, dirs, files in os.walk(path):
        if root == path:
            for fname in dirs:
                recipe_dir.add(root+"/"+fname)
        else:
            for fname in files:
                if root in recipe_dir and re_readme_md.search(fname):
                    filename = root +"/"+fname
                    info = None
                    errors = []
                    with open(filename) as f:
                        inside = False
                        data = None
                        for line in f:
                            if info is not None:
                                info["content"] += line
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
                                        errors.append("json error in "+filename+"\n")
                                        #print (e)
                                        #print ("parse failure",data)
                                        break
                                else:
                                    data = ""
                                inside = not inside
                            elif data is not None:
                                data += line
                    if info is None:
                        info = {}
                    #if "visibility" not in info or "public" != info["visibility"].lower():
                        #errors.append("invisible")


                    if len(errors) > 0:
                        skipped.append([",".join(errors), filename])
                    else:
                        #info["content"] = markdown2.markdown(info["content"])
                        obj = object_add("Recipe", info)     
    if len(skipped) > 0:
        print ("skipped")
        for msg, p in skipped:
            print ("    ",msg,p)

    return obj


#############################

def person_add_names(person):
    if "name" in person and ", " in person["name"]:
        names = person["name"].split(", ")
        person["nameLast"] = names[0]
        person["nameFirst"] = names[1]
    else:
        if "nameFirst" not in person or "nameLast" not in person:
            if "person:" in person["id"][:7]:
                names = person["id"][7:].split("__")
            else:
                names = person["id"].split("__")
            person["nameLast"] = names[0].title()
            person["nameFirst"] = " ".join(names[1:]).title()
    person["name"] = person["nameLast"]+", "+person["nameFirst"]
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

def object_score_update(obj, recursive=False):
    word_score = {"":1}
    for key,value in obj.items():
        if key in key_weight:
            weight = key_weight[key]
        else:
            weight = weight_default

        if weight == 0:
            continue

        word_freq = word_freq_get(value)
        for word,freq in word_freq.items():
            word = word.lower()
            if word not in word_score:
                word_score[word] = weight*freq
            else:
                word_score[word] += weight*freq 
    id1 = obj["id"]
    if id1 in id_id_link:
        for id2 in id_id_link[id1].keys():
            if id2 in id_word_score:
                if id1[0:3] == "tag" or id2[0:3] == "tag":
                    wieght = 0
                else:
                    wieght = .1
                if wieght > 0:
                    for word,score in id_word_score[id2].items():
                        if word not in word_score:
                            word_score[word] = wieght*score
                        else:
                            word_score[word] += wieght*score

    id_word_score[id1] = word_score

def word_freq_get(value):
    word_freq = {}
    type_ = type(value)
    if str == type_:
        if value in id_word_score:
            word_freq = id_word_score[value]
        else:
            words = re_not_word.split(re_html.sub("",value))
            total = len(words)
            for word in words:
                word = word.lower()
                if len(word) > 1 and re_word.search(word): 
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
    return word_freq

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

