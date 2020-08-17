#!  /usr/bin/env python3
import json
import sys
import lib.utils as utils
import subprocess

for fname in sys.argv[1:]:
    person = json.load(open(fname,"r"))
    if "nameFirst" not in person or "nameLast" not in person:
        if "person:" in person["id"][:7]:
            names = person["id"][7:].split("_")
        else:
            names = person["id"].split("_")
        person["nameLast"] = names[0].title()
        person["nameFirst"] = " ".join(names[1:]).title()
        person["name"] = person["nameLast"]+", "+person["nameFirst"]
    if "organizaion" in person:
        person["organizations"] = person["organization"]
        del person["organization"]
    person["id"] = utils.id_create(fname,"person",person["nameLast"]+"__"+person["nameFirst"])
    filename = person["id"][7:]+".json"
    subprocess.run(["git","mv",fname,filename])
    json.dump(person,open(filename,"w"),indent=4)
    
