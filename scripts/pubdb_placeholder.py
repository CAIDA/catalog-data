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
    
error = False

def main():
    if not load_ids("paper","papers",args.papers_file)  \
        or not load_ids("presentation","presentations",args.media_file):
        utils.error_print()
        sys.exit(1)

    ## load all existing ids 
    ## parameters: sources, and the type that is calling it
    # utils.id_check_load("sources", "pubdb")

    ## Add this to utils as id_check_load()
    for type_ in os.listdir("sources"):
        p = "sources/"+type_
        if os.path.isdir(p):
            for fname in os.listdir(p):
                fname = p+"/"+fname
                if re.search("json$",fname) and "___pubdb" not in fname: 
                    try:
                        obj = json.load(open(fname,"r"))
                    except json.decoder.JSONDecodeError as e:
                        error_add(fname, e)
                        continue
                    except ValueError as e:
                        print ("-----------\nJSON ERROR in ",fname,"\n")
                        raise e
                    if "id" not in obj:
                        error_add(fname,'no id for "{'+obj['name']+'"')
                        continue 
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
        utils.error_print()
        sys.exit(1)
    ## add to this end 

    re_best = re.compile("Best\s*Paper")#, re.IGNORECASE)
    re_distinguished = re.compile("Distinguished\s*Paper")#, re.IGNORECASE)
    print ("processing objects")
    for obj in objects:
        obj["tags"].append("caida")
        if "annotation" in obj and (re_best.search(obj["annotation"]) or re_distinguished.search(obj["annotation"])):
            obj["tags"].append("best paper")

        key_to_key(obj,"pubdb_presentation_id","pubdb_id")
        key_to_key(obj,"venue","publisher")
        if "presenters" in obj:
            for info in obj["presenters"]:
                key_to_key(info,"name","person")
                key_to_key(info,"organization","organizations")
                for key in ["name","person"]:
                    if key in info:                        
                        info['person'] = person_create(obj["filename"],info["person"])
                if "date" in info:
                    date = utils.date_parse(info["date"])
                    if date is not None:
                        info["date"] = date
                        if "date" not in obj or obj["date"] < info["date"]:
                            obj["date"] = info["date"]
        if "authors" in obj:
            for info in obj["authors"]:
                key_to_key(info,"organization","organizations")
                info['person'] = person_create(obj["filename"], info["person"])
        
        links = []
        if "fundingSources" in obj:
            for tag in obj["fundingSources"]:
                obj["tags"].append("funding:"+tag)

        if "links" in obj:
            access = []
            for link in obj["links"]:
                if link["label"] == "DOI":
                    obj["doi"] = link["to"]
                    continue
                   
                id_ = None
                m = re.search("https://www.caida.org/publications/([^\/]+)/(\d\d\d\d)\/([^/]+)/$",
                        link["to"])
                if m:
                    type_,date, id_ = m.groups()
                    if type_ == "papers":
                        type_ = "paper"
                    elif type_ == "presentations":
                        type_ = "presentation"
                else:
                    for regex in [re.compile("https://catalog.caida.org/details/([^\/]+)/([^/]+)"),
                        re.compile("https://catalog.caida.org/([^\/]+)/([^/]+)")]:
                        m = regex.search(link["to"])
                        if m:
                            type_,id_ = m.groups()
                            break

                if id_ is not None:# and id_ in seen:
                    if type_ == "media":
                        type_ = "presentation"
                    links.append({
                        "to":type_+":"+id_,
                        "label":link["label"]
                    })

                else:
                    if "access" not in obj:
                        obj["access"] = []
                    access.append({
                        "access":"public",
                        "url":link["to"],
                        # "tags":[link["label"]],
                        "type": link["label"]
                    })
            del obj["links"]

            if len(access) > 0:
                obj["access"] = access

        if "datePublished" in obj:
            obj["date"] = utils.date_parse(obj["datePublished"])

        if "linkedObjects" in obj and len(obj["linkedObjects"]) > 0:
            linked = obj["linkedObjects"].lower().strip()
            if re_ids_only.search(linked):
                for to_id in re_whitespace.split(linked):
                    links.append(to_id)
            else:
                print (obj["id"], "failed to parse linkedObject `"+linked+"'")

        if len(links) > 0:
            obj["links"] = links

    if error:
        utils.error_print()
        sys.exit(1)

    # fix links
    ids = set()
    for obj in objects:
        ids.add(obj["id"])
        if "links" in obj and len(obj["links"]) > 0:
            for index, id_ in enumerate(obj["links"]):
                if "media" in id_ and id_ not in ["media:2014_a_coordinated_view_of_the_egypt_internet_blackout_2011","media:2020_dynamips_conext_video"]:
                    obj["links"][index] = "presentation:"+id_[6:]

                if id_ == "dataset:routeviews_ipv4_prefix2as" or id_ == "dataset:routeviews_ipv6_prefix2as":
                    obj["links"][index] = "dataset:routeviews_prefix2as"

    # Dump objects
    for obj in id_person.values():
        if "already_exists" not in obj:
            json.dump(obj,open(obj["outfile"],"w"),indent=4)

    # print objects
    for obj in objects:
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
        error_add(filename, e)
        return False 
    except ValueError as e:
        error_add(filename, "invalid JSON format")
        return False 
        raise e
    return True


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

def error_add(filename, message):
    global error
    utils.error_add(filename,message)
    error = True
    

id_person = {}
def person_create(filename, pid):
    if pid[:7] == "person:":
        nameLast,nameFirst = pid[7:].split("__")
    else:
        nameLast,nameFirst = pid.split("__")
    person = utils.person_seen_check(nameLast,nameFirst)
    if person is None:
        id_ = utils.id_create(filename,'person',pid)
        if id_ not in id_person:
            person = {
                "id": id_,
                "__typename":"person",
                "filename":filename,
                "outfile":"sources/person/"+id_[7:]+"___pubdb.json", 
                "nameLast": nameLast.replace("_"," ").title(),
                "nameFirst": nameFirst.replace("_"," ").title()
            }
            id_person[id_] = person
        else:
            person = id_person[id_]
    elif person["id"] not in id_person:
        person["already_exists"] = True
        id_person[person["id"]] = person
    
    return person["id"]

main()
