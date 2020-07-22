~~~
{
    "id": "iana_asn_allocation",
    "name": "IANA ASN Allocations",
    "description": "The following solution will create two json files (one for 16-bit, one for 32-bit) listing the ranges in which AS numbers are reserved and allocated.",
    "question": "How to get the range of reserved and allocated ASNs?"
    tags:[
      "asn", 
      "iana", 
      "ipv4", 
      "autonomous system"
    ]
}
~~~

## Solution

This solution will download two gzipped json files in the indicated download directory:
- Current 16-bit allocations
- Current 32-bit allocations

**Usage**: `$ python3 current-asn.py -p [download path]`

~~~python 
import pandas as pd
import argparse
import os
import json
import gzip

def dir_path(string):
    if os.path.isdir(string):
        return string
    else:
        raise NotADirectoryError(string)

parser = argparse.ArgumentParser(description='Download current asn json ranges.')
parser.add_argument('-p', '--path', type=dir_path, help='directory for download i.e. ../allocations/')
args = parser.parse_args()


def aggregate_ranges(ls):
    """
    Aggregates consecutive lists of ranges into a single range.
    """
    final = []
    i = 0
    if len(ls) == 1:
        return ls
    curr_range = ls[0]
    while i != len(ls)-1:
        i+=1
        current = ls[i]
        if ((curr_range[0] <= current[1]) and (curr_range[0] >= current[0])) or ((curr_range[0] <= current[0]) and (curr_range[1] >= current[0])):
            curr_range = [min([curr_range[0], current[0]]), max([current[1], curr_range[1]])]
            if i == len(ls)-1:
                final.append(curr_range)
                return final
            continue
            current = ls[i]
        if (curr_range[1] + 1 == current[0]) or (curr_range[1] == current[0]):
            curr_range[1] = current[1]
            if i == len(ls)-1:
                final.append(curr_range)
                return final
        else:
            final.append(curr_range)
            if i == len(ls)-1:
                final.append(current)
                return final
            else:
                curr_range = current
    return final

def simplify(x):
    """
    Returns either "reserved", "unassigned", or "allocated"
    """
    if 'reserved' in x:
        return 'reserved'
    if 'unassigned' in x:
        return 'unassigned'
    else:
        return 'allocated'

def list_format(num): 
    if type(num) == int:
        num = str(num)
    if '-' in num:
        return [int(num.split('-')[0]), int(num.split('-')[1])]
    else:
        return [int(num), int(num)]

###### Reads in current csv files from IANA ######
current_16 = pd.read_csv('https://www.iana.org/assignments/as-numbers/as-numbers-1.csv')
current_32 = pd.read_csv('https://www.iana.org/assignments/as-numbers/as-numbers-2.csv')


###### Simplifies designations ######
current_16["Description"] = current_16["Description"].apply(lambda x: simplify(x.lower()))
current_32["Description"] = current_32["Description"].apply(lambda x: simplify(x.lower()))

###### Aggregates separate rows to determine range of allocated/unallocated/reserved asn ######
current_16["Number"] = current_16["Number"].apply(list_format)
current_32["Number"]= current_32["Number"].apply(list_format)

asn16 = (current_16
 .drop(current_16.columns.difference(['Number','Description']), axis=1)
 .groupby("Description")["Number"]
 .apply(list)
.apply(aggregate_ranges)).to_dict()

asn32 = (current_32
 .drop(current_32.columns.difference(['Number','Description']), axis=1)
 .groupby("Description")["Number"]
 .apply(list)
.apply(aggregate_ranges)).to_dict()

if __name__ == "__main__":
    if os.path.exists(args.path):
        with gzip.open(args.path + "asn-16-bit.json.gz", "wt", encoding="ascii") as outfile:
            json.dump(asn16, outfile)
        with gzip.open(args.path + "asn-32-bit.json.gz", "wt", encoding="ascii") as outfile:
            json.dump(asn32, outfile)
    else:
        print("directory does not exist")
~~~

## Background

### What is ASN?

- ASN is short for autonomous system numbers
- ASNs are assigned to Autonomous Systems, which are sub networks that amalgamate to form the entire Internet network
- Autonomous systems are allocated to unique ASN first through IANA, then through their region's Regional Internet Registry
- Information about the ASNs have been gathered from IANA, an organization that manages and records IP address and ASN allocations


### Why does this solution contain two files?

- ASNs began as 16-bit numbers, meaning that there are around 65,000 unique ASNs
- Researchers realized that 16 bits would not be enough, and made ASNs 32-bit numbers instead

## Caveats
- This solution uses only the current dataset provided by IANA
- Results contain only the range of allocated and reserved ASNs. To download files for rir allocations, view solution/mapping_asn_to_rir
