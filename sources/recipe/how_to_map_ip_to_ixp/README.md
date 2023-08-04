# <b>How to map an IP address to a Internet eXchange Point (IXP)</b>

~~~json
{
    "id" : "how_to_map_ip_to_ixp",
    "visibility" : "public",
    "name" : "How to map an IP address to a Internet eXchange Point (IXP)",
    "description" : "Maps each IP address to it's Internet Exchange Point.",
    "links" : [{"to" : "dataset:ixps"}],
    "tags" : [
        "IPv4",
        "IXP"
    ],
    "authors":[
        {
            "person": "person:zak_nathan",
            "organizations": ["CAIDA, San Diego Supercomputer Center, University of California San Diego"]
        }
    ]
}
~~~

## <b><u>Introduction</u></b>

The following solution shows how to parse a given IXP Dataset (.jsonl) file and map given IPs Address (.txt) to a IX. A script has been given which takes in a text file (-i) with a list of IP Addresses and a IXP Dataset (-ix), which prints out IXs that are matched to an IP. If the output option (-o) is selected and a file is specified, the mapped IP, IX, and IX Name, will be formatted as a CSV and exported.

### <b>Usage</b>

To use this script two files are required, a file containing IP addresses (one per line) and a IXP Dataset, which can be downloaded [here](https://publicdata.caida.org/datasets/ixps/).

To map all IPs to IXs and print to terminal:

~~~bash
python3 ip_map_ixp.py -i <ip_file> -ix <ixs_file>
~~~

To map all IPs to IXs and save to file:

~~~bash
python3 ip_map_ixp.py -i <ip_file> -ix <ixs_file> -o <output_file>
~~~

A sample IP file can be found [here](https://github.com/CAIDA/catalog-data/blob/294-how-to-map-ip-to-ixp/sources/recipe/how_to_map_ip_to_ixp/ip.txt).

## <b><u>Solution</u></b>

Below are code samples from the available script showing how to parse and map an IP to an IX. The script parses the given files, and creates a dictionary from the IXP Dataset, ```ip_ixs```. The first sample shows how to parse the IXP Dataset from the provided .jsonl file:

~~~Python
def parseJSONL(ixpJSONL):
    ixs = {}
    index = 0
    #Test if file exists.
    try:
        open(ixpJSONL)
    except:
        print("Failed to open file:", ixpJSONL)
        return

    #Reads every line in JSONL file.
    for line in open(ixpJSONL):
        #Add dictionary index if line is not a comment.
        if line[0] != '#':
            ixs[index] = json.loads(line)
            index += 1
    #Return completed dictionary
    return ixs
~~~

Below is a function for parsing the IP Address file:

~~~Python
def parseIPs(ipFile):
    try:
        open(ipFile)
    except:
        print("Failed to open file:", ipFile)
        return

    ips = []
    for line in open(args.ip_list):
        ips.append(line.rstrip('\n\r'))
    return ips
~~~

Below is a function to find what index in the ```ip_ixs``` dictionary a specified IP Address is located:

~~~Python
def findIndex(ip, ixps):
    #Iterate through dictionary.
    for i in range(0, len(ixps)):
        #Iterate through associated IPv4 Addresses in dictionary index.
        for x in ixps[i]['prefixes']['ipv4']:
            #Check if any IP matched the one specified.
            if ip == x.split('/')[0]:
                #If a match is found, return dictionary index.
                return i
~~~

## <b><u>Background</u></b>

### <b> What is an Internet Exchange Point (IXP)? </b>

An IXP is a physical infrastructure that allow Internet Service Providers (ISPs), Content Delivery Networks(CDNs), and other organizations to exchange Internet traffic between their networks.
IXPs are managed by one of the following: non-profit organizations, associations of ISPs, operator-neutral for-profit companies, university or government agencies, informal associations of networks.

### <b> What is an IP address? </b>

IP addresses are unique identifiers that connect devices to the Internet network for communication purposes.

### <b> IP File Format </b>

Any lines starting with a number sign will be ignored.

~~~test
# ....
<ip>
<ip>
~~~

Copyright (c) 2022 The Regents of the University of California
All Rights Reserved