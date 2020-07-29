import argparse
import re
import warts
from warts.traceroute import Traceroute

directory = "../../../../dataset/" #add file name behind

parser = argparse.ArgumentParser()
parser.add_argument("-t", type=str, dest="traceroute_file", default=None, help="Please enter the file name of warts file")
parser.add_argument("-d", type=str, dest="dns_file", default=None, help="Please enter the file name of ip2hostname file") 
args = parser.parse_args()

re_warts = re.compile(r".warts$")
re_txt = re.compile(r".txt$")
re_ipv4_traceroute = re.compile(r"team-probing")
re_ipv6_traceroute = re.compile(r"topo-v6.l8")
re_ipv4_dns = re.compile(r"dns-names.l7")
re_ipv6_dns = re.compile(r"dns-names.l8")

if not re_warts.search(args.traceroute_file):
    print("The file type of the first argument should be .warts")
elif not re_txt.search(args.dns_file):
    print("The file type of the second argument should be .txt")
elif re_ipv4_traceroute.search(args.traceroute_file) and re_ipv6_dns.search(args.dns_file):
    print("Parsing Ipv4 traceroute file should use Ipv4 DNS file")
elif re_ipv6_traceroute.search(args.traceroute_file) and re_ipv4_dns.search(args.dns_file):
    print("Parsing Ipv6 traceroute file should use Ipv6 DNS file") 
else:

    traceroute = []
    dns = {}

    # reading DNS file
    with open(directory + args.dns_file) as f:
        for line in f:
            line = line.split()
            if len(line)==2:
                continue
            elif line[2] == "FAIL.SERVER-FAILURE.in-addr.arpa" or line[2] == "FAIL.NON-AUTHORITATIVE.in-addr.arpa":
                continue
            else:
                dns[line[1]] = line[2]

    with open(directory + args.traceroute_file, 'rb') as f:

        traceroute_list = []
        while True:
            record = warts.parse_record(f)
            if record == None:
                break
            if isinstance(record, Traceroute):
                if record.src_address:
                    if record.src_address in dns:
                        traceroute_list.append(record.src_address + ":" +dns[record.src_address])
                    else:
                        traceroute_list.append(record.src_address)
                
                for h in record.hops:
                    if h.address in dns:
                        traceroute_list.append(h.address + ":" + dns[h.address])
                    else:
                        traceroute_list.append(h.address)

                if record.dst_address:
                    if record.dst_address in dns:
                        traceroute_list.append(record.dst_address + ":" + dns[record.dst_address])
                    else:
                        traceroute_list.append(record.dst_address)
                traceroute.append(traceroute_list)



