################################## Imports #####################################
import argparse
import json
import re
# import pyasn
import sys
# import gzip

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
    # parser.add_argument("-p", type=str, default=None, dest="prefix_2_as6_file", help="Path to a .prefix2as6 file.")
    # parser.add_argument("-d", type=str, default=None, dest="dat_file", help="Name for .dat file used for ipv6 prefix to AS mapping.")
    args = parser.parse_args()

     # Exit if missing the sc_to_json_file.
    if args.sc_to_json_file is None:
        print("sc_to_json_file not found")
        print(sys.argv[0],"-t sc_to_json")
        sys.exit()
    """
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
    """ 
    sc_to_json_file = args.sc_to_json_file
    # prefix_2_as6_file = args.prefix_2_as6_file

    # Create list of ipv6 addresses
    ark_ip_topology(sc_to_json_file)

    # Create a .dat file and pyasn object from the prefix_2_as6_file
    # create_asn_db()

    # Create list of asns
    # create_asns()

############################### Helper Methods #################################

def ark_ip_topology(sc_to_json_file):
    '''
    Parse JSON object and create a docummented output of an ark trace. 
    '''
    
    data = []
    for line in open(sc_to_json_file, 'r'):
        data.append(json.loads(line))
    
    for elem in data[1:5]:
        print 'traceroute from %s, ' % (elem['src'])
    
    
    
    
    
    
    """
    for elem in data[1:2]:
        print('   {')
        print('\t\'version\' : \'{}\' | # warts version'.format(elem['version']))
        print('\t\'type\' : \'{}\' | # warts trace file'.format(elem['type']))
        print('\t\'userid\' : \'{}\' | # user id (unset)'.format(elem['userid']))
        print('\t\'method\' : \'{}\' | # method to collect the data\n'.format(elem['method']))
        
        print('\t\'src\' : \'{}\' | # source: IP address of measurement box'.format(elem['src']))
        print('\t\'dst\' : \'{}\' | # destination: IP address of the target of trace'.format(elem['dst']))
        print('\t\'icmp_sum\' : \'{}\' | # UPDATE'.format(elem['icmp_sum']))
        print('\t\'stop_reason\' : \'{}\' | # UPDATE'.format(elem['stop_reason']))
        print('\t\'stop_data\' : \'{}\' | # UPDATE'.format(elem['stop_data']))
        print('\t\'start\' : {')
        for key, value in elem['start'].items():
            # print(key, ':', value)
            print('\t\t\'{}\' : \'{}\' | # UPDATE'.format(key,value))
        print('\t\t},')    
        print('\t\'hop_count\' : \'{}\' | # UPDATE'.format(elem['hop_count']))
        print('\t\'attempts\' : \'{}\' | # UPDATE'.format(elem['attempts']))
        print('\t\'firsthop\' : \'{}\' | # UPDATE'.format(elem['firsthop']))
        print('\t\'wait\' : \'{}\' | # UPDATE'.format(elem['wait']))
        print('\t\'wait_probe\' : \'{}\' | # UPDATE'.format(elem['wait_probe']))
        print('\t\'tos\' : \'{}\' | # UPDATE'.format(elem['tos']))
        print('\t\'probe_size\' : \'{}\' | # UPDATE'.format(elem['probe_size']))
        print('\t\'hops\' : {')
        #for hop in elem['hops']:
            # print('\t\'addr\' : \'{}\' | # UPDATE'.format(hop['addr']))
                        
        print('   }')
    """
main()