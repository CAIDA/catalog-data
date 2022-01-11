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
python3 ip_ixp.py -i <ip_file> -ix ixs_202110.jsonl
~~~

To map all IPs to IXs and save to file:

~~~bash
python3 ip_ixp.py -i <ip_file> -ix ixs_202110.jsonl -o <output_file>
~~~

## <b><u>Solution</u></b>

Below are code samples from the available script showing how to parse and map an IP to an IX. The script parses the given files, and creates a dictionary from the IXP Dataset, ```ip_ixs```. The first sample shows how to parse the IXP Dataset from the provided .jsonl file:

~~~Python
def parseJSONL(ixpJSONL):
    ixs = {}
    key = 0
    #Test if file exists.
    try:
        open(ixpJSONL)
    except:
        print("Failed to open file:", ixpJSONL)
        return

    #Reads every line in JSONL file.
    for i in open(ixpJSONL):
        #Add dictionary index if line not a comment.
        if i[0] != '#':
            ixs[key] = json.loads(i)
            key += 1
    #Return completed dictionary
    return ixs
~~~

Below is a function for parsing the IP Address file:

~~~Python
def parseIPs(ipFile):
    #Test if file exists.
    try:
        open(ipFile)
    except:
        print("Failed to open file:", ipFile)
        return

    ips = []
    #Get every line in file.
    for i in open(args.ip_list):
        if i[0] != '#':
            #Strip IP of newline or carriage return then append to list.
            ips.append(i.rstrip('\n\r'))
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

### <b>What is a IXP?</b>

An Internet eXchange Point is a point at which multiple different networks connect to exchange traffic. Some of these networks include ISPs, CDNs, and Mobile Service Providers.

### <b> Why are they important? </b>

IXPs allow internet traffic to be redirected when connectivity issues arive, they also allow for routing traffic through faster/shorter routes to a destination.

### <b> IP File Format </b>

Any lines starting with a number sign will be ignored.

~~~test
# ....
<ip>
<ip>
~~~