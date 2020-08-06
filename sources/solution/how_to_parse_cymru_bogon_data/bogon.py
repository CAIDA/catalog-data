import argparse
import pyasn
import numpy as np
import os

parser = argparse.ArgumentParser(description='Checks whether an array of addresses is bogon.')
parser.add_argument('bogon', metavar='b', type=str,
                    help='path to bogon dataset')

parser.add_argument('ips', metavar='i', nargs='+', type=str,
                    help='list of ip addresses')

args = parser.parse_args()

def bogon_load(path):
    """
    Loads bogon dataset into memory.
    """
    temp_file = "_bogon.dat"
    f = open(path, "r")
    ips = []
    next(f)
    for line in f.readlines():
        ips.append(line.replace('\n',"") + "\t1")
    hdrtxt = '; IP-ASN32-DAT file\n; Original file : <Path to a rib file>\n; Converted on  : temp\n; CIDRs         : 512490\n;'
    np.savetxt(temp_file, ips, header=hdrtxt,fmt='%s')
    bogondb = pyasn.pyasn('_bogon.dat')
    os.remove(temp_file)
    return bogondb

def bogon_check_ip(ips, bogondb):
    """
    Checks whether a given IP address is bogon
    """
    final = []
    for ip in ips:
        # Check if IP is valid
        try:
            bogondb.lookup(ip)
        except ValueError:
            print("Invalid IP: ", ip)
            final.append(False)
            continue
        
        # Look up IP
        if bogondb.lookup(ip)[1]:
            final.append(True)
        else:
            final.append(False)
    print(final)

if __name__ == '__main__':
    bogondb = bogon_load(args.bogon)
    bogon_check_ip(args.ips, bogondb)