import argparse
import warts
from warts.traceroute import Traceroute

import psutil # memory statistic

directory = "../../../../dataset/" #add file name behind

parser = argparse.ArgumentParser()
# ark warts dataset

ipv4_warts = ""
ipb4_ip2hostname = ""
ipv6_warts = "topo-v6.l8.20190101.1546305192.ams2-nl.warts"
ipb6_ip2hostname = "dns-names.l8.20190101.txt"

parser.add_argument("-w", dest = "warts_file", default = ipv6_warts, help = "Please enter the file name of warts file")
parser.add_argument("-i", dest= "ip2hostname_file", default = ipb6_ip2hostname, help = "Please enter the file name of ip2hostname file") 
args = parser.parse_args()
count = 0

# src_prefix = set()
# dst_prefix = set()
# src_24 = set()
# dst_24 = set()
# # === open ipv3_prefix_probing_dataset


# print("Reading ipv4_prefix_probing_dataset.warts...\n")
# with open(directory + args.warts_file, 'rb') as f:
    
#     # print(record)
#     # while not isinstance(record, Traceroute):
#     #     record = warts.parse_record(f)
#     # if record.src_address:
#     #     print("Traceroute source address:", record.src_address)
#     # if record.dst_address:
#     #     print("Traceroute destination address:", record.dst_address)
#     # print("Number of hops:", len(record.hops))
#     # print(record.hops)
#     while True:
        
#         record = warts.parse_record(f)
#         if record == None:
#             break

#         if isinstance(record, Traceroute):
#             count += 1
#             if record.src_address:
#                 print("Traceroute source address:", record.src_address)
#                 # src_prefix.add(record.src_address)
#             if record.dst_address:
#                 print("Traceroute destination address:", record.dst_address)
#                 # dst_prefix.add(record.dst_address)
#             # for h in record.hops:
#             print("Traceroute hops:", record.hops, '\n')
#         if count > 100:
#             break

# print("\n\n\n\nsrc count: ", len(src_prefix))
# print("dst count: ", len(dst_prefix))
# print("total count: ", count)
# print("\n\n\nReading ipv4_routed_24_ropology_dataset.warts...\n")
# count = 0
# count_24 = 0
# duplicate_dst = {}

# with open(directory+"ipv4_routed_24_ropology_dataset.warts", 'rb') as f:
#     while True:
        
#         record = warts.parse_record(f)
#         if record == None:
#             break

#         if isinstance(record, Traceroute):
#             count += 1
#             if record.src_address:
#                 # print("Traceroute source address:", record.src_address)
#                 src_24.add(record.src_address)
#                 # if record.src_address in src:
#                 #     print(record.src_address + " is in src")
#                 #     input("press anything to continue")
#             if record.dst_address:
#                 # print("Traceroute destination address:", record.dst_address)
#                 dst_24.add(record.dst_address)
#                 if record.dst_address in dst_prefix:

#                     # print(record.dst_address + " is in dst_prefix")
#                     # input("press anything to continue")
#                     count_24 += 1

#                     duplicate_dst[record.dst_address] = record.hops


#             # print("Traceroute hops:", record.hops , "\n")
# print("\n\n\n\nsrc count: ", len(src_24))
# print("dst count: ", len(dst_24))
# print("dst24 in dst_prefix:", count_24)
# print("total count: ", count)
# count = 0



# print("Reading ipv4_prefix_probing_dataset.warts...\n")
# with open(directory+"ipv4_prefix_probing_dataset.warts", 'rb') as f:
    
#     # print(record)
#     # while not isinstance(record, Traceroute):
#     #     record = warts.parse_record(f)
#     # if record.src_address:
#     #     print("Traceroute source address:", record.src_address)
#     # if record.dst_address:
#     #     print("Traceroute destination address:", record.dst_address)
#     # print("Number of hops:", len(record.hops))
#     # print(record.hops)
#     while True:
        
#         record = warts.parse_record(f)
#         if record == None:
#             break

