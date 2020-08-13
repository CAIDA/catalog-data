#! /usr/bin/env python3
import json
import re
import os
import sys

re_id_illegal = re.compile("[^a-z^\d^A-Z]+")
objects = []
seen = set()
name_id = {}

def main():
    load_ids("media","data/PANDA-Presentations-json.pl.json")
    load_ids("paper","data/PANDA-Papers-json.pl.json")
    for type_ in os.listdir("sources"):
        p = "sources/"+type_
        if os.path.isdir(p):
            for fname in os.listdir(p):
                fname = p+"/"+fname
                if re.search("json$",fname): 
                    try:
                        obj = json.load(open(fname,"r"))
                    except ValueError as e:
                        print (fname)
                        raise e
                    id_add(fname, type_, obj["id"])
                    if "name" in obj:
                        name = id_create(fname, type_,obj["name"])
                        #if "evolution" in name:
                            #print (obj["id"])
                            #print (name)
                            #print ()
                        name_id[name] = id_create(fname, type_,obj["id"])
        
    for obj in objects:
        #print (obj["__typename"], obj["id"])
        key_to_key(obj,"pubdb_presentation_id","pubdb_id")
        key_to_key(obj,"venue","publisher")
        obj["resources"] = []
        if "presenters" in obj:
            obj["type"] = "PRESENTATION"
            for info in obj["presenters"]:
                key_to_key(info,"name","person")
                key_to_key(info,"organization","organizations")
                for key in ["name","person"]:
                    if key in info:
                        info["person"] = "person:"+info[key]
                        if key != "person":
                            del info[key]
                if "date" in info and re.search("\d\d\d\d\.\d",info["date"]):
                    year,mon = info["date"].split(".")
                    if len(mon) < 2:
                        mon = "0"+mon
                    info["date"] = year+"."+mon
        if "authors" in obj:
            for info in obj["authors"]:
                key_to_key(info,"organization","organizations")

        if "links" in obj:
            links = []
            for link in obj["links"]:
                m = re.search("https://www.caida.org/publications/([^\/]+)/(\d\d\d\d)\/([^/]+)/$",link["to"])
                if m:
                    type_,date, id_ = m.groups()
                    if type_ == "papers":
                        type_ = "paper"
                    elif type_ == "presentations":
                        type_ = "media"
                    id_ = id_create(obj["filename"],type_,date+"_"+id_)
                    if id_ in seen:
                        links.append({
                            "to":id_,
                            "url":link["to"]
                        })
                else:
                    obj["resources"].append({
                        "name":link["label"],
                        "url":link["to"],
                        "tags":[]
                    })
            obj["links"] = links
        if obj["__typename"] == "paper":
            obj["bibtexFields"] =  {}
            for key_from in ["type", "booktitle","institution","journal","volume","venue","pages","peerReviewedYes","bibtex","year","mon"]:
                if key_from in obj and len(obj[key_from]) > 0:
                    if key_from == "booktitle":
                        key_to = "bookTitle"
                    else:
                        key_to = key_from

                    obj["bibtexFields"][key_to] = obj[key_from]
                    del obj[key_from]

        if "datePublished" in obj:
            year,mon = obj["datePublished"].split(".")
            if len(mon) < 2:
                mon = "0"+mon
            obj["date"] = obj["datePublished"] = year+"."+mon


        #print (obj["filename"])
        json.dump(obj,open(obj["filename"],"w"),indent=4)
        #print (json.dumps(obj,indent=4))

def key_to_key(obj,key_a,key_b):
    if key_a in obj:
        obj[key_b] = obj[key_a]
        del obj[key_a]

def load_ids(type_,filename):
    for obj in json.load(open(filename,"r")):
        obj["__typename"] = type_
        id_add(filename, type_, obj["id"])
        original = "sources/"+type_+"/"+obj["id"]+".json"
        if not os.path.exists(original):
            obj["filename"] = "sources/"+type_+"/"+obj["id"]+"__pubdb.json"
            objects.append(obj)


def id_add(filename, type_,id_):
    id_ = id_create(filename, type_,id_)
    yearless = id_yearless(id_)
    name_id[yearless] = id_
    seen.add(id_)

def id_create(filename, type_,id_):
    if id_ is not None:
        if ":" in id_:
            values = id_.split(":")
            type_ = values[0]
            name = "_".join(values[1:])
        elif type_ is not None:
            name = id_
        else:
            print (filename, "type not defined for",id)
            sys.exit()
    else:
        print (filename, "id not defined")
        sys.exit()
    if type_ == "presentation":
        type_ = "media"
      
    name = re_id_illegal.sub("_",name)
    name = re.sub("_+$","",re.sub("^_+","",name))
    id_ = type_+":"+name
    return id_.lower()

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
    
main()
