import json
import argparse

def findIndex(ip, ixs):
    for i in range(0, len(ixs)):
        for x in ixs[i]['prefixes']['ipv4']:
            if ip == x.split('/')[0]:
                return i
def exportCSV(ips, ixs):
    data = "ip,ixID,ixName\n"
    for ip in ips:
        if findIndex(ip, ixs) is not None:
            data += str(ip)
            data += ','
            data += str(ixs[findIndex(ip, ixs)]['ix_id'])
            data += ','
            data += str(ixs[findIndex(ip, ixs)]['name'])
            data += '\n'
    file = open(args.ixp_list, "w")
    file.write(data)
def printIXs(ips, ixs):
    for ip in ips:
        if findIndex(ip, ixs) is not None:
            print(ip, "|", ixs[findIndex(ip, ixs)]['ix_id'], "|", ixs[findIndex(ip, ixs)]['name'])


parser = argparse.ArgumentParser()
parser.add_argument('-i', '--in', dest='ip_list', type=str, required=True, help="Path to IP list.")
parser.add_argument('-o', '--out', dest='ixp_list', type=str, required=False, help="Path to save as CSV.")
parser.add_argument('-ix', dest='ix_file', type=str, required=True, help="Path to IXP data.")
args = parser.parse_args()

#Open ixp jsonl and convert into dictionary entries:
def parseJSONL(ixpJSONL):
    ixs = {}
    index = 0
    #Test if file exists.
    try:
        open(ixpJSONL)
    except:
        print("Failed to open file:", ixpJSONL)
        return

    #Reads every line in JSONL file.
    for line in open(ixpJSONL):
        #Add dictionary index if line is not a comment.
        if line[0] != '#':
            ixs[index] = json.loads(line)
            index += 1
    #Return completed dictionary
    return ixs

#Make IP file into a list of IPs:
def parseIPs(ipFile):
    try:
        open(ipFile)
    except:
        print("Failed to open file:", ipFile)
        return

    ips = []
    for line in open(args.ip_list):
        ips.append(line.rstrip('\n\r'))
    return ips


ixs = parseJSONL(args.ix_file)
ips = parseIPs(args.ip_list)

#If -o argument is selected export to CSV with selected name and print values to terminal:
ip_ixs = {}
if args.ixp_list is not None:
    exportCSV(ips, ixs)

    for ip in ips:
        ip_ixs[ip] = {
            'ip' : ip,
            'name' : ixs[findIndex(ip, ixs)]['name'],
            'ix_id' : ixs[findIndex(ip, ixs)]['ix_id']
        }

#If -o argument is not selected only print values to terminal:
if args.ixp_list is None:
    for ip in ips:
        ip_ixs[ip] = {
            'ip' : ip,
            'name' : ixs[findIndex(ip, ixs)]['name'],
            'ix_id' : ixs[findIndex(ip, ixs)]['ix_id']
        }
    printIXs(ips, ixs)
