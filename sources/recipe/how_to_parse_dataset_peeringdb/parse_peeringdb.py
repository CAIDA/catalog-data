import argparse
import sqlite3
import json


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-s", dest='dataset', type=str, default="peeringdb_dump_2016_01_01.sql", help="")
    parser.add_argument("-j", dest='json_dataset', type=str, default= "peeringdb_2_dump_2020_01_01.json")
    args = parser.parse_args()


    with open(args.json_dataset) as f:
        data = json.load(f)

    print(data.keys())
    # print(data['ix']['data'][0])
    # print("\n\n")
    # print(data['ix']['data'][1])
    # print(len(data['ix']['data']))
    # print(len(data['ix']))

    # print("Initial sqlit3")
    # connection = sqlite3.connect(":memory:") 
    # cursor = connection.cursor()

    # sql_file = open(args.dataset)
    # read_line = sql_file.read()
    # cursor.executescript(read_line)

    # for r in cursor.execute("SELECT * FROM mgmtFacilities"):
    #     print(r)
def get_fac():
    pass
def get_single_fac():
    pass
def get_ix():
    pass
def get_single_ix():
    pass
def get_ixfac():
    pass
def get_single_ixfac():
    pass
def get_ixlan():
    pass
def get_ixpfx():
    pass
def get_net():
    pass
def get_single_net():
    pass
def get_org():
    pass
def get_single_org():
    pass
def 


'ix', 'ixfac', 'net', 'ixlan', 'as_set', 'api', , 'netfac', 'org', 'ixpfx', 'netixlan', 'poc'])
if __name__ == '__main__':
    main()