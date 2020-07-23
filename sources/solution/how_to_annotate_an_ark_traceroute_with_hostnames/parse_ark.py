import warts
from warts.traceroute import Traceroute

directory = "../../../../dataset/" #add file name behind

count = 0


# === open ipv3_prefix_probing_dataset


print("Reading ipv4_prefix_probing_dataset.warts...")
with open(directory+"ipv4_prefix_probing_dataset.warts", 'rb') as f:
    
    # print(record)
    # while not isinstance(record, Traceroute):
    #     record = warts.parse_record(f)
    # if record.src_address:
    #     print("Traceroute source address:", record.src_address)
    # if record.dst_address:
    #     print("Traceroute destination address:", record.dst_address)
    # print("Number of hops:", len(record.hops))
    # print(record.hops)
    while True:
        count += 1
        record = warts.parse_record(f)
        if record == None or count > 10:
            break

        if isinstance(record, Traceroute):
            if record.src_address:
                print("Traceroute source address:", record.src_address)
            if record.dst_address:
                print("Traceroute destination address:", record.dst_address)
            print("Traceroute hops:", record.hops)

print("\n\nReading ipv4_routed_24_ropology_dataset.warts...")
count = 0
with open(directory+"ipv4_routed_24_ropology_dataset.warts", 'rb') as f:
    while True:
        count += 1
        record = warts.parse_record(f)
        if record == None or count > 10:
            break

        if isinstance(record, Traceroute):
            if record.src_address:
                print("Traceroute source address:", record.src_address)
            if record.dst_address:
                print("Traceroute destination address:", record.dst_address)
            print("Traceroute hops:", record.hops)

count = 0

# DNS ipv4
print("\n\nReading DNS IPv4...")
count = 0
with open(directory+"dns-names.l7.20190111.txt") as f:
    for line in f:
        count += 1
        print(line)
        if count > 10:
            break


print("\n\nReading DNS IPv46...")
count = 0
with open(directory+"dns-names.l8.20190101.txt") as f:
    for line in f:
        count += 1
        print(line)
        if count > 10:
            break



