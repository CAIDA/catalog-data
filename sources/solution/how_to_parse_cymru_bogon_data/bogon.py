import pyasn
import argparse

parser = argparse.ArgumentParser(description='Finds IXP annotations.')
parser.add_argument('bogon', metavar='b', type=str,
                    help='path to bogon dataset')

parser.add_argument('pyasndb', metavar='p', type=str,
help='path to bgp as path dataset')

parser.add_argument('ips', metavar='i', nargs='+', type=str,
                    help='list of ip addresses')

args = parser.parse_args()

def bogon_load(path):
    f = open(path, "r")
    ips = []
    next(f)
    for line in f.readlines():
        ips.append(line.replace('\n', ''))
    return ips

def bogon_check_ip(ips, bogons, db):
    asndb = pyasn.pyasn(db)
    final = [False]*len(ips)
    for ip in range(len(ips)):
        try:
            prefix = asndb.lookup(ips[ip])[1]
            if prefix:
                if prefix in bogons:
                    final[ip] = True
        except:
            continue
    print(final)

if __name__ == '__main__':
    bogons = bogon_load(args.bogon)
    bogon_check_ip(args.ips, bogons, args.pyasndb)