
~~~json
{
    "id" : "how_to_infer_router_ASes_using_bdrmapit",
    "name" : "",
    "description" : "",
    "links": [
      {"to": "dataset:"}
    ],
    "tags" : [
      "asn",
      "bdrmapit"
    ],
    "authors":[
        {
            "person": "person:victor__ren",
            "organizations": ["CAIDA, San Diego Supercomputer Center, University of California San Diego"]
        }
    ]
}
~~~

## Introduction
This program provides an implementation on how to infer router ASes using bdrmapIT.

## Background

BGP (Border Gateway Protocol)
An autonomous system (AS) consists of one or more network operators that uses the same routing policy.

Each AS is assigned a unique AS number (ASN).
Click [here](https://en.wikipedia.org/wiki/Autonomous_system_(Internet)) for more information on AS.

### bdrmapIT
If you wish to learn more about bdrmapIT, click [here](https://alexmarder.github.io/bdrmapit/) to access its website.

### ip2as

### retrieve_external

## Instructions
### Prerequisites
**Create new Python Environment and install bdrmapIT**
1. Create and activate new python environment for bdrmapIT using [Anaconda](https://www.anaconda.com/products/distribution).

~~~bash
conda create -n bdrmapit 'python<=3.9'
conda activate bdrmapit
~~~

2. Create a folder for this task. I will refer to the folder as *how_to_infer_router_ASes_using_bdrmapit*, but you can name the folder as you like.
3. Clone bdrmapIT repository `git clone https://github.com/alexmarder/bdrmapit`
4. Go to bdrmapit directory `cd bdrmapit`
5. Install required packages through pip: `pip install -r requirements.txt`
6. Compile cython code and build package `python setup.py sdist bdist_wheel build_ext`
7. Install bdrmapit and traceparser scripts using pip developer mode `pip install -e .`

**Install ip2as**
1. Install using pip: `pip install -U ip2as`

**Install retrieve_external**
1. Install *traceutils*: `pip install traceutils`
2. `git clone https://github.com/alexmarder/retrieve-external`
3. `cd retrieve-external`
4. `pip install -r requirements.txt`
5. `pip install .`

### Infer Router ASes
1. Activate bdrmapit environment: `conda activate bdrmapit`
2. Go to directory *how_to_infer_router_ASes_using_bdrmapit*
3. There are three main steps to infer router ASes:
   - Create or download prefix2as files
   - (strongly recommended) Extract origins from RIR extended delegation files
   - Create prefix to AS mappings

**Create or download prefix2as files**
1. Download Routeviews prefix2as files via CAIDA through [this link](https://publicdata.caida.org/datasets/routing/routeviews-prefix2as/).
2. (Optional) Instead of downloading prefix2as files, you can also create them manually.

**Extract origins from RIR extended delegation files**

**Create prefix to AS mappings**

## Caveats
The program may produce some unusual output (ASN may be <=0). The table below tells user how to interpret the result.

| ASN    | Explanation                                                                                                             |
|:-------|:------------------------------------------------------------------------------------------------------------------------|
 | 0      | Address has no covering prefix in the prefix-to-AS mappings, and insufficient information in the graph to derive an ASN |
| -1     | Should be rare; occurs when bdrmapIT failed to assign the router an annotation                                          |
| <=-100 | IXP public peering address with insufficient graph information for an AS annotation                                     |
The unusual output information comes from the *Unusual Output* section from [this link](https://alexmarder.github.io/bdrmapit/). Visit the webpage for more information.