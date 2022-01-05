#! /usr/bin/env python3
__author__ = "Bradley Huffaker"
__email__ = "<bradley@caida.org>"
import json
import re
import os
import sys
import argparse
import lib.utils as utils

objects = []
seen = set()
name_id = {}

re_ids_only = re.compile("^[a-z_\s:\d]+$")
re_whitespace = re.compile("\s+")

parser = argparse.ArgumentParser()
parser.add_argument("-p", dest="papers_file", type=str, required=True)
parser.add_argument("-m", dest="media_file", type=str, required=True)
args = parser.parse_args()

def main():
    load_ids("paper","papers",args.papers_file)
    load_ids("media","presentations",args.media_file)
    error = False
    for type_ in os.listdir("sources"):
        p = "sources/"+type_
        if os.path.isdir(p):
            for fname in os.listdir(p):
                fname = p+"/"+fname
                if re.search("json$",fname) and "___pubdb" not in fname: 
                    try:
                        obj = json.load(open(fname,"r"))
                    except json.decoder.JSONDecodeError as e:
                        error = True
                        print ("error",fname, e)
                        continue
                    except ValueError as e:
                        print ("-----------\nJSON ERROR in ",fname,"\n")
                        raise e
                    id_add(fname, type_, obj["id"])
                    if "name" in obj:
                        name = utils.id_create(fname, type_,obj["name"])
                        #if "evolution" in name:
                            #print (obj["id"])
                            #print (name)
                            #print ()
                        name_id[name] = utils.id_create(fname, type_,obj["id"])
                    if type_ == "person":
                        utils.person_seen_add(fname, obj)
        
    if error:
        sys.exit(1)

    re_best = re.compile("Best\s*Paper")#, re.IGNORECASE)
    re_distinguished = re.compile("Distinguished\s*Paper")#, re.IGNORECASE)
    print ("processing objects")
    for obj in objects:
        obj["tags"].append("caida")
        if "annotation" in obj and (re_best.search(obj["annotation"]) or re_distinguished.search(obj["annotation"])):
            obj["tags"].append("best paper")

        key_to_key(obj,"pubdb_presentation_id","pubdb_id")
        key_to_key(obj,"venue","publisher")
        resources_front = []
        resources_back = []
        if "presenters" in obj:
            obj["type"] = "PRESENTATION"
            for info in obj["presenters"]:
                key_to_key(info,"name","person")
                key_to_key(info,"organization","organizations")
                for key in ["name","person"]:
                    if key in info:
                        info["person"] = "person:"+info[key]
                        person_create(obj["id"],info["person"])
                        if key != "person":
                            del info[key]
                if "date" in info:
                    date = utils.date_parse(info["date"])
                    if date is not None:
                        info["date"] = date
                        if "date" not in obj or obj["date"] < info["date"]:
                            obj["date"] = info["date"]
        if "authors" in obj:
            for info in obj["authors"]:
                key_to_key(info,"organization","organizations")
        
        if "links" in obj:
            links = []
            for link in obj["links"]:
                if link["label"] == "DOI":
                    obj["doi"] = link["to"]
                   
                m = re.search("https://www.caida.org/publications/([^\/]+)/(\d\d\d\d)\/([^/]+)/$",link["to"])
                id_ = None
                if m:
                    type_,date, id_ = m.groups()
                    if type_ == "papers":
                        type_ = "paper"
                    elif type_ == "presentations":
                        type_ = "media"

                m = re.search("https://catalog.caida.org/details/([^\/]+)/([^/]+)",link["to"])
                if m:
                    type_,id_ = m.groups()
                    id_ = utils.id_create(obj["filename"],type_,id_)


                if id_ is not None and id_ in seen:
                        links.append({
                            "to":id_,
                            "label":link["label"]
                        })
                else:
                    if "label" in link and (
                            re.search("^PDF$", link["label"], re.IGNORECASE)
                            or 
                            re.search("^HTML$", link["label"], re.IGNORECASE)):
                        if "access" not in obj:
                            obj["access"] = []
                        obj["access"].append({
                            "access":"public",
                            "url":link["to"],
                            "tags":link["label"]
                        })
                    resource = {
                        "name":link["label"],
                        "url":link["to"],
                        "tags":[]
                    }
                    if re.search("^pdf$", resource["name"], re.IGNORECASE):
                        resources_front.append(resource)
                    else:
                        resources_back.append(resource)
            obj["links"] = links
        if obj["__typename"] == "paper":
            obj["bibtexFields"] =  {}
            for key_from in ["type", "booktitle","institution","journal","volume","publisher","venue","pages","peerReviewedYes","bibtex","year","mon"]:
                if key_from in obj and len(obj[key_from]) > 0:
                    if key_from == "booktitle":
                        key_to = "bookTitle"
                    else:
                        key_to = key_from

                    obj["bibtexFields"][key_to] = obj[key_from]
                    if key_from != "publisher":
                        del obj[key_from]

            resources_front.append({
                "name":"bibtex",
                "url":"https://www.caida.org/publications/papers/"+obj["id"][:4]+"/"+obj["id"][5:]+"/bibtex.html"
                })
        resources_front.extend(resources_back);
        obj["resources"] = resources_front

        if "datePublished" in obj:
            obj["date"] = utils.date_parse(obj["datePublished"])

        if "linkedObjects" in obj and len(obj["linkedObjects"]) > 0:
            linked = obj["linkedObjects"].lower().strip()
            if re_ids_only.search(linked):
                for to_id in re_whitespace.split(linked):
                    obj["links"].append(to_id)
            else:
                print (obj["id"], "failed to parse linkedObject `"+linked+"'")



        json.dump(obj,open(obj["filename"],"w"),indent=4)


    for obj in id_person.values():
        if "already_exists" not in obj:
            json.dump(obj,open(obj["filename"],"w"),indent=4)


