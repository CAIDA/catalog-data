
~~~json
{
    "id" : "how_to_infer_router_ASes_using_bdrmapit",
    "name" : "",
    "description" : "",
    "links": [
      {"to": "dataset:caida-prefix2as"}
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
This recipe provides an implementation on how to infer router ASes using bdrmapIT.

## Background
BGP (Border Gateway Protocol) is a network protocol that consists of autonomous systems (ASes) that aims to transfer data through most efficient routes. [1] 
Click [here](https://www.cloudflare.com/learning/security/glossary/what-is-bgp/) for more information on BGP.

An autonomous system (AS) consists of one or more network operators that uses the same routing policy. Each AS is assigned a unique AS number (ASN). [2] 
Click [here](https://en.wikipedia.org/wiki/Autonomous_system_(Internet)) for more information on AS.

**bdrmapIT** is a Python implementation of the bdrmap algorithm described in [this paper](https://www.caida.org/catalog/papers/2016_bdrmap/bdrmap.pdf).
For more information on bdrmapIT, please refer to the [bdrmapIT website](https://alexmarder.github.io/bdrmapit/). [3]
**ip2as** maps router prefixes to ASes. More information about ip2as can be found [here](https://alexmarder.github.io/ip2as/). [4]
**retrieve_external** is an optional package that is strongly recommended in this recipe. It retrieves datasets such as BGP Route Announcements and RIR Extended Delegations. More information about retrieve_external can be found [here](https://github.com/alexmarder/retrieve_external/wiki). [5]  

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
8. Go back to parent directory `cd ..`

**Install ip2as**
1. Install using pip: `pip install -U ip2as`

**Install retrieve_external**
1. Install *traceutils*: `pip install traceutils`
2. `git clone https://github.com/alexmarder/retrieve-external`
3. `cd retrieve-external`
4. `pip install -r requirements.txt`
5. `pip install .`
6. Go back to parent directory `cd ..`

By here, you should have *bdrmapit*, *retrieve_external*, and *ip2as* installed. Use `git show <package>` to check if these packages are installed, make sure that you're in the bdrmapit python environment.

In your folder for this task you should also see two directories `retrieve-external` and `bdrmapit`. [3, 4] 

### Infer Router ASes
1. Activate bdrmapit environment: `conda activate bdrmapit`
2. Go to directory *how_to_infer_router_ASes_using_bdrmapit*
3. There are three main steps to infer router ASes:
   - Create or download prefix2as files
   - (strongly recommended) Extract origins from RIR extended delegation files
   - Create prefix to AS mappings

**Create or download prefix2as files**
1. Download Routeviews prefix2as files via CAIDA through [this link](https://publicdata.caida.org/datasets/routing/routeviews-prefix2as/). 
2. (Optional) Instead of downloading prefix2as files from CAIDA, you can also create them manually through instructions [here](https://alexmarder.github.io/ip2as/#extracting-origin-ases-from-ribs).

**Extract origins from RIR extended delegation files**
1. Download AS relationships file and AS customer cone files from [here](https://publicdata.caida.org/datasets/as-relationships/serial-1/). AS relationship files are named as `yyyymmdd.as-rel.txt.bz2` and AS customer cone files are names as `yyyymmdd.ppdc-ases.txt.bz2`
2. Run command `./retrieve-external/retrieve_external/retrieve.py -b <start> -e <end> -d rirs rir` to extract RIR Extended Delegation file. `<start>` and `<end>` denote data collection starting and ending dates and can be written in format yyyymmdd.
3. Create file with RIR file names through `find rirs | grep "rirs/" > rir_files.txt`. 
4. Create `rir.prefixes` file through `rir2as -f rir_files.txt -r <AS relationship file> -c <AS customer cone file> -o rir.prefixes`.   

**Create prefix to AS mappings**
1. Download [PeeringDB json file](https://publicdata.caida.org/datasets/peeringdb-v2/)
2. Download [AS-to-organization mappings](https://publicdata.caida.org/datasets/as-organizations/)
3. Run script below to produce prefix to AS mappings

~~~bash
ip2as -p <RIB prefix file> -r <RIR prefix file> -R <AS relationship file> -c <Customer Cone file> -a <AS to organization mapping file> -P <peeringdb file> -o <output file>
~~~

A concrete example with actual file names:

~~~bash
ip2as -p routeviews-rv2-20220801-0400.pfx2as.gz -r rir.prefixes -R 20220801.as-rel.txt.bz2 -c 20220801.ppdc-ases.txt.bz2 -a 20220701.as-org2info.txt.gz -P peeringdb_2_dump_2021_12_31.json -o ip2as.prefixes
~~~

More information about this step can be found [here](https://alexmarder.github.io/ip2as/#prefix-to-as). [4]

**Interpreting Result**

*test_output.txt* gives users a preview of the example output. The file is space divided where the left portion tells you the router prefix and the right portion tells which AS the router likely belongs to. 

## Caveats
The program may produce some unusual output (ASN may be <=0). The table below tells user how to interpret the result. [3]

| ASN    | Explanation                                                                                                             |
|:-------|:------------------------------------------------------------------------------------------------------------------------|
 | 0      | Address has no covering prefix in the prefix-to-AS mappings, and insufficient information in the graph to derive an ASN |
| -1     | Should be rare; occurs when bdrmapIT failed to assign the router an annotation                                          |
| <=-100 | IXP public peering address with insufficient graph information for an AS annotation                                     |

## References
1. “What Is BGP? | BGP Routing Explained | Cloudflare.” Couldflare, https://www.cloudflare.com/learning/security/glossary/what-is-bgp/. 
2. “Autonomous System (Internet).” Wikipedia, Wikimedia Foundation, 29 July 2022, https://en.wikipedia.org/wiki/Autonomous_system_(Internet). 
3. Marder, Alex. “BdrmapIT Documentation.” Bdrmapit, https://alexmarder.github.io/bdrmapit/. 
4. Marder, Alex. “Ip2as Documentation.” ip2as, https://alexmarder.github.io/ip2as/.
5. Marder, Alex. “Home · Alexmarder/retrieve_external Wiki.” GitHub, https://github.com/alexmarder/retrieve_external/wiki. 