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
    final_set = [None]*len(ips)


    with open(path) as f:
        next(f)
        for line in f:
            obj = json.loads(line)
            name = obj['name']
            recorded_ipv4 = list(map(ipaddress.ip_network, obj['prefixes']['ipv4']))
            recorded_ipv6 = list(map(ipaddress.ip_network, obj['prefixes']['ipv6']))
            for find in range(len(ips_format)):
                ele = ips_format[find]
                if ele != None:
                    if ele.version == 4:
                        for ipv4 in recorded_ipv4:
                            if ele in ipv4:
                                final_set[find] = name
                    elif ele.version == 6:
                         for ipv6 in recorded_ipv6:
                            if ele in ipv6:
                                final_set[find] = name 
                    else:
                        continue                      
    print(final_set)

if __name__ == '__main__':
    annotate_traceroute(args.path, args.list)
