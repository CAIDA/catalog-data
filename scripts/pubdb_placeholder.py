#! /usr/bin/env python3
import json
import re
import os

re_id_illegal = re.compile("[^a-z^\d^A-Z]+")

def main():
    #process("media","../catalog-tools/data/in/PANDA-Presentations-json.pl.json")
    process("paper","../catalog-tools/data/in/PANDA-Papers-json.pl.json")

def process(type_,filename):
    objects = json.load(open(filename,"r"))
    for obj in objects:
        obj["placeholder"] = True
        for key in ["pubdb_presentation_id"]:
            if key in obj:
                obj["pubdb_id"] = obj[key]
                del obj[key]
        obj["resources"] = []
        links = []
        if "presenters" in obj:
            for p in obj["presenters"]:
                p["person"] = id_create("person",p["name"])
                del p["name"]
                p["organizations"] = p["organization"]
                del p["organization"]
                if p["url"] == "":
                    p["url"] = None
        if "authors" in obj:
            for a in obj["authors"]:
                a["organizations"] = a["organization"]
                del a["organization"]

        for link in obj["links"]:
            m = re.search("https://www.caida.org/publications/([^\/]+)/(\d\d\d\d)/([^/]+)",link["to"])
            if m:
                types, date,name = m.groups()
                if types == "papers":
                    t = "paper"
                elif types == "presentations":
                    t = "media"
                else:
                    t = None

                if t is not None:
                    links.append({
                        "to":id_create(t,date+"_"+name),
                        "label":link["label"]
                    })
                else:
                    print ("unknown type:",link["to"])
            else:
                resource = {
                    "name":link["label"],
                    "url":link["to"]
                }
                if link["label"] == "PDF":
                    link["tags"] = ["tag"]
                    link["format"] = "PDF"
                obj["resources"].append(resource)

        obj["links"] = links
        original = "sources/"+type_+"/"+obj["id"]+".json"
        filename = "sources/"+type_+"/"+obj["id"]+"__placeholder.json"
        if not os.path.exists(original):
            #print (json.dumps(obj,indent=4))
            json.dump(obj,open(filename,"w"),indent=4)
            pass
        else:
            print (filename)

def id_create(type_,name,id_=None):
    if id_ is not None:
        m = re_type_name.search(id_)
        if m:
            type_,name = m.groups()
        elif type_ is not None:
            name = id_
        else:
            print ("type not defined for",id)
            sys.exit()
    id_ = type_+":"+re_id_illegal.sub("_",name)
    return id_.lower()
    
main()
