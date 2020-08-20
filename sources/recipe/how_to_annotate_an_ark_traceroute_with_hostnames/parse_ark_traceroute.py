import argparse
import re
import warts
from warts.traceroute import Traceroute

dns = {} 


def main():
    global dns
    parser = argparse.ArgumentParser()
    parser.add_argument("-t", type=str, dest="traceroute_file", default=None, help="Please enter the file name of traceroute file")
    parser.add_argument("-d", type=str, dest="dns_file", default=None, help="Please enter the file name of dns file") 

    args = parser.parse_args()

    re_warts = re.compile(r".warts$")
    re_txt = re.compile(r".txt$")
    re_ipv4_traceroute = re.compile(r"team-probing")
    re_ipv6_traceroute = re.compile(r"topo-v6.l8")
    re_ipv4_dns = re.compile(r"dns-names.l7")
    re_ipv6_dns = re.compile(r"dns-names.l8")
    if not re_warts.search(args.traceroute_file):
        print("The file type of traceroute file should be .warts")
    elif not re_txt.search(args.dns_file):
        print("The file type of the dns file should be .txt")
    elif re_ipv4_traceroute.search(args.traceroute_file) and re_ipv6_dns.search(args.dns_file):
        print("Parsing Ipv4 traceroute file should use Ipv4 DNS file")
    elif re_ipv6_traceroute.search(args.traceroute_file) and re_ipv4_dns.search(args.dns_file):
        print("Parsing Ipv6 traceroute file should use Ipv6 DNS file") 
    else:

        # reading DNS file       
        load_dns_file(args.dns_file)

        # load .wart file 
        with open(args.traceroute_file, 'rb') as f:
            traceroute_list = []
            while True:
                record = warts.parse_record(f)
                if record == None:
                    break
                if isinstance(record, Traceroute):
                    ips, hostnames = parse_trace(record, True)
                    # print(ips)
                    # print(hostnames)


def load_dns_file(dns_file):
    global dns
    with open(dns_file) as f:
                for line in f:
                    line = line.split()
                    if len(line) == 2: # missing hostname
                        continue
                    elif line[2] == "FAIL.SERVER-FAILURE.in-addr.arpa" or line[2] == "FAIL.NON-AUTHORITATIVE.in-addr.arpa":
                        continue
                    else:
                        dns[line[1]] = line[2]

def parse_trace(trace, single_IP=False):
    global dns
    ips = []
    hostnames = []

    # source
    if trace.src_address:
        ips.append(trace.src_address)
        if trace.src_address in dns:
            hostnames.append(dns[trace.src_address])
        else:
            hostnames.append(None)
    # hops
    for h in trace.hops:
        if single_IP:
            if len(h.address.split(',')) >= 2:
                ips.append(None)
                hostnames.append(None)

            else: # sinle ip in a hop
                ips.append(h.address)

                if h.address in dns:
                    hostnames.append(dns[h.address])
                else:
                    hostnames.append(None)

        else: # support multiple ips
            hop_hostnames = []
            hop_ips = h.address.split(',')
            ips.append(hop_ips)
            for ip in hop_ips:
                if ip in dns:
                    hop_hostnames.append(dns[ip])
                else:
                    hop_hostnames.append(None)
            hostnames.append(hop_hostnames)

    # destination
    if trace.dst_address:
        ips.append(trace.dst_address)
        if trace.dst_address in dns:
            hostnames.append(dns[trace.dst_address])
        else:
            hostnames.append(None)
    
    return ips, hostnames

if __name__ == '__main__':
    main()


