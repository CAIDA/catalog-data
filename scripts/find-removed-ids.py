#!/usr/bin/env python3

# imports
import requests

ids_current = set()
query = """{
  search {
    edges {
       node {
          id   
       }
    }
  }
}"""
request = requests.post("https://api.catalog.caida.org/", json={'query': query})
if request.status_code == 200:
    response = request.json()

for nodes in response["data"]["search"]["edges"]:
    ids_current.add(nodes["node"]["id"]);

for id in ids_current:
    print(id)