import argparse
import re
import warts
from warts.traceroute import Traceroute

dns = {} 

def main():
    global dns
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
        print("The file type of traceroute file should be .warts")
    elif not re_txt.search(args.dns_file):
        print("The file type of the dns file     should be .txt")
    elif re_ipv4_traceroute.search(args.traceroute_file) and re_ipv6_dns.search(args.dns_file):
        print("Parsing Ipv4 traceroute file should use Ipv4 DNS file")
    elif re_ipv6_traceroute.search(args.traceroute_file) and re_ipv4_dns.search(args.dns_file):
        print("Parsing Ipv6 traceroute file should use Ipv6 DNS file") 
    else:

        traceroute = []
        

        # reading DNS file
        with open(directory + args.dns_file) as f:
            for line in f:
                line = line.split()
                if len(line)==2: # no hostname
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
                    ips, hostnames = parse_trace(record, True)
                    print(ips)
                    print(hostnames)
                    input("press")
                    

                    # p = True
                    # for i in hostnames:
                    #     if len(i)!=0:
                    #         p = False
                    #         break
                    # if not p:
                    #     print(ips)
                    #     print(hostnames)
                    #     input("press to continue")




def parse_trace(trace, single_IP=False):
    global dns
    ips = []
    hostnames = []

    if trace.src_address:
        ips.append(trace.src_address)
        if trace.src_address in dns:
            hostnames.append(dns[trace.src_address])
        else:
            hostnames.append(None)

    for h in trace.hops:
        if single_IP:
            if len(h.address.split(','))>=2:
                ips.append(None)
                hostnames.append(None)
                input("There are at least two ip addresses in a hop")
            else: # sinle ip in a hop
                ips.append(list(h.address))
                if h.address in dns:
                    hostnames.append()
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

    if trace.dst_address:
        ips.append(trace.dst_address)
        if trace.dst_address in dns:
            hostnames.append(dns[trace.dst_address])
        else:
            hostnames.append(None)
    
    return ips, hostnames

if __name__ == '__main__':
    main()


