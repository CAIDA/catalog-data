# Example Scripts for Accessing AS2Org

~~~
{
    "name": "Example Scripts for Accessing AS2Org",
    "description": "This solution downloads the full as2org dataset for a target date, the largest AS with a given organization name, and the organization for a target AS.",
    "links": [
        "software:as_organization_api",
        "dataset:as_rank",
        "recipe:how_to_download_from_asrank"
    ],
    "tags": [
        "measurement methodology",
        "topology",
        "software/tools",
        "ASN",
        "organization"
    ],
    "authors":[
        {
            "person": "person:tran__david",
            "organizations": [ "CAIDA, San Diego Supercomputer Center, University of California San Diego" ]
        }
    ]
}
~~~

## Introduction

The solution downloads the full as2org dataset for a target date, the largest AS with a given organization name, and the organization for a target AS using the AS2Org API.

## Solution

The full script can be found [here](https://github.com/CAIDA/catalog-data/blob/master/sources/recipe/as2org_access.py). Below are methods for downloading the as2org dataset, largest AS, and organization for a specified target.

Usage: `python as2org_access.py -d <target date> -l <target org name> -o <target ASN>`

Examples:

- `python as2org_access.py -d 20210701 -l "Charter Communications"`

- `python as2org_access.py -o 3356`

~~~
def dataset(targetDate):
  """
  Download as2org dataset for a target date (YYYYMMDD)
  """
  data = []
  file = open(f"as2org_dataset_{targetDate}.json", "w")
  print(f"Downloading dataset for target date {targetDate}")

  for type in {"asns", "orgs"}:
    hasNextPage = True  
    first = 5000
    offset = 0

    while (hasNextPage):
      url_built = f"{URL}/{type}/?datestart={targetDate}&dateend={targetDate}&offset={offset}&first={first}"
      print("  Downloading", type + ":", "offset", offset)

      try:
        response = getJsonResponse(url_built)
        hasNextPage = response["pageInfo"]["hasNextPage"]
        first = response["pageInfo"]["first"]
        offset = response["pageInfo"]["offset"] + first

        if (response["data"] != None):
          for object in response["data"]:
            data.append(object)          
      except Exception as err:
        print(url_built)
        print(err)
        sys.exit()

  file.write(json.dumps(data, indent=4))
  file.close()
  print("-" * 40)

def largestAS(targetOrgName):
  """
  Download largest AS with a given organization name
  """
  largestASN = 0
  largestAS = None
  file = open(f"largestAS_{targetOrgName}.json", "w")
  print(f"Downloading largest AS for org name {targetOrgName}")

  try: 
    largestASN = findASN(targetOrgName)
  except Exception as err:
    print(url_built)
    print(err)
    sys.exit()

  url_built = f"{URL}/asns/{largestASN}"
  try:
    response = getJsonResponse(url_built)
    largestAS = response["data"][0]
  except Exception as err:
    print(url_built)
    print(err)
    sys.exit()

  file.write(json.dumps(largestAS, indent=4))
  file.close()
  print("-" * 40)

def org(targetASN):
  """
  Download the organization for a target AS
  """
  # Get orgid given asn
  url_built = f"{URL}/asns/{targetASN}/"
  org = None
  orgId = 0
  file = open(f"org_{targetASN}.json", "w")
  print(f"Downloading org for target AS {targetASN}")

  try:
    response = getJsonResponse(url_built)
    orgId = response["data"][0]["orgId"]

  except Exception as err:
    print(url_built)
    print(err)
    sys.exit()

  # Get org given orgid
  url_built = f"{URL}/orgs/{orgId}"
  try: 
    response = getJsonResponse(url_built)
    org = response["data"][0]
  except Exception as err: 
    print(url_built)
    print(err)
    sys.exit()

  file.write(json.dumps(org, indent=4))
  file.close()
  print("-" * 40)
~~~

## Background

The [AS2Org API](https://api.data.caida.org/as2org/v1/doc) provides a mapping from AS numbers to organizations. 

From ["How to get an ASN's name, organization and country?"](https://catalog.caida.org/details/recipe/getting_an_asns_name_country_organization) recipe:

- **What is an AS?**
   - AS stands for Autonomous system.
   - It can be broadly be thought of as a single organization, or a collection of routers that route groups of IP addresses under a common administration, typically a large organization or an ISP (Internet Service Provider).
   - It is a connected group of one or more IP addresses (known as IP prefixes) that provide a common way to route internet traffic to systems outside the AS.
   - Each AS is responsible for routing traffic within itself. This is known as intra-AS routing.
   - Each AS can also route traffic between itself and other autonomous systems. This is known as inter-AS routing. 
   -  More information on AS can be found [here]( https://www.cs.rutgers.edu/~pxk/352/notes/autonomous_systems.html) and [here](https://catalog.caida.org/details/media/2016_as_intro_topology_windas_intro_topology_wind.pdf)

- **What is an ASN?**
    - Each AS is assigned a unique ASN, or *Autonomous System Number* that allows it to be uniquely identified during routing.

- **What is an ASN's organization?**
   - Each ASN can be mapped to a organization that controls multiple AS's over its network.

- **What is an ASN's country?**
   - The country where the ASN's organization is located.

## Caveats

The solution script uses the [ASRank API](https://api.asrank.caida.org/v2/restful/doc) to find the largest AS for a target organization name, since the AS2Org API does not provide any information the size of an AS.
