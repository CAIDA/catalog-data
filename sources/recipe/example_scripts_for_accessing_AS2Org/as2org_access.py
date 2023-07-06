# Copyright (c) 2022 The Regents of the University of California
# All Rights Reserved

import requests
import json
import argparse
import sys

URL = 'https://api.data.caida.org/as2org/v1'
ASRANK_URL = 'https://api.asrank.caida.org/v2'

def main():
  # Handle flags and args
  parser = argparse.ArgumentParser()
  parser.add_argument("-d", type=int, required=False)
  parser.add_argument("-l", type=str, required=False)
  parser.add_argument("-o", type=str, required=False)
  args = parser.parse_args()
  if args.d:
    dataset(args.d)
  if args.l: 
    largestAS(args.l)
  if args.o: 
    org(args.o)

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

# Helper methods
def getJsonResponse(URL):
  response = requests.get(URL)
  return response.json()

def findASN(orgName):
  """
  Find ASN of largest AS of given org name
  """
  # Find org id associated with orgName
  try:
    url_built = f"{URL}/orgs"
    orgs = getJsonResponse(url_built)
    orgId = 0
    for org in orgs["data"]:
      if (org["orgName"] == orgName):
        orgId = org["orgId"]
  except Exception as err: 
    print(url_built)
    print(err)
    sys.exit()

  asrank_org = getJsonResponse(f"{ASRANK_URL}/restful/organizations/{orgId}")
  return asrank_org["data"]["organization"]["members"]["asns"]["edges"][0]["node"]["asn"]

main()