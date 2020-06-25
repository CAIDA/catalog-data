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
    fname_type = {
        "Datasets.json":"dataset",
        "Licenses.json":"license",
        "Authors.json":"author",
        "Papers.json":"paper",
        "Presentations.json":"presentation",
        "Venues.json":"venue",
        "Softwares.json":"software"
    }
    for fname in os.listdir(source_dir):
        path = source_dir+"/"+fname
        if fname in fname_type:
            type_ = fname_type[fname]
            print ("loading",path)
            with open(path,"r") as f:
                for info in json.load(f):
                    info["__typename"] = type_
                    obj = object_lookup(info)
        elif fname == "Solutions":
            solutions_process(path)

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
                print (json.dumps(obj,indent=4))
                print (json.dumps(id_objs[id_],indent=4))

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
    id_ = type_+":"+re_id_illegal.sub("_",name)
    return object_lookup_id(id_)

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
    if "id" not in info:
        if "name" in info and "__typename" in info:
            id_ = info["__typename"]+":"+re_id_illegal.sub("_",info["name"])
            info["id"] = id_.lower()
        else:
            print ("no id or name,_typename",info)
            sys.exit()

    id_ = info["id"] = info["id"].lower()
    if id_ not in id_object:
        id_object[id_] = {"id":id_.lower(),"__typename":info["__typename"].capitalize()}
    obj  = id_object[id_]
    obj["__typename"] = info["__typename"].capitalize()

    object_types = set(["datasets","licenses","softwares","solutions","papers","publications"])
    for key in info.keys():
        if key == "links":
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
            else:
                obj[key] = info[key]
                if key == "authors" or key == "venues":
                    for author_org in info[key]:
                        for k in ["author","presenter"]:
                            if k in author_org:
                                id_ = author_org[k]
                                author = object_lookup_id(id_)
                                if "nameFirst" not in author and "name" not in author:
                                    author["name"] = id_
                        if "venue" in author_org:
                            object_lookup_id(author_org["venue"])
                           

    if "tags" in obj:
        for tag in obj["tags"]:
            link = { "to":object_lookup_type_name("tag",tag)["id"] }
            link_lookup(obj["id"],link)


    if "links" in info:
        for link in info["links"]:
            link_lookup(obj["id"],link)

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
    print ("path:",path)
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
        name_last, name_first = name.split(",_")
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


##########################################################################
##########################################################################


def papers_load(fname):
    print ("loading",fname)
    with open(fname,"r") as f:
        for paper in json.load(f):
            paper_update(paper["name"], paper)

def nodes_load(fname, func):
    print ("loading",fname)
    with open(fname,"r") as f:
        for node in json.load(f):
            name = None 
            if "name" in node:
                name = node["name"]
            func(name, node)

def lookup(types, type, name, source=None, skip=None):
    m = re.search("^"+type+":(.+)",name)
    if m:
        id = name
        name = m.group(1)
    else:
        id = type+":"+re_id_illegal.sub("_",name) # name.replace(" ","_").replace(":","_")
        id = id.lower().replace(" ","_")

    if types not in type_data:
        type_data[types] = {}
    if id not in type_data[types]:
        node = type_data["nodes"][id] = type_data[types][id] = {"id":id,"_type":type.capitalize()}
        node["name"] = name

    node = type_data[types][id]
    if source:
        for key,value in source.items():
            if (not skip or key not in skip):
                if key not in node:
                    node[key] = value
                else:
                    current = node[key]
                    if isinstance(current,list) and isinstance(value,list):
                        for v in value:
                            if v not in current:
                                current.append(v)
    if "tags" in node:
        tags = []
        for i,tag in enumerate(node["tags"]):
            if not re_tag.search(tag):
                if not re_only_white_space.search(tag):
                    tags.append(lookup("tags","tag",tag)["id"])
            else:
                tags.append(tag)
        node["tags"] = tags
    return node

def node_cleanup_duplicates(node):
    for key,value in node.items():
        if isinstance(value,list):
            clean = []
            for v in value:
                if v not in clean:
                    clean.append(v)
            node[key] = clean

def dataset_update(name, dataset_source):
    dataset = lookup("datasets","dataset",name,dataset_source)
    if "entities" in dataset:
        for i, entity in enumerate(dataset["entities"]):
            entity["datasets"] = [dataset["id"]]
            dataset["entities"][i] = entity_update(entity["name"], entity, dataset)["id"]
    if "joins" in dataset:
        for i,join in enumerate(dataset["joins"]):
            join["datasets"] = [dataset["id"]]
            dataset["joins"][i] = join_update(None, join)["id"]
    if "papers" in dataset:
        for i,name in enumerate(dataset["papers"]):
            paper = lookup("papers","paper",name)
            paper["datasets"] = [dataset["id"]]
    return dataset

def paper_update(name, paper_source):
    paper = lookup("papers","paper",name, paper_source)
    id = paper["id"]
    for key,func in [["datasets",dataset_update],["entities",entity_update],
            ["joins", join_update]]:
        if key in paper:
            array = [None] * len(paper[key])
            for i,name in enumerate(paper[key]):
                node = {"name":name,"papers":[id]}
                array[i] = func(name, node)["id"]
            paper[key] = array
    return paper

