################################## Imports #####################################
import argparse
import json
import re
import pyasn
import sys

############################## Global Variables ################################

re_multi_origin = re.compile(r"\w+[_]\d+$")

ips  = []
asns = []
asn_db = None

# Files/Filesets
dat_file = None
prefix_2_as6_file = None

################################# Main Method ##################################
def main():
    global re_multi_origin
    global asn_db 
    global ips
    global dat_file
    global prefix_2_as6_file

    parser = argparse.ArgumentParser()
    parser.add_argument("-t", type= str, default=None, dest= "sc_to_json_file", help="Path to a .json file.")
    parser.add_argument("-p", type=str, default=None, dest="prefix_2_as6_file", help="Path to a .prefix2as6 file.")
    parser.add_argument("-d", type=str, default=None, dest="dat_file", help="Name for .dat file used for ipv6 prefix to AS mapping.")
    args = parser.parse_args()

     # Exit if missing the sc_to_json_file.
    if args.sc_to_json_file is None:
        print("sc_to_json_file not found")
        print(sys.argv[0],"-t sc_to_json")
        sys.exit()

    # Exit if missing the prefix_2_as6_file.
    if args.prefix_2_as6_file is None:
        print("prefix_2_as6_file not found")
        print(sys.argv[0],"-p prefix_2_as6_file")
        sys.exit()
    

    # Edge Case: Create a default name for dat_file if none is given.
    if args.dat_file is None or not re.search(r".dat$", args.dat_file):
        dat_file = "ipv6_prefix_2_as.dat"
    else:
        dat_file = args.dat_file
    
    sc_to_json_file = args.sc_to_json_file
    prefix_2_as6_file = args.prefix_2_as6_file

    # Create list of ipv6 addresses
    create_ips(sc_to_json_file)

    # Create a .dat file and pyasn object from the prefix_2_as6_file
    create_asn_db()

    # Create list of asns
    create_asns()

############################### Helper Methods #################################

def create_ips(sc_to_json_file):
    '''
    Parse JSON object and create list of ip addresses. 
    '''
    global ips

    data = []
    for line in open(sc_to_json_file, 'r'):
        data.append(json.loads(line)) 

    for elem in data:
        ips.append(elem['src'])
        hops = elem["hops"]
        for hop in hops:
            ips.append(hop["addr"])
        ips.append(elem['dst'])
    # print(ips)

def create_asn_db_body(curr_line):
    '''
    Parse the given line and either return formatted line or None.
    '''
    if not re_multi_origin.search(curr_line):
        # curr_line Format:     <prefix>\t<length>\t<as> 
        # curr_data Format:     [ <prefix>, <length>, <as> ]
        # return Format:        <prefix>/<length>\t<as>\n
        curr_data = curr_line.split()
        return curr_data[0] + "/" + curr_data[1] + "\t" + curr_data[2] + "\n"
    # Edge Case: Return None if curr_line is neither BGP or necessary data.
    else:
        return None


def create_asn_db():
    '''
    Update asn_db with a pyasn object created from prefix_2_as6_file. 
    '''
    global asn_db

    with open(dat_file, "w") as out_file:
        with open(prefix_2_as6_file, "r") as in_file:
            # Iterate over lines in in_file and write/format them to out_file
            curr_line = in_file.readline()
            while curr_line:
                # curr_line = curr_line.decode()
                parsed_line = create_asn_db_body(curr_line)
                # Only write to out_file if parsed_line was necessary data.
                if parsed_line is not None:
                    out_file.write(parsed_line)
                curr_line = in_file.readline()

    # Create the asn_db with the dat_file that was just created.
    try:
        asn_db = pyasn.pyasn(dat_file)
    except ValueError as error:
        print("dat_file was not able to be made with given .prefix2as6 file")
        print(str(error))

def create_asns():
    '''
     Create list of asns from pyasn lookup
    '''
    global ips
    global asn_db 

    asns = []
    for ip in ips:
        try:
            asn, prefix = asn_db.lookup(ip)
        except ValueError:
            print("No corresponding asn for ", ip)
        asns.append(asn)
    # print(asns)

main()
