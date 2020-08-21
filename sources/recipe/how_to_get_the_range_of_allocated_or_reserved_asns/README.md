~~~
{
    "id": "how_to_get_the_range_of_allocated_or_reserved_asns",
    "name": "How to get the range of allocated or reserved asns?",
    "description": "The following solution will create two dictionaries listing the ranges in which AS numbers: one compressed, one not compressed.",
     "links": [{"to":"dataset:iana_as_numbers"}],
    "tags":[
      "asn", 
      "iana", 
      "autonomous system"
    ]
}
~~~

## Solution

This solution will return two dictionaries - one compressed (with only allocated and reserved keys) and one with designations. 

**Usage**: 

The function `iana_asn_asignee` inputs two dataframe paths - one for the IANA's 16-bit asn csv file and one for IANA's 32-bit asn csv file, and returns a dictionary with designation names. The function `iana_asn_compressed` returns a dictionary with all designations converted to "allocated," revealing only the ranges of allocated and reserved numbers. 

These links will automatically download the current IANA ASN space registries:

- 16-bit: https://www.iana.org/assignments/as-numbers/as-numbers-1.csv
- 32-bit: https://www.iana.org/assignments/as-numbers/as-numbers-2.csv

`$ python3 current-asn.py [16-bit csv file path] [32-bit csv file path]`

~~~python 
import pandas as pd
import argparse
import os


def aggregate_ranges(ls):
    """
    Helper function that aggregates consecutive lists of ranges into a single range.
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
    Helper function returns either "reserved", "unassigned", or "allocated"
    """
    if 'reserved' in x:
        return 'reserved'
    if 'unassigned' in x:
        return 'unassigned'
    else:
        return 'allocated'

def clean_designation_names(x):
    """
    Helper function returns either "reserved", "unassigned", or "allocated"
    """
    if 'reserved' in x:
        return 'reserved'
    if 'unassigned' in x:
        return 'unassigned'
    else:
        return x.replace('assigned by', '').strip()


def combine(csv_path16, csv_path32):
    """
    Combines 16-bit and 32-bit csv files.
    """   
    current_16 = pd.read_csv(csv_path16)
    current_32 = pd.read_csv(csv_path32)
    current_32 = current_32.loc[current_32["Number"] != '0-65535']
    return pd.concat([current_16, current_32])

def iana_asn_asignees(csv_path16, csv_path32):
    """
    Takes in two IANA files (one for 32-bit and one for 16-bit asn) and returns a dictionary with ranges by assignee.
    """
    current = combine(csv_path16, csv_path32)
    current["Description"] = current["Description"].apply(lambda x: clean_designation_names(x.lower()))
    current["Number"] = current["Number"].apply(lambda x: [int(x), int(x)] if '-' not in x else [int(x.split('-')[0]), int(x.split('-')[1])])

    asn = (current
    .drop(current.columns.difference(['Number','Description']), axis=1)
    .groupby("Description")["Number"]
    .apply(list)
    .apply(aggregate_ranges)).to_dict()

    try:
        del asn['unallocated']
    except KeyError:
        pass

    return asn

def iana_asn_compressed(csv_path16, csv_path32): 
    """
    Takes in two IANA files (one for 32-bit and one for 16-bit asn) and returns a dictionary with allocated or reserved ranges.
    """
    current = combine(csv_path16, csv_path32)
    current["Description"] = current["Description"].apply(lambda x: simplify(x.lower()))
    current["Number"] = current["Number"].apply(lambda x: [int(x), int(x)] if '-' not in x else [int(x.split('-')[0]), int(x.split('-')[1])])

    asn = (current
    .drop(current.columns.difference(['Number','Description']), axis=1)
    .groupby("Description")["Number"]
    .apply(list)
    .apply(aggregate_ranges)).to_dict()

    try:
        del asn['unallocated']
    except KeyError:
        pass

    return asn


#print(iana_asn_asignees(csv1path, csv2path), iana_asn_compressed(csv1path, csv2path))
~~~

## Background

### What is ASN?

- ASN is short for autonomous system numbers
- ASNs are assigned to Autonomous Systems (AS), which are sub networks that amalgamate to form the Internet network
- Autonomous systems are allocated to unique ASN first through IANA, then through their region's Regional Internet Registry
- Information about the ASNs have been gathered from IANA, an organization that manages and records IP address and ASN allocations


## Why are two files needed?
- ASNs began as 16-bit numbers, meaning that there were previously only 65,000 unique numbers. In the early 2010s, a steady growth of the Internet network revealed the need for expansion. They thus began using 32-bits to allow for more unique numbers
- IANA currently formats the datasets so that 16-bit allocations are separate from 32-bit allocations. This solution will combine the two datasets to return all of the number ranges
- Note: The numbers are directly transferable as 32-bit allocations start from where the 16-bit allocations end

## Caveats
- This solution uses only the current datasets provided by IANA
- This solution combines the 16-bit and 32-bit csv files, so both must be provided
