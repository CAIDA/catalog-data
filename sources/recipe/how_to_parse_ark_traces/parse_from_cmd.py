import warts
import sys
import argparse
from warts.traceroute import Traceroute

parser = argparse.ArgumentParser()
parser.add_argument("-f", type= str, default=None, dest= "warts_file", help="Path to a .warts file.")
args = parser.parse_args()

if args.warts_file is None:
        print("warts_file not found")
        print(sys.argv[0],"-f warts_file")
        sys.exit()
        
warts_file = args.warts_file

with open(warts_file, 'rb') as f:
    while True:
        record = warts.parse_record(f)
        if record == None:
            break
        print('\n')
        print(record)
        if isinstance(record, Traceroute):
            for hop in record.hops:
                print(hop)
            print('\n')