def entity_update(name, entity_source = None, dataset = None):
    entity = lookup("entities","entity",name,entity_source,["features"])
    entity["name"] = name
    if entity_source:
        for key in ["description"]:
            if key in entity_source and key not in entity:
                entity[key] = entity_source[key]
        if "features" in entity_source:
            if "features" not in entity:
                entity["features"] = []
            for f in entity_source["features"]:
                feature = f.copy()
                if dataset:
                    if "datasets" not in feature:
                        feature["datasets"] = []
                    feature["datasets"].append(dataset["id"])
                if "id" not in feature:
                    feature["id"] = ":".join(["feature",dataset["name"],entity["name"]])
                entity["features"].append(feature)
    return entity

def join_update(name, join_source):
    id = "+".join(sorted(join_source["entities"]))
    if not name:
        name = id
    #if "label" in join_source:
        #id += ":"+join_source["label"]
        #name += " "+join_source["label"]
    join_source["name"] = name
    join = lookup("joins","join",id,join_source)
    entityObjectIds = []
    for i,name in enumerate(join["entities"]):
        entity = {"joins":[join["id"]]}
        join["entities"][i] = entity_update(name,entity)["id"]
    #for entities in [join_source["entities"],reversed(join_source["entities"])]:
        #i = "join:"+"+".join(entities)
        #if i not in type_data["joins"]:
            #type_data["joins"][i] = join
    return join

def tag_update(name, tag_source = None):
    if name:
        m = re.search("tag:(.+)",name)
        if m:
            name = m.group(1)
            print ("   >",name)
    tag = lookup("tags","tag",name, tag_source)
    return tag

def selections_load(fname):
    print ("loading",fname)
    with open(fname,"r") as f:
        for selection in json.load(f):
            lookup("selections","selection",selection["name"],selection)

def selections_load_dir(dname):
    re_html = re.compile("\.html$", re.IGNORECASE)
    re_pre_start = re.compile("<pre>", re.IGNORECASE)
    re_pre_end = re.compile("</pre>", re.IGNORECASE)
    re_body = re.compile("</body>", re.IGNORECASE)
    print ("loading",dname)
    for fname in os.listdir(dname):
        path = dname+"/"+fname
        if re_html.search(fname):
            stage = "json_before"
            json_string = ""
            with open(path) as f:
                for line in f:
                    if re_body.search(line):
                        break
                    if stage == "json_before":
                        if re_pre_start.search(line):
                            stage = "json_in"
                    elif stage == "json_in":
                        if re_pre_end.search(line):
                            stage = "json_after"
                            selection = json.loads(json_string)
                            selection["description"] = ""
                        else:
                            json_string += line
                    else:
                        selection["description"] += line.rstrip()
    lookup("selections","selection",selection["name"],selection)


####################################


def id_word_score_get(type, id, seen):
    if id not in id_word_score:
        if id in seen:
            return None
        seen.add(id)
        if type in type_key_w_type_w:
            node = type_data[type][id]
            key_weights = type_key_w_type_w[type]["key_weights"]
            type_weights = type_key_w_type_w[type]["type_weights"]
            word_score = word_score_get(node, key_weights, type_weights, seen)

            # put in empty string for a search on nothing
            empty_string = ""
            if empty_string not in word_score:
                word_score[empty_string] = 1
            else:
                word_score[empty_string] += 1
        else:
            word_score = None
        id_word_score[id] = word_score
    return id_word_score[id]

def word_score_get(node,key_weights, type_weights, seen):
    word_score = {}
    for key,weight in key_weights:
        if key in node:
            words = re_not_word.split(re_html.sub("",node[key]))
            for word in words:
                word = word.lower()
                if word not in word_score:
                    word_score[word] = weight/len(words)
                else:
                    word_score[word] += weight/len(words)
    for type,weight in type_weights:
        if type in node:
            for id in node[type]:
                src = id_word_score_get(type, id, seen)
                if src:
                    for word,value in src.items():
                        if word not in word_score:
                            word_score[word] = value*weight
                        else:
                            word_score[word] += value*weight
    return word_score

def word_score_joins(join):
    word_score = {}
    add_word_score_children(word_score,join, [
        ["entities",.9],
        ["tags", .8]
        ])
    return word_score

################################################
def id_neighbors_print(fname):

    id_links = {}
    # Build up the links
    for node in type_data["nodes"].values():
        id = node["id"]
        for key,value in node.items():
            if type(value) == list:
                for i in value:
                    if type(i) == str and i in type_data["nodes"]:
                        add_link(id_links, id,i)
                        add_link(id_links, i,id)

    id_neighbors = {}
    for id,ids_set in id_links.items():
        id_neighbors[id] = list(ids_set)

    print("writing",fname)
    with open(fname,"w") as f:
        f.write(json.dumps(id_neighbors,indent=4, sort_keys=True))

#    for time in range(0,30):
#        for id,ids in id_links.items():
#            id_score = id_id_score[id] = {id:id_score_node_weight}
#            for i in ids:
#                if i in id_id_score:
##                    for j,score in id_id_score[i]:
##                        if j not in id_score:
##                            id_score[j] = score
#                        else:
#                            id_score[j] += score
#
#    for id,id_score in id_id_score.items():
#        id_scores = []
#        for id,score in id_score.items():
#            id_scores.append([id,score])
#        id_id_score[id] = sorted(id_scores,key=lambda k: k[1])
#
#    print("writing",fname)
#    with open(fname,"w") as f:
#        f.write(json.dumps(id_id_score,indent=4, sort_keys=True))

def add_link(id_links, i,j):
    if i not in id_links:
        id_links[i] = set()
    id_links[i].add(j)

main()

