# Copyright (c) 2023 The Regents of the University of California
# All Rights Reserved

import argparse
import re

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-a", type=str, dest="as_file", default=None, help="Please enter the file name of AS dataset")
    parser.add_argument("-l", type=str, dest="geo_file", default=None, help="Please enter the file name of geo info dataset")
    args = parser.parse_args()
    load_rel_geo(directory+ args.as_file, directory+ args.geo_file)

def load_rel_geo(as_file, geo_file):

    re_format = re.compile("# format:(.+)")
    geo_info = {}

    with open(geo_file, 'r') as f:
        for line in f:
            m = re_format.search(line)
            if m:
                keys = m.group(1).strip().split("|")

            #skip comment of empty line
            if line[0] == "#" or len(line) == 0:
                continue

            line = line.strip().split("|")
            info={}
            for i in range(len(keys)):
                info[keys[i]] = line[i]

            if info['lid'] not in geo_info:
                geo_info[info['lid']] = info


    print("\n\n\nlaoding as relationship file")
    count = 0
    with open(as_file, 'r') as f:
        for line in f:

            # skip comment and empty line
            if line[0] == "#" or len(line)==0:
                continue

            line = line.strip().split("|")

            # get geolocation info of asn_0
            if line[2]:
                source = geo_info[line[2].split(",")[0]]

            # get geolocation info of asn_1
            try:
                dest = geo_info[line[3].split(",")[0]]
            except:
                dest = {}

            as_rel_geo = {line[0]: {line[1]: [source, dest]}, line[1]: {line[0]: [source, dest]}}
            print(as_rel_geo) 
            input("press")

if __name__ == "__main__":
    main()