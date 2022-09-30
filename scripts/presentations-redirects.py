#!  /usr/bin/env python3
import os
import json

for d in ["sources/presentation"]:
    print (d)
    for f in os.listdir(d):
        if f != "hidden.json":
            with open(d+"/"+f) as fin:
                id_ = json.load(fin)["id"]
                print (", ".join(["media:"+id_,"presentation:"+id_, "", "true"]))