#         if isinstance(record, Traceroute):
#             count += 1
#             if record.dst_address:
#                 # print("Traceroute destination address:", record.dst_address)
#                 if record.dst_address in duplicate_dst:

#                     if len(record.hops) != len(duplicate_dst[record.dst_address]):
#                         print("\n\n\ndestination:", record.dst_address)
#                         print("hops in prefix_ptobing:\n", record.hops)
#                         print("hops in 24:\n", duplicate_dst[record.dst_address])
                        
#                     else:
#                         for i in range(len(record.hops)):

#                             if record.hops[i].address != duplicate_dst[record.dst_address][i].address:
#                                 print("\n\n\ndestination:", record.dst_address)
#                                 print("hops in prefix_ptobing:\n", record.hops)
#                                 print("hops in 24:\n", duplicate_dst[record.dst_address])
#                                 break



# print("\n\n\n\nduplicate destination: ", duplicate_dst)
# print("\n\n\n\nduplicate destination: ", duplicate_dst_in_prefix)



# [source: hostname, hops in order, destination]


# parse ip2hostname file
ip2hostname = {}
duplicate_check = {}

count = 0
print("\n\n\nReading DNS IPv4...\n\n")
count = 0
with open(directory + args.ip2hostname_file) as f:
    for line in f:
        line = line.split()
        if len(line)==2:
            continue
        elif line[2] == "FAIL.SERVER-FAILURE.in-addr.arpa" or line[2] == "FAIL.NON-AUTHORITATIVE.in-addr.arpa":
            continue
        elif line[1] in duplicate_check:
            print("Found duplicate ip2hostname:\n", line[1], " ", line[2])
            print(duplicate_check[line[1]])
            input("press to continue")
        else:
            duplicate_check[line[1]] = line[2]
            ip2hostname[line[1]] = line[2]

        # print(line)
        count += 1
print(count)
input("press to continue")

src_prefix = set()
dst_prefix = set()
src_24 = set()
dst_24 = set()
count = 0
# === open ipv3_prefix_probing_dataset

traceroute = []
print("Reading ipv4_prefix_probing_dataset.warts...\n")

with open(directory + args.warts_file, 'rb') as f:

    traceroute_list = []
    while True:
        status = psutil.virtual_memory().percent
        record = warts.parse_record(f)
        if record == None:
            break

        if isinstance(record, Traceroute):
            count += 1
            if record.src_address:
                # print("Traceroute source address:", record.src_address)
                src_prefix.add(record.src_address)
                if record.src_address in ip2hostname:
                    traceroute_list.append(record.src_address + ":" +ip2hostname[record.src_address])
                    # print(traceroute_list)
                    # input("Found src in ip2hostname, press to continue")
                else:
                    traceroute_list.append(record.src_address)
            
            for h in record.hops:
                if h.address in ip2hostname:
                    traceroute_list.append(h.address + ":" + ip2hostname[h.address])
                    # print(traceroute_list)
                    # input("Found hops in ip2hostname, press to continue")
                else:
                    traceroute_list.append(h.address)

            if record.dst_address:
                # print("Traceroute destination address:", record.dst_address)
                if record.dst_address in ip2hostname:
                    traceroute_list.append(record.dst_address + ":" + ip2hostname[record.dst_address])
                    # print(traceroute_list)
                    # input("Found dest in ip2hostname, press to continue")
                else:
                    traceroute_list.append(record.dst_address)
                #     print("destination: ", record.dst_address)
        
        # print(traceroute_list)
        # print("\n\n")
            traceroute.append(traceroute_list)
            #     print("Traceroute hops:", h.address, '\n')

            if count % 1000 == 0:
                # break
                print(int(count*100/132539), "% ", status) 
        #     break
        # if count > 10:
        #     break
print(count)
print(len(traceroute))

# print("\n\n\nReading DNS IPv6...\n\n")
# count = 0
# with open(directory+"dns-names.l8.20190101.txt") as f:
#     for line in f:
#         count += 1
#         print(str(count) + " " + line)
#         if count > 10:
#             break



