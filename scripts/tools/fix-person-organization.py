#!  /usr/bin/env python3 
import sys
import re
re_org = re.compile('"organization"')
for fname in sys.argv[1:]:
    found = False
    lines = []
    with open(fname) as fin:
        for line in fin:
            if re_org.search(line):
                found = True
                line = line.replace("organization","organizations")
            lines.append(line)

    if found:
        print (fname)
        with open(fname, "w") as fout:
            for line in lines:
                fout.write(line)

            
