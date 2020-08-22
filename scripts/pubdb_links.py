#! /usr/bin/env python3
__author__ = "Bradley Huffaker"
__email__ = "<bradley@caida.org>"
from bs4 import BeautifulSoup
import json
import re
import os
import sys
import subprocess
import lib.utils as utils
import urllib.request, urllib.error
import traceback

url_id = {
    "www.caida.org/data/active/ipv4_prefix_probing_dataset.xml":"dataset:ipv4_routed_24_topology_dataset",
    "www.caida.org/data/as-or":"dataset:as_organization",
    "www.caida.org/data/as-relatio":"dataset:as_relationships",
    "www.caida.org/data/active/as-relationships":"datasetas_relationships"
}

invalid_id = set([
    "dataset:overview",
    "dataset:passive"
    ])

pubdb_links_file = "data/pubdb_links.json"

def url_cleaner(url):
    return re.sub("https?://", "", re.sub("[/,\.\)]+$","",url))

def main():
    for type_ in os.listdir("sources"):
        p = "sources/"+type_
        if os.path.isdir(p):
            for fname in os.listdir(p):
                fname = p+"/"+fname
                if re.search("json$",fname) and "__" not in fname: 
                    try:
                        obj = json.load(open(fname,"r"))
                        id_ = utils.id_create(fname, type_,obj["id"])
                        if "resources" in obj:
                            for resource in obj["resources"]:
                                if "url" in resource and len(resource["url"]) > 10:
                                    url = url_cleaner(resource["url"])
                                    print (url)
                                    url_id[url] = id_
                    except ValueError as e:
                        print (fname)
                        raise e
                        #if "evolution" in name:
                            #print (obj["id"])
                            #print (name)
                            #print ()
                        name_id[name] = utils.id_create(fname, type_,obj["id"])
    print ()
    seen = set()
    links = []
    for type_,filename in [["media","data/PANDA-Presentations-json.pl.json"], 
        ["paper","data/PANDA-Papers-json.pl.json"]]:
        for obj in json.load(open(filename,"r")):
            id_ = utils.id_create(filename, type_, obj["id"])
            failed = None
            if "links" in obj:
                for link in obj["links"]:
                    if "to" in link:
                        m = re.search("(\d\d\d\d/[^\/]+/[^/]+.pdf$)",link["to"])
                        if m:
                            fname = "data/files/"+m.group(1)
                            found = None
                            if os.path.exists(fname):
                                found = fname
                            else:
                                fname = "data/presentations/"+m.group(1)
                                if os.path.exists(fname):
                                    found = fname
                            if found:
                                fname_txt = re.sub("pdf","txt",fname)
                                if not os.path.exists(fname_txt):
                                    subprocess.run(["pdftotext",found])
                                with open(fname_txt,"r") as f:
                                    for line in f:
                                        m = re.search("(http[^\s]+)",line)
                                        if m:
                                            url = url_cleaner(m.group(1))
                                            if url in url_id:
                                                link = [id_,url_id[url]]
                                                l = json.dumps(link)
                                                if l not in seen:
                                                    links.append(link)
                                                    seen.add(l)
                                            else:
                                                m = re.search("www.caida.org/data/([^/]+)",url)
                                                if m: 
                                                    i = utils.id_create("","dataset",m.group(1)) 
                                                    #if i not in invalid_id:
                                                        #print ("    ",url,"            ",id_, "     ",i)
                                                        #print (i)
                                                        #filename = "data/www_caida_org/"+re.sub("[^a-z]+","_",url)+".html"
                                                        #print (filename, m.group(1))
                                                        #if not os.path.exists(filename):
                                                            #download("http://"+url,filename)
                                                        #sys.exit()
                            else:
                                failed = fname
            #if failed is not None:
                #print (id_,failed)

    with open(pubdb_links_file,"w") as f:
        print ("writing",pubdb_links_file)
        json.dump(links,f,indent=4)


def download(url, filename):
    print ("downloading",url)
    try:
        response = urllib.request.urlopen(url, timeout=5)
        html = response.read()
        with open(filename,"wb") as f:
            f.write(html)
            f.close()
    except urllib.error.HTTPError as e:
        traceback.print_stack()
        print ('HTTPError = ' + str(e.code))
        with open(filename,"w") as f:
            f.close()
    except Exception:
        traceback.print_stack()
        print ('generic exception: ' + traceback.format_exc())
        sys.exit()


main()
