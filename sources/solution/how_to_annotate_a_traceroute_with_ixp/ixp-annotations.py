import json
import argparse
import numpy as np
import pyasn
import os

parser = argparse.ArgumentParser(description='Finds IXP annotations.')
parser.add_argument('path', metavar='p', type=str,
                    help='path to ixp dataset')
parser.add_argument('list', metavar='l', nargs='+', type=str,
                    help='list of ip addresses')
args = parser.parse_args()

def load_traceroute(path):
    temp_file = "_ixp.dat"
    with open(path) as f:
        next(f)
        data = []
        diction = {}
        i = 1
        for line in f:
            obj = json.loads(line)
            name = obj['name']
            diction[i] = name
            recorded_ipv4 = list(map(lambda x: x+"\t%d"%i, obj['prefixes']['ipv4']))
            recorded_ipv6 = list(map(lambda x: x+"\t%d"%i, obj['prefixes']['ipv6']))
            data+=(recorded_ipv4+recorded_ipv6)
            i+=1
        hdrtxt = '; IP-ASN32-DAT file\n; Original file : <Path to a rib file>\n; Converted on  : temp\n; CIDRs         : 512490\n;'
        np.savetxt(temp_file, data, header=hdrtxt,fmt='%s')
        ixpdb = pyasn.pyasn(temp_file)
        os.remove(temp_file)
        return ixpdb, diction
                
def annotate_traceroute(ixpdb, diction, ips):
    """
    Inputs a path to data file and a list of IP addresses and returns a corresponding list of IXP names.
    """
    # Converts all into IP address format, appends None if not IP address
    ixp_list = [None]*len(ips)
    for index in range(len(ips)):
        try:
            ixpdb.lookup(ips[index])
        except ValueError:
            print("Invalid IP: ", ips[index])
            continue  
        if ixpdb.lookup(ips[index])[1]:
            ixp_list[index] = diction[ixpdb.lookup(ips[index])[0]]
        else:
            continue                
    print(ixp_list)

if __name__ == '__main__':
    # annotate_traceroute(args.path, args.list)
    ixpdb, diction = load_traceroute(args.path)
    annotate_traceroute(ixpdb, diction, args.list)
