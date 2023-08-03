#! /usr/bin/env python3

import json, glob

def main():
    for filepath in glob.glob('./sources/*/*.json'):
        with open(filepath, 'r') as file:
            obj = json.load(file)

        if not 'access' in obj:
            continue
            
        for access in obj['access']:
            if not 'tags' in access or 'type' in access:
                continue
            access['type'] = access['tags'][0]
            access['tags'] = access['tags'][1:]
            if len(access['tags']) == 0:
                del access['tags']


        with open(filepath, 'w') as file:
            json.dump(obj, file, indent=4)
            file.write('\n')
            
main()