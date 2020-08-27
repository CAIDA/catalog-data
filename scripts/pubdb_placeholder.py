#! /usr/bin/env python3
__author__ = "Bradley Huffaker"
__email__ = "<bradley@caida.org>"
import json
import re
import os
import sys
import lib.utils as utils

objects = []
seen = set()
name_id = {}

id_person = {}

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
                        raise e
                    id_ = id_add(fname, type_, obj["id"])
                    if type_ == "person" and "names" in obj:
                        obj["filename"] = fname
                        for n in obj["names"]:
                            id_alias = utils.id_create(fname,'person',
                                n["nameLast"]+"__"+n["nameFirst"])
                            id_person[id_alias] = obj

                    if "name" in obj:
                        name = utils.id_create(fname, type_,obj["name"])
                        #if "evolution" in name:
                            #print (obj["id"])
                            #print (name)
                            #print ()
                        id_ = name_id[name] = utils.id_create(fname, type_,obj["id"])
        
    for obj in objects:
        #print (json.dumps(obj, indent=4))
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
                        person_create(obj["id"],info["person"])
                        if key != "person":
                            del info[key]
                if "date" in info and re.search("\d\d\d\d\.\d",info["date"]):
                    year,mon = info["date"].split(".")
                    if len(mon) < 2:
                        mon = "0"+mon
                    info["date"] = year+"."+mon
                    if "date" not in obj or obj["date"] < info["date"]:
                        obj["date"] = info["date"]
        if "authors" in obj:
            for info in obj["authors"]:
                key_to_key(info,"organization","organizations")

        found = False

        if "links" in obj:
            url_base = None
            if obj["__typename"] == "paper":
                url_base = "https://www.caida.org/publications/papers/"+obj["datePublished"][:4]+"/"+obj["id"][5:]
            #for link in obj["links"]:
                #m = re.search("(.+)/[^\/]+.pdf$",link["to"])
                #if link["label"] == "PDF" and m:
                    #url_base = m.groups()[0]

            links = []
            for link in obj["links"]:
                m = re.search("https://www.caida.org/publications/([^\/]+)/(\d\d\d\d)\/([^/]+)/$",link["to"])
                if m:
                    type_,date, id_ = m.groups()
                    if type_ == "papers":
                        type_ = "paper"
                    elif type_ == "presentations":
                        type_ = "media"
                    id_ = utils.id_create(obj["filename"],type_,date+"_"+id_)
                    if id_ in seen:
                        links.append({
                            "to":id_,
                            "url":link["to"]
                        })
                else:
                    url = link["to"]
                    if url[0] == "/":
                        url = "https://www.caida.org"+url
                    elif url[:4] != "http" and url[:6] != "mailto":

                        if url_base: 
                            url = url_base+"/"+url
                        else:
                            print ("found:",url)
                            found = True
                    obj["resources"].append({
                        "name":link["label"],
                        "url":link["to"],
                        "tags":[]
                    })
            obj["links"] = links
        if found:
            print (json.dumps(obj, indent=4))

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


        filename = obj["filename"].replace("__pubdb","")
        if not os.path.exists(filename):
            json.dump(obj,open(obj["filename"],"w"),indent=4)

    for obj in id_person.values():
        filename = obj["filename"].replace("__pubdb","")
        if not os.path.exists(filename):
            json.dump(obj,open(obj["filename"],"w"),indent=4)


def key_to_key(obj,key_a,key_b):
    if key_a in obj:
        obj[key_b] = obj[key_a]
        del obj[key_a]

def load_ids(type_,filename):
    try:
        for obj in json.load(open(filename,"r")):
            obj["__typename"] = type_
            id_add(filename, type_, obj["id"])
            original = "sources/"+type_+"/"+obj["id"]+".json"
            if not os.path.exists(original):
                obj["filename"] = "sources/"+type_+"/"+obj["id"]+"__pubdb.json"
                objects.append(obj)
    except ValueError as e:
        print ("JSON error in",filename)
        raise e


def id_add(filename, type_,id_):
    id_ = utils.id_create(filename, type_,id_)
    yearless = id_yearless(id_)
    name_id[yearless] = id_
    seen.add(id_)
    return id_

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
    

def person_create(filename, obj):
    id_ = utils.id_create("filename",'person',obj)
    if id_ not in id_person:
        if obj[:7] == "person:":
            nameLast,nameFirst = obj[7:].split("__")
        else:
            nameLast,nameFirst = obj.split("__")
        person = {
            "id": id_,
            "__typename":"person",
            "filename":"sources/person/"+id_[7:]+"__pubdb.json", "nameLast": nameLast.replace("_"," ").title(), "nameFirst": nameFirst.replace("_"," ").title()
        }
        id_person[id_] = person
main()
