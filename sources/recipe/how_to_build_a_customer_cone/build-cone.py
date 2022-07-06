#!/usr/bin/env python2

#import the low level _pybgpsteam library and other necessary libraries
from pybgpstream import BGPStream
from ipaddress import ip_network
import time
import sys
import requests

URL = "https://api.asrank.caida.org/v2/graphql"

def main():
    print ("This is going to take some time",file=sys.stderr)
    peer_provider = download_links()
    asn__cone = download_paths(peer_provider)
    for asn,cone in asn__cone.items():
        print (asn," ".join(cone))

def download_links():
    print ("Downloanding relationships",file=sys.stderr)
    first = 1000
    offset = 0
    hasNextPage = True

    peer_provider = set()
    with open("20220601.as-rel.txt") as fin:
        for line in fin:
            if len(line) == 0 or line[0] == "#":
                continue
            asn0, asn1, rel = line.rstrip().split("|")
            if rel == 0:
                peer_provider.add(asn1+" "+asn0)
                peer_provider.add(asn0+" "+asn1)

            elif rel == -1:
                peer_provider.add(asn1+" "+asn0)

            else:
                peer_provider.add(asn0+" "+asn1)

    return peer_provider

    while hasNextPage:
        query = AsnLinksQuery(first, offset, asns)
        request = requests.post(URL,json={'query':query})
        if request.status_code != 200:
            print ("Query failed to run returned code of %d " % (request.status_code))

        data = request.json()
        if not ("data" in data and "asnLinks" in data["data"]):
            print ("Failed to parse:",data,file=sys.stderr)
            sys.exit()

        peer_customer = set()
        data = data["data"]["asnLinks"]
        for edge in data["edges"]:
            asn0 = edge["node"]["asn0"]["asn"]
            asn1 = edge["node"]["asn1"]["asn"]
            rel = edge["node"]["asn1"]["relationship"]
            if rel == "peer":
                peer_provider.add(asn1+" "+asn0)
                peer_provider.add(asn0+" "+asn1)
            elif rel == "provider":
                peer_provider.add(asn1+" "+asn0)
            else: 
                peer_provider.add(asn0+" "+asn1)

        hasNextPage = data["pageInfo"]["hasNextPage"]
        offset += len(data["edges"])
        break

    return peer_provider



def AsnLinksQuery(first,second, asns):
    return """{
    asnLinks(first:%s, offset:%s) {
        totalCount
        pageInfo {
            first
            offset
            hasNextPage
        }
        edges {
            node {
                relationship
                asn0 {
                    asn
                }
                asn1 {
                    asn
                }
                numberPaths
            }
        }
    }
}""" % (str(first), str(second))

def download_paths(peer_provider):

    # The set of ASes reachable through an AS's customers
    asn__cone = {}

    print ("Downloanding paths",file=sys.stderr)

    # Initialize BGPStream, with routeviews-stream project, filtering for amsix.
    stream = BGPStream(project="routeviews-stream", filter="router amsix")
    # The stream will not load new data till its done with the current pulled data.
    stream.set_live_mode()
    print("starting stream...", file=sys.stderr)
    for record in stream.records():
        rec_time = time.strftime('%y-%m-%d %H:%M:%S', time.localtime(record.time))
        for elem in record:
            prefix = ip_network(elem.fields['prefix'])
            # Only print elements that are announcements (BGPElem.type = "A").
            if elem.type == "A":
                asns = elem.fields['as-path'].split(" ")

                # Skip until the first peer-peer or provider->customer link
                i = 0
                while i+1 < len(asns):
                    link = asns[i]+" "+asns[i+1]
                    i += 1

                # Since an AS only announces it's customer cone it's peer or provider,
                # The remaining ASes in the path are in it's customer cone.
                while i < len(asns):
                    if asns[i] not in asn__cone:
                        asn__cone[asns[i]] = set()
                    cone = asn__cone[asns[i]]
                    j = i+1
                    while j < len(asns):
                        cone.add(asns[j])

    return asn__cone

#run the main method
main()
