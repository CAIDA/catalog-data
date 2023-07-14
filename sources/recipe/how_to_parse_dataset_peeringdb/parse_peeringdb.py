# Copyright (c) 2020 The Regents of the University of California
# All Rights Reserved

import argparse
import sqlite3
import json


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', dest='dataset', default=None, help='Input dataset filename.')
    parser.add_argument('-get', dest='type', type=str, help='Input what kind of object you would like to get.')
    parser.add_argument('-id', dest='single_id', type=int, help='Input the id of single object you would like to get.')
    args = parser.parse_args()

    if args.dataset.endswith('.json') and args.type and not args.single_id:
        print(get_object(args.dataset, args.type))
    elif args.dataset.endswith('.json') and args.type and args.single_id:
        print(get_single_object(args.dataset, args.type, args.single_id))

    elif args.dataset.endswith('.sqlite') and args.type and not args.single_id:
        print(get_sqlite_object(args.dataset, args.type)) 

    elif args.dataset.endswith('.sqlite') and args.type and args.single_id:
        print(get_sqlite_single_object(args.dataset, args.type, args.single_id))


def get_json_data(filename):
    with open(filename) as f:
        data = json.load(f)
    return data

def get_object(filename, type):
    data = get_json_data(filename)
    return data[type]['data']

def get_single_object(filename, type, target_id):
    data = get_json_data(filename)
    for item in data[type]['data']:
        if item['id'] == target_id:
            return item

def get_sqlite_object(filename, type):
    connection = sqlite3.connect(filename)
    cursor = connection.cursor()

    # The result of a "cursor.execute" can be iterated over by row
    data = cursor.execute('SELECT * FROM ' + type + ';')
    names = [description[0] for description in cursor.description]
    obj = []
    for row in data:
        single_obj = {}
        for i in range(len(names)):
            single_obj[names[i]] = row[i]
        obj.append(single_obj)

    # Be sure to close the connection
    connection.close()
    return obj

def get_sqlite_single_object(filename, type, target_id):
    connection = sqlite3.connect(filename)
    cursor = connection.cursor()

    # The result of a "cursor.execute" can be iterated over by row
    data = cursor.execute('SELECT * FROM ' + type + ';')
    names = [description[0] for description in cursor.description]
    for row in data:
        if row[0] == target_id:
            single_obj = {}
            for i in range(len(names)):
                single_obj[names[i]] = row[i]
            connection.close()
            return single_obj

if __name__ == '__main__':
    main()