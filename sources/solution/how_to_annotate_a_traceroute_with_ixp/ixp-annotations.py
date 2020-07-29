import json
import argparse
import ipaddress

parser = argparse.ArgumentParser(description='Finds IXP annotations.')
parser.add_argument('path', metavar='p', type=str,
                    help='path to ixp dataset')
parser.add_argument('list', metavar='l', nargs='+', type=str,
                    help='list of ip addresses')
args = parser.parse_args()

def annotate_traceroute(path, ips):
    """
    Inputs a path to data file and a list of IP addresses and returns a corresponding list of IXP names.
    """
    # Converts all into IP address format, appends None if not IP address
    ips_format = []
    for ip in ips:
        try:
            ips_format.append(ipaddress.ip_address(ip))
        except: 
            ips_format.append(None)
    ips_set = set(ips_format)
    final_set = [None]*len(ips)


    with open(path) as f:
        next(f)
        for line in f:
            obj = json.loads(line)
            name = obj['name']
            for ip in obj['prefixes']['ipv4']:
                hosts = set(ipaddress.ip_network(ip).hosts())
                inside = hosts.intersection(ips_set)
                if len(inside) != 0:
                    for i, e in enumerate(ips_format):
                        if e in inside:
                            final_set[i] = name
    print(final_set)

if __name__ == '__main__':
    annotate_traceroute(args.path, args.list)
