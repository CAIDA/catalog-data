~~~json
{
    "id" : "how_to_map_ips_through_pyipmeta",
    "name" : ,
    "description": ,
    "links": [
        {"to":"dataset:maxmind"}
        {"to":"dataset:netacuity_edge"}
        {"to":"dataset:routeviews_ipv4_prefix2as"}
    ],
    "tags" : [
        
    ],
    "authors":[
        
    ]
    "resources": [
        {
            "name":"how to contribute",
            "url":"https://github.com/CAIDA/catalog-data/wiki/how-to-contribute"
        }
    ]
}
~~~
## Introduction:
--------------------
PyIPMeta is a Python library that provides a high-level interface for historical and realtime lookups of:
* geolocation metadata, using Maxmind GeoIP and/or NetAcuity (Digital Element) geolocation databases
* prefix to ASN metadata using CAIDA's prefix2AS datasets.
## Installing :
Before Installing PyIpMeta, you will need:
* A version of [libipmeta](https://github.com/CAIDA/libipmeta), 3.1.0 or newer.
* Python setuptools (sudo apt install python-setuptools on Ubuntu)
* Python development headers (sudo apt install python-dev on Ubuntu)

Methods to install PyIpMeta can be found [here](https://github.com/CAIDA/pyipmeta)

The current verion of PyIPMeta is running on Python 2
* Further information on how to install PyIpMeta can be found [here](https://github.com/CAIDA/pyipmeta)

## Solution
--------------------
This solution will be comprized of two parts; one for SWIFT datasets and one for local datasets.
* Example files can be found [here](./solution_examples/)
Usage:
Using local files:
~~~
#!/usr/bin/env python

import _pyipmeta
import json

ipm = _pyipmeta.IpMeta()

# try getting a provider that exists
prov = ipm.get_provider_by_id(1)

# enables provider with local dataset
ipm.enable_provider(prov, "-b ./maxmind/2017-03-16.GeoLiteCity-Blocks.csv.gz -l ./maxmind/2017-03-16.GeoLiteCity-Location.csv.gz")

# runs geolocation on IPs specified in file
for line in open("ipnames.txt", "r"):
    sline = line.strip()
    print("Querying Maxmind for an IP address " + sline + ":")
    (res,) = ipm.lookup(sline)
    print(res)
~~~
Using dataset files from (SWIFT) database:
~~~
#!/usr/bin/env python

import pyipmeta

ipm = pyipmeta.IpMeta(providers=["maxmind"], time="20191230")
filename = "ipnames.txt"
for line in open("ipnames.txt", "r"):
    sline = line.strip()
    print("Querying Maxmind for an IP address " + sline + ":")
    (res1,) =ipm.lookup(sline) 
    print(res1)
    #print(res2)
del ipm
~~~



## Key: 
--------------------
The follow solution describes how to use PyIpMeta to preform historical and realtime geolocation metadata lookups on IP addresses.

## How to access and use datasets with PyIPMeta 
There are two ways of providing database files to PyIpMeta, either through local database files or through CAIDA's automatic database download feature (Swift).
* Swift credentials can be in environment variables or stored in a `.env` file.
* It is recommended to use `pyipmeta` for Swift datasets and `_pyipmeta` for local datasets.

How to get SWIFT credentials and more information about the used datasets can be found here:
* [Maxmind](https://catalog.caida.org/dataset/maxmind) datasets
* [NetAcuity](https://catalog.caida.org/software/netacuity) datasets
* [CAIDA's prefix two ASN (prefix2AS)](https://catalog.caida.org/dataset/routeviews_ipv4_prefix2as) datasets
## Providers (used for local files)
The available providers and their options are as follows:
* An example of the use of local maxmind is shown below:

maxmind:
* Blocks and Locations file (more information can be found [here](https://dev.maxmind.com/geoip/docs/databases/city-and-country?lang=en#locations-files))
    * `-l <file>`; where the file can either be a v1 or v2 locations file (must be used with `-b`)
    * `-b <file>`; where the file can either be a v1 or v2 blocks file (this may be repeated for multiple block files; must be used with `-b`)

netacq-edge:
* Blocks and Locations file (more information can be found [here](https://www.digitalelement.com/solutions/ip-location-targeting/netacuity/))
    * `-b <file>`; where file is an ipv4 blocks file (must be used with `-l`)
    * `-l <file>`; where file is an ipv4 locations file (must be used with `-b`)
* `-6 <file>`; ipv6 file
* `-c <file>`; country decode file
* `-r <file>`; region decode file 
* `-p <file>`; netacq2polygon mapping file
* `-t <file>`; polygon table file (can be used up to 8 times to specify multiple tables)

pfx2as:
* `-f <file>` pfx2as file

## Examples of usage of providers:
* Using local database files:
~~~
import _pyipmeta
ipm = _pyipmeta.IpMeta()
prov = ipm.get_provider_by_name("maxmind")
ipm.enable_provider(prov, "-b ./maxmind/2017-03-16.GeoLiteCity-Blocks.csv.gz -l ./maxmind/2017-03-16.GeoLiteCity-Location.csv.gz")
~~~
* Using automatic database download feature (Swift) with specific date:
~~~
import pyipmeta
ipm = pyipmeta.IpMeta(providers=["maxmind"], time="Dec 30 2019")
ipm = pyipmeta.IpMeta(providers=["maxmind"], time="20191230") // both have the same function
~~~
* Using automatic database download feature (Swift) with the latest date (currently having issues with reliability with this method):
~~~
ipm = pyipmeta.IpMeta(providers=["maxmind"])
~~~

## Fuctions:
### pyipmeta:
- **pyipmeta.IpMeta(providers=["__provider__"], time=YYYYMMDD)** :
    * Finds dataset with at specified time from specified provider
    * Multiple providers can be provided in the format `providers=["maxmind", "netacq-edge", ...]`
    * `time` argument can be omited, in which case, will load new data when it becomes available (checking every 10 minutes).
- **.lookup()** :
    * Returns the geolocation meta data for the searched up IP address / prefix
#### _pyipmeta
- **pyipmeta.IpMeta()** :
    * Run before other _pyipmeta a functions. Used to instantiate instance
- **.get_provider_by_id(__arg1__)** :
    * Returns provider by given id
- **.get_provider_by_name(__arg1__)** :
    * Returns provider by given name
- **.get_all_providers()** :
    * Returns a list of all providers
- **.enable_provider(__provider__, __args__)** : 
    * Enables one specified provider from the object returned by getting providers by name/id
    * Look a the provider section above for format based on provider used
- **.lookup()** :
    * Returns the geolocation meta data for the searched up IP address / prefix

## Explanation of the PyIPMeta's geolocation metadata fields 
--------------------
## Geolocation Metadata fields

- **connection_speed** : The connection speed of the ip address
- **city** : the city location of IP address
- **asn_ip_count** : the number of IP addresses that this ASN (or ASN group) 'owns'
- **post_code** : the postal code of corresponding to the lookup IP Address
- **lat_long** : the latitude and longitude location of the IP address
- **region** : the region the IP address originated from
- **area_code** : the area code of the ip address
- **asns** : the list of Autonomous System Numbers originating from IP address
- **continent_code** : the continent origin of IP address
- **metro_code** : the metro code of IP address
- **matched_ip_count** : the number of IPs in queried prefix covered by this record
- **region_code** :  the region code the IP address originated from
- **country_code** : the country origin of IP address (ISO2)
- **id** : the id of the ip address
- **polygon_ids** : the list of polygon ids related to ip address

## Background 
--------------------
What is geolocation and why is it important?
* **Geolocation** is the mapping of Internet resources to physical locations. In the case of case of PyIPMeta, IP addresses are mapped to 
(ised to tax/regulate for government and to capture geograpuic deployment and utilization of internet resources, and provides commercial intrests).
* PyIPMeta is an easy to use tool to extrapolate geolocation from datasets
* More information about geolocation can be found [here](https://catalog.caida.org/paper/2011_geocompare_tr).

What is ASN?
* An ASN (or *Autonomous System Number*) is a unique value applied to each AS (*Autonomous System*) that allows it boe identified during routing.

## Caveats
--------------------
* The latest date automatic database download feature (as shown above) seems to have issues with running properly. 
* There are currently issues with running local files on `pyipmeta` and Swift's database files using `_pyipmeta`.