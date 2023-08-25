#!  /usr/bin/env python3
import sys
import os
import json

parent_dir = os.path.dirname(os.path.realpath(__file__))+"/../lib"
sys.path.append(parent_dir)
import utils

fname = sys.argv[1]
print (fname)
print (json.dumps(utils.parse_markdown(fname), indent=4))