def key_to_key(obj,key_a,key_b):
    if key_a in obj:
        obj[key_b] = obj[key_a]
        del obj[key_a]

def load_ids(type_,key, filename):
    print ("loading", key, filename)
    try:
        data = json.load(open(filename,"r"))
        if key not in data:
            print ("   JSON file needs to contain an array of",key)
            sys.exit(-1)

        for obj in data[key]:
            obj["__typename"] = type_
            id_add(filename, type_, obj["id"])
            original = "sources/"+type_+"/"+obj["id"]+".json"
            if not os.path.exists(original):
                obj["filename"] = "sources/"+type_+"/"+obj["id"]+"___pubdb.json"
                objects.append(obj)
    except json.decoder.JSONDecodeError as e:
        print ("error",filename, e)
    except ValueError as e:
        print ("JSON error in",filename)
        raise e


def id_add(filename, type_,id_):
    id_ = utils.id_create(filename, type_,id_)
    yearless = id_yearless(id_)
    name_id[yearless] = id_
    seen.add(id_)

def id_lookup(id_):
    if id_ in seen:
        return id_

    yearless = id_yearless(id_)
    if yearless in name_id:
        return name_id[yearless]

    return None

def id_yearless(id_):
    m = re.search("(.+):(\d\d\d\d)_(.+)",id_)
    if m:
        type_,date,name = m.groups()
        return type_+":"+name
    return id_
    

id_person = {}
def person_create(filename, obj):
    if obj[:7] == "person:":
        nameLast,nameFirst = obj[7:].split("__")
    else:
        nameLast,nameFirst = obj.split("__")
    person = utils.person_seen_check(nameLast,nameFirst)
    if person is None:
        id_ = utils.id_create("filename",'person',obj)
        if id_ not in id_person:
            person = {
                "id": id_,
                "__typename":"person",
                "filename":"sources/person/"+id_[7:]+"__pubdb.json", "nameLast": nameLast.replace("_"," ").title(), "nameFirst": nameFirst.replace("_"," ").title()
            }
            id_person[id_] = person
    elif person["id"] not in id_person:
        person["already_exists"] = True
        id_person[person["id"]] = person
main()
