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

source_dir="sources"

id_object = {}
id_id_link = {}

id_word_score = {}

re_tag = re.compile("^tag:")
re_only_white_space = re.compile("^\s*$")
re_not_word = re.compile("[\s ,\?\.\(\)\:]+")
re_html = re.compile("<[^>]+>")
re_id_illegal = re.compile("[:\s\?]+")
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


# valid object types
object_types = set([
    "dataset",
    "solution",
    "license",
    "author",
    "paper",
    "presentation",
    "venue",
    "software",
    "media",
    "group"
])


# Weights used to create word scoring for search
weight_default = 1
key_weight = {
    "__typename":0,
    "id":0,
    "name": 10,
    "tags": 10
}
link_weight = {
    "paper":.3,
    "dataset":.5,
    "software":.3,
    "solutions":.3
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

def main():

    #######################
    #######################
    for fname in sorted(os.listdir(source_dir)):
        path = source_dir+"/"+fname
        if fname == "solutions":
            solutions_process(path)
        elif fname in object_types:
            print ("loading",path)
            type_ = fname
            for filename in sorted(os.listdir(path)):
                if re.search("\.json$",filename,re.IGNORECASE):
                    print ("   ",path+"/"+filename)
                    info = json.load(open(path+"/"+filename))
                    info["__typename"] = type_.lower()
                    object_lookup(info)

    #######################
    # Check that the objects are valid
    #######################
    type_checker = {
        "Author":author_checker,

        "Dataset":object_checker,
        "Software":object_checker,
        "Paper":object_checker,
        "Presentation":object_checker
    }

    id_failed = []
    for id_,obj in id_object.items():
        type_ = obj["__typename"]
        if type_ in type_checker:
            message = type_checker[type_](obj)
            if message is not None:
                id_failed.append({"id":id_,"message":message})

    for id_msg in id_failed:
        id_ = id_msg["id"]
        msg = id_msg["message"]
        print ("removing[",msg,"]",id_)
        del id_object[id_]

    #######################
    # look for missing ids
    #######################
    for obj in id_object.values():
        errors = []
        if "links" in obj:
            for link in obj["links"]:
                id_ = link["to"]
                if id_ not in id_object:
                    errors.append([obj["id"],"links",id_])
        if len(errors) > 0:
            for id_message_id in errors:
                id0,message,id1 = id_message_id
                print("missing",id0, message, id1)

    #######################
    # add dates
    #######################
    if os.path.exists(id_object_file):
        id_objs = json.load(open(id_object_file,"r"))
    else:
        id_objs = {}
    date = time.strftime("%Y/%m/%d %H:%M:%S")
    for id_,obj in id_object.items():
        if id_ in id_objs:
            for key in ["dateCreated","dateLastUpdated"]:
                if key in id_objs[id_]:
                    obj[key] = id_objs[id_][key]

            if "date" in id_objs[id_]:
                del id_objs[id_]["date"]
            if "date" in obj:
                del obj["date"]

            if obj != id_objs[id_]:
                #print (json.dumps(obj,indent=4))
                #print (json.dumps(id_objs[id_],indent=4))
                print ("updating",obj["id"])
                obj["dateLastUpdated"] = date
        for key in ["dateCreated","dateLastUpdated"]:
            if key not in obj:
                obj[key] = date

    date_type_key= {
        "dateset":"dateStart",
        "paper":"datePublished",
    }

    for obj in id_object.values():
        type_ = obj["__typename"]
        key = "------"
        if type_ == "presentation" and "venue" in obj:
            date = None
            for venue in obj["venue"]:
                if date is None or venue["date"] > date:
                    date = venu["date"]
            if date is not None:
                obj["date"] = date
        elif type == "venue" and "dates" in obj:
            date = None
            for d in obj["dates"]:
                if date is None or d["date"] > date:
                    date = d["date"]
            if date is not None:
                obj["date"] = date
        else:
            if type_ in date_type_key:
                key = date_type_key[type_]

            if key not in obj:
                key = "dateLastUpdated"
            obj["date"] = obj[key]

    #######################
    # ca
    #######################
    for i in range(0,10):
        for obj in id_object.values():
            object_score_update(obj)
        
    word_score_id = {}
    for id_,word_score in id_word_score.items():
        for word,score in word_score.items():
            if word not in word_score_id:
                word_score_id[word] = []
            word_score_id[word].append([score,id_])
    for word,score_ids in word_score_id.items():
        word_score_id[word] = sorted(score_ids,reverse=True)

    for score_id in word_score_id["rank"]:
        print ("   ",score_id)


    #######################
    # print files
    #######################
    print ("writing",id_object_file)
    json.dump(id_object, open(id_object_file,"w"),indent=4)

    print ("writing",id_id_link_file)
    json.dump(id_id_link, open(id_id_link_file,"w"),indent=4)

    print ("writing",word_score_id_file)
    json.dump(word_score_id, open(word_score_id_file,"w"),indent=4)


    sys.exit()

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

def object_lookup_type_name(type_,name):
    if type_ == name[0:len(type_)]:
        obj = object_lookup_id(name)
    else:
        id_ = type_+":"+re_id_illegal.sub("_",name)
        obj = object_lookup_id(id_)
        obj["__typename"] = type_
        obj["name"] = name
    return obj

def object_lookup_id(id_):
    id_ = id_.lower()
    m = re_type_name.search(id_)
    if m:
        type_,name = m.groups()
        #print (">>>",id_,type_,name)
        return object_lookup({
            "id":id_,
            "__typename":type_
        })
    else:
        print ("failed to parse id",id_)
        sys.exit()


def object_lookup(info):
    type_ = info["__typename"] = info["__typename"].lower()
    if "id" not in info:
        if "name" in info and "__typename" in info:
            id_ = info["__typename"]+":"+re_id_illegal.sub("_",info["name"])
            info["id"] = id_.lower()
        else:
            print ("no id or name,_typename",info)
            sys.exit()
    else:
        if not re.search("^"+type_,info["id"]):
            info["id"] = info["__typename"]+":"+info["id"]
    id_ = info["id"] = info["id"].lower()
    if id_ not in id_object:
        id_object[id_] = {"id":id_.lower(),"__typename":info["__typename"]}
    obj  = id_object[id_]

    object_types = set(["datasets","licenses","softwares","solutions","papers","publications"])
    for key in info.keys():
        if key == "links" or key == "tags":
            continue
            
        if key not in obj:
            if key in object_types:
                objs  = []
                for i in info[key]:
                    if type(i) == str:
                        o = object_lookup_id(i)
                    else:
                        o = object_lookup(i)
                    objs.append(o["id"])
                obj[key] = objs
            elif re_date_key.search(key) and type(info[key]) == str:
                values = re_not_digit.split(info[key])
                digits = ["1990","01","01","00","00","00"]
                for i,value in enumerate(values):
                    digits[i] = value
                #dt = datetime.datetime.strptime(" ".join(digits), "%Y %m %d %H %M %S")
                #date = int(time.mktime(dt.timetuple()))
                obj[key] = "%s/%s/%s/ %s:%s:%s" % (digits[0],digits[1],digits[2],digits[3],digits[4],digits[5])
            elif obj["__typename"] == "Venue" and key == "dates":
                for date_url in info[key]:
                    venue_add_date_url(obj,date_url["name"],date_url["url"])

            else:
                if key == "authors" or key == "venues" or key == "presenters":
                    obj[key] = info[key]
                    for author_org in obj[key]:
                        for k in ["author","presenter"]:
                            if k in author_org:
                                id_ = author_org[k]
                                author = object_lookup_id(id_)
                                if "name" not in author:
                                    author["name"] = id_
                                author_org[k] = author["id"]
                        if "venue" in author_org:
                            venue = object_lookup_id(author_org["venue"])
                            venue["_name"] = author_org["venue"]
                            if "date" in author_org:
                                date = author_org["date"]
                                if "url" in author_org:
                                    url = author_org["url"]
                                else:
                                    url = ""
                                venue_add_date_url(venue,date,url)
                            author_org["venue"] = venue["id"]
                else:
                    obj[key] = tag_convert(info[key])
                           

    if "tags" in info:
        tags = [None] * len(info["tags"])
        for i,tag in enumerate(info["tags"]):
            tags[i] = object_lookup_type_name("tag",tag)["id"]
            link = { "to":tags[i]}
            link_lookup(obj["id"],link)
        obj["tags"] = tags


    if "links" in info:
        for link in info["links"]:
            link_lookup(obj["id"],link)

    return obj

def venue_add_date_url(venue, date, url):
    if "dates" not in venue:
        venue["dates"] = []
    found = False
    for date_url in venue["dates"]:
        if date_url["name"] == date:
            found = True
    if not found:
        venue["dates"].append({"name":date,"url":url})

def tag_convert(obj,padding=""):
    type_ = type(obj)
    #print (len(padding),padding,obj)
    if type_ == dict:
        for key,value in obj.items():
            if "tags" == key and type(value) == list:
                for i,tag in enumerate(obj["tags"]):
                    obj["tags"][i] = object_lookup_type_name("tag",tag)["id"]
            else:
                obj[key] = tag_convert(key,padding + " ")

    elif type_ == list:
        for i,value in enumerate(obj):
            obj[i] = tag_convert(value,padding + " ")
    #print (len(padding),padding,obj)

    return obj

def link_lookup(id_, info):
    id_ = id_.lower()
    if type(info) == str:
        info = { "to":info }
    info["from"] = id_
    if type(info["to"]) == str:
        obj = object_lookup_id(info["to"])
    else:
        obj = object_lookup(info["to"])
    info["to"] = obj["id"]

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

#############################

def solutions_process(path):
    solutions_dir = set()
    skipped = []
    for root, dirs, files in os.walk(path):
        if root == path:
            for fname in dirs:
                solutions_dir.add(root+"/"+fname)
        else:
            for fname in files:
                if root in solutions_dir and re_readme_md.search(fname):
                    p = root +"/"+fname
                    info = None
                    with open(p) as f:
                        inside = False
                        data = None
                        for line in f:
                            #print (line.rstrip())
                            if info is not None:
                                info["context"] += line
                            elif re.search("~~~",line):
                                if inside:
                                    if data == "":
                                        break
                                    try:
                                        info = json.loads(data)
                                    except Exception as e:
                                        print (p)
                                        print (data)
                                        raise e
                                    info["context"] = ""
                                    data = None
                                else:
                                    data = ""
                                inside = not inside
                            elif data is not None:
                                data += line
                    errors = []
                    if info is None:
                        info = {}
                    if "visibility" not in info or "public" != info["visibility"].lower():
                        errors.append("invisible")
                    if "id" not in info:
                        errors.append("no id")

                    if len(errors) > 0:
                        skipped.append([",".join(errors), p])
                    else:
                        info["__typename"] = "solution"
                        object_lookup(info)     
    if len(skipped) > 0:
        print ("skipped")
        for msg, p in skipped:
            print ("    ",msg,p)


#############################

def author_checker(author):
    if "nameFirst" not in author or "nameLast" not in author:
        if "name" in author:
            name = author["name"]
        else:
            name = author["id"]
        name = re.sub("[^:]:","",name)
        print (name)
        name_last, name_first = name.split("_")
        author["nameFirst"] = name_first
        author["nameLast"] = name_last
    return None

def object_checker(obj):
    if "name" not in obj:
        values = obj["id"].split(":")
        print ("creating name for",obj["id"])
        obj["name"] = ":".join(values[1:]).replace("_"," ")

    for key in ["tags","links","urls"]:
        if key not in obj:
            obj[key] = []

    return None

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
                if word in word_freq:
                    word_freq[word] += 1/total
                else:
                    word_freq[word] = 1/total

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

main()

