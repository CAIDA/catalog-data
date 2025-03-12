# How to Identify Root Causes in Customer Cone Changes

~~~json
{
    "id" : "how_to_identify_root_causes_in_customer_cone_changes",
    "visibility" : "public",
    "name" : "How to Identify Root Causes in Customer Cone Changes",
    "description" : "A tool for exploring the potential causes of changes in a given customer cone",
    "links": [],
    "tags" : [],
    "authors":[
        {
            "person": "person:masserfrye__richard",
            "organizations": ["CAIDA, San Diego Supercomputer Center, University of California San Diego"]
        }
    ]   
}
~~~

### Introduction
#### What is a customer cone?

A customer cone is the set of Autonomous Systems (ASes). An AS is a group of computers (e.g. a telecom company) that functions as a conduit for internet traffic; ASes often have business relationships with each other to facilitate the exchange of traffic. When data is sent from one computer to another over the internet, it passes through a series of ASes; this series is called a path.

The customer cone of a given AS is made up of ASes that satisfy two requirements: (a) the given AS must be able to direct traffic to them, and (b) they must be customers of that AS, or customers of customers, etc.

As an example, say we want to determine whether an AS called A is in the customer cone of an AS called B. For requirement (a), we would have to examine the set of paths and check whether there are any that indicate B directs traffic to A. Suppose the following path is observed: 

`C | B | X | A`

Suppose also that B and C do not have a paid relationship (in other words, they are *peers*). We can infer that this path came about because C needed a route to A, and B announced to C that B had a route to A. In this example, requirement (a) is satisfied. If X is a customer of B, then (b) is satisfied, and B's customer cone contains A. 

#### What is this recipe for?

Occasionally, the customer cone of a particular AS may grow or shrink dramatically over a short period of time. The purpose of this recipe is to provide potential ways to gain some insight into why such a change may have occurred in a given case.

## Using this recipe

### Getting Started

First, select a target AS and two dates to analyze. Download a `.paths.bz2` file, a `.as-rel.txt.bz2` file, and a `.ppdc-ases.txt.bz2` file from each date; there should be 6 files in total. Put all six files into the same directory.

Then, choose either the notebook `Explainer.ipynb` or the script `table.py` for analysis. Both files contain the same code, but differ in how they can be used.

### `table.py`

`table.py` should be run from the command line, like so:

```
python3 table.py -t [Target ASN] -d1 [YYYYMMDD] -d2 [YYYYMMDD] -dir [path to directory with data] [-g] (optional, analyze gains rather than losses)
```

For example, if you're analyzing gains in the cone of AS5511 between June 1st, 2022 and August 1st, 2022, and your data files are in the directory `data`, you should run:
```
python3 table.py -t 5511 -d1 20220601 -d2 20220801 -dir data -g
```

### `Explainer.ipynb`

`Explainer.ipynb` is a notebook file that combines code and explanation to provide more detail about the analysis process. It can be opened and run with Jupyter (see [this page](https://jupyter.org/install) for installing Jupyter if you don't have it).

Copyright (C) 2023 The Regents of the University of
California. All Rights Reserved.