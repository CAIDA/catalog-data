~~~json
{
    "id": "how_to_parse_telescope_flowtuple_xml",
    "visibility":"public",
    "name": "How to parse telescope flowtuple xml",
    "description": " ",
    "tags": [
      "traffic", 
      "telescope-flowtuple", 
      "security",
      "telescope",
      "UCSD Network Telescope"
    ],
    "links": [
        "dataset:corsaro_flowtype",
    ],
    "authors":[
        {
            "person": "person:isacmlee",
            "organizations": ["CAIDA, San Diego Supercomputer Center, University of California San Diego"]
        }
    ]
}
~~~

## Introduction 
The following recipe provides an explanation of STARDUST and telescope data as well as an in-depth walkthrough on how to parse telescope flowtuple data. 

### Purpose
 Historically, researchers have used telescope traffic data (<i>aka</i> Internet Background Radiation, or IBR) to study worms, DoS attacks, and scanning (e.g. searching for hosts running a vulnerable service). Relatively recent research has explored the possibility of using IBR as a data source of Internet-wide measurements and inference for macroscopic Internet properties. See [Leveraging Internet Background Radiation for
Opportunistic Network Analysis](https://www.caida.org/catalog/papers/2015_leveraging_internet_background_radiation/leveraging_internet_background_radiation.pdf). 

You can read about further research at [STARDUST/research](https://stardust.caida.org/research/).


## Background
Check [STARDUST](https://stardust.caida.org/overview/) for more details.

#### What are Network Telescopes? 
Network Telescopes (<i>aka</i> Internet black holes, darknets, darkspace) are passive monitoring systems capturing unsolicited Internet traffic sent to a segment of unutilized IP address space (i.e. IP addresses owned by an organization but not assigned to any hosts). Traffic captured at network Telescopes provide precious data for researchers to study a large variety of Internet-related phenomena. 


#### What is STARDUST? 
<b>S</b>ustainable <b>T</b>ools for <b>A</b>nalysis and <b>R</b>esearch on <b>D</b>arknet <b>U</b>n<b>S</b>olicited <b>T</b>raffic

STARDUST is a collection of <b>software tools</b> and <b>datasets</b> as well as <b>research infrastructure</b> built to make real-time and historical analysis of telescope traffic efficient and easily accessible to researchers. 

STARDUST hosts the <i>UCSD Network Telescope</i>, one of the largest known network Telescopes on the Internet (~12 million IPv4 addresses). It also provides data from network Telescopes operated by other collaborating organizations. 
#### Why use STARDUST? 
STARDUST enables users to access Telescope traffic in real-time as well as historical datasets with various levels of granularity.

#### What is FlowTuple data?
FlowTuple data is an aggregated representation of traffic captured at the network telescope that enables a more efficient processing and analysis for many research use cases that do not need access to the full packet contents. 

Check [here](https://stardust.caida.org/docs/data/flowtuple/) for more details on FlowTuples.

## Gaining Access to Telescope FlowTuple Data
Submit the [CAIDA UCSD Network Telescope Datasets Request Form](https://www.caida.org/catalog/datasets/request_user_info_forms/telescope-near-real-time_dataset_request/). 

Once submitted, <b>allow for five to ten business days for your request to be processed</b>. Once users are approved for data access, they will receive an account on a CAIDA machine that provides direct access to the Telescope data requested. Accounts are valid for a nominal twelve months in which research is expected to be complete. 

<b>Note: all analysis must be performed on CAIDA computers; download of raw data is not allowed.</b> 

## Accessing a CAIDA VM 
Once you have gained access to the telescope flowtuple data, please see walkthrough [here](https://stardust.caida.org/docs/accessingthevm/).

## Parsing the Data through Swift and PyAvro-STARDUST
As STARDUST uses cloud-based Swift object storage to store raw traffic traces and flow-level traces, we must first authenticate with Swift to gain access to the containers and objects with our desired data.

#### Authenticating with Swift
Find your credential file (each computer will be different).
~~~bash
user@vm001:~$ ls -a
user@vm001:~$ cat .limbo_cred

export OS_PROJECT_NAME=telescope
export OS_USERNAME=userxxx
export OS_PASSWORD=xxxxx
export OS_AUTH_URL=https://hermes-auth.caida.org
export OS_IDENTITY_API_VERSION=3
~~~
* This file is used to set some environment variables that allow your Swift client to authenticate with the Swift cluster.

To source the file which loads the variables into the environment (note the first dot followed by a space):
~~~bash
user@vm001:~$ . .limbo_cred
~~~

When you use the Swift command shown below, it uses the environment variables to authenticate with Swift, allowing you to gain access to the data.

~~~bash
user@vm001:~$ swift auth
~~~

#### Accessing Containers and Objects with Swift
FlowTuple data is stored in Openstack Swift using the Apache Avro data format. Specifically, data for each year is saved in a separate Swift container:
* telescope-ucsdnt-avro-flowtuple-v4-2021
* telescope-ucsdnt-avro-flowtuple-v4-2020
* telescope-ucsdnt-avro-flowtuple-v4-...

To see first 5 objects within a container:
~~~bash
user@vm001:~$ swift list telescope-ucsdnt-avro-flowtuple-v4-2021 | head -n 5

datasource=ucsd-nt/year=2021/month=01/day=01/hour=00/v3_5min_1609459200.ft4.avro
datasource=ucsd-nt/year=2021/month=01/day=01/hour=00/v3_5min_1609459500.ft4.avro
datasource=ucsd-nt/year=2021/month=01/day=01/hour=00/v3_5min_1609459800.ft4.avro
datasource=ucsd-nt/year=2021/month=01/day=01/hour=00/v3_5min_1609460100.ft4.avro
datasource=ucsd-nt/year=2021/month=01/day=01/hour=00/v3_5min_1609460400.ft4.avro
~~~
To process the file you will need to get the data to your VM because the file is stored on the Swift cluster, not locally. With the size of the file, you will not be able to download the file due to the size availability on your VM.

#### Processing FlowTuple Files with PyAvro-STARDUST 
To process the data, we will utilze the PyAvro-STARDUST module. However, we will first create a virtual environment <i>stardust</i> with virtualenv.

<i>Your VM will most likely require you to install both pip3 and virtualenv.</i>

With your new virtual environment, follow instructions to install PyAvro-STARDUST [here](https://github.com/CAIDA/pyavro-stardust).

##### Transferring a PyAvro script to remote VM 
For our example, we will use [this](https://github.com/CAIDA/pyavro-stardust/blob/master/examples/flowtuple4-example.py) script to parse the data for finding the global counter for each flowtuple, the number of packets for each IP protocol, the most common TTLs, packet sizes, and TCP flag combinations that our Swift flowtuple object contains.

You can copy and paste the code from the script into your own Python file in your local environment. But in order to transfer this script from our local machine to the VM, we must use <i>scp</i>. 

First, open a new tab in your terminal and navigate to the directory with your python script. 

This line securely transfers your python script to your gateway:
~~~bash
scp pyavro-example.py username1@limbonet-gw.caida.org:
~~~
<i>"username1" will be the username given when provided access to the data.</i> 

Once you log back into your gateway, you will be able to transfer from remote environment to another remote environment of a CAIDA VM.

~~~bash
scp pyavro-example.py login_name:
~~~
<i>Leaving it blank after the ':' will transfer the script to the home directory.</i>

##### Running the PyAvro script
To run the script, use this format:
~~~bash
user@vm001L:~$ python pyavro-example.py swift://<container name>/<object name>
~~~
Example with real data (remember to authenticate swift):
~~~bash
user@vm001L:~$ python pyavro-example.py swift://telescope-ucsdnt-avro-flowtuple-v4-2021/datasource=ucsd-nt/year=2021/month=01/day=01/hour=00/v3_5min_1609459200.ft4.avro
~~~

##### Outputs
You will output the global counter for each flowtuple, the number of packets for each IP protocol, the most common TTLs, packet sizes, and TCP flag combinations that our Swift flowtuple object contains.

## Caveats
#### Data Policy 
CAIDA strictly enforces a "take software to the data" policy for this dataset: <b>all analysis must be performed on CAIDA computers; download of raw data is not allowed.</b> CAIDA provides several basic tools to work with the dataset, including CoralReef and Corsaro. Researchers can also upload their own analysis software.


