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
    if len(sys.argv) < 1:
        print ("Failed to any filenames")
        sys.exit()

    load_ids("media","data/PANDA-Presentations-json.pl.json")
    load_ids("paper","data/PANDA-Papers-json.pl.json")
    for type_ in os.listdir("sources"):
        #print ("loading",type_)
        path = "sources/"+type_
        if os.path.isdir(path):
            for filename in os.listdir(path):
                fname = path+"/"+filename
                if type_ == "solution":
                    if os.path.isdir(fname):
                        for solution in os.listdir(fname):
                            solution_path = fname+"/"+solution
                            if re.search("readme.md",solution_path,re.IGNORECASE):
                                info = solution_parse(solution_path)
                                if "id" in info:
                                    id_add(solution_path, "solution", info["id"])
                                else:
                                    id_add(solution_path, "solution", filename)
                elif re.search("json$",fname): 
                    obj = json.load(open(fname,"r"))
                    id_add(fname, type_, obj["id"])
                    if "name" in obj:
                        name = id_create(fname, type_,obj["name"])
                        #if "evolution" in name:
                            #print (obj["id"])
                            #print (name)
                            #print ()
                        name_id[name] = id_create(fname, type_,obj["id"])

    nothing_found = True

    for fname in sys.argv[1:]:
        if "sources/solution" in fname:
            info = solution_parse(fname)
        else:
            info = json.load(open(fname,"r"))
        missing = []
        changed = False
        if "links" in info:
            for i,link in enumerate(info["links"]):
                if type(link) == str:
                    to = link
                    changed = True
                    found = id_lookup(to)
                    if found is not None:
                        to = found
                    if to is not None:
                        info["links"][i] = {"to":to}
                        changed = True
                else:
                    #link["oo"] = link["to"]
                    to = id_create(fname, None,link["to"])
                    to = "solution:getting_an_asns_name_country_organization"
                    found = id_lookup(to)
                    if found is None:
                        missing.append(link["to"])
                    else:
                        to = found
                    if to is not None and to != link["to"]:
                        info["links"][i]["to"] = to
                        changed = True
        if "licenses" in info:
            for i,license in enumerate(info["licenses"]):
                l = id_create(fname, "license",license)
                found = id_lookup(l)
                if found is None:
                    missing.append(license)
                else:
                    l = found
                if l != info["licenses"]:
                    change = True


        if len(missing) > 0: 
            print (fname)
            for missed in missing:
                print ("    ",missed)
            nothing_found = False

        #if changed:
            #print ("updating",fname)
            #json.dump(info,open(fname,"w"),indent=4)
            #print (json.dumps(info,indent=4))

    if nothing_found:
        print ("no missing ids found")

def load_ids(type_,filename):
    #print ("loading",filename)
    for obj in json.load(open(filename,"r")):
        id_add(filename, type_, obj["id"])

def id_add(filename, type_,id_):
    id_ = id_create(filename, type_,id_)
    yearless = id_yearless(id_)
    name_id[yearless] = id_
    seen.add(id_)

def id_create(filename, type_,id_=None):
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

def solution_parse(fname): 
    with open(fname,"r") as f:
        data = None
        for line in f:
            if re.search("~~~",line):
                if data is None:
                    data = ""
                else:
                    break
            elif data is not None:
                data += line
        if data is not None:
            try: 
                info = json.loads(data)
            except ValueError as e:
                print ("parse failure",fname)
                print (e)
                info = {}
            return info
    return {}

main()
