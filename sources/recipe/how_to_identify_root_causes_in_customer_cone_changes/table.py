# Copyright (C) 2023 The Regents of the University of
# California. All Rights Reserved.

import bz2
import os
import argparse
import time

######################################################################
## Parameters
######################################################################

parser = argparse.ArgumentParser()
parser.add_argument("-dir", dest='dir_name', help="name of directory where all data files are", type=str)
parser.add_argument("-d1", dest='date_1', help="first date, format: YYYYMMDD", type=int)
parser.add_argument("-d2", dest='date_2', help="second date, format: YYYYMMDD", type=int)
parser.add_argument("-t", dest='target', help="target AS, as int", type=int, required=True)
parser.add_argument("-g", dest='gained', help="examine gained ASes (default: lost)", action="store_true")
args = parser.parse_args()


if args.target is None:
    raise  Exception("Missing target. Specify target with -t")

if args.dir_name is None or args.date_1 is None or args.date_2 is None:
    raise Exception("Specify an initial date with -d1 YYYYMMDD, a later date with -f2 YYYYMMDD, and a directory with -dir")
else:
    RELS1 = os.path.normpath("{}/{}.as-rel.txt.bz2".format(DIRECTORY, args.date_1))
    RELS2 = os.path.normpath("{}/{}.as-rel.txt.bz2".format(DIRECTORY, args.date_2))
    CONES1 = os.path.normpath("{}/{}.ppdc-ases.txt.bz2".format(DIRECTORY, args.date_1))
    CONES2 = os.path.normpath("{}/{}.ppdc-ases.txt.bz2".format(DIRECTORY, args.date_2))
    PATHS1 = os.path.normpath("{}/{}.paths.bz2".format(DIRECTORY, args.date_1))
    PATHS2 = os.path.normpath("{}/{}.paths.bz2".format(DIRECTORY, args.date_2))

TARGET = args.target
GAINED = args.gained

if GAINED:
    word = 'gained'
    sm_paths = PATHS1
    lg_paths = PATHS2
    sm_cones = CONES1
    lg_cones = CONES2
    sm_rels = RELS1
    lg_rels = RELS2
else:
    word = 'lost'
    sm_paths = PATHS2
    lg_paths = PATHS1
    sm_cones = CONES2
    lg_cones = CONES1
    sm_rels = RELS2
    lg_rels = RELS1

# Get a specific cone from a ppdc-ases file
def get_cone(filename, target):
    cone = set()
    ts = str(target)
    with bz2.open(filename, 'r') as cfile:
        for line in cfile:
            line = line.decode('utf-8')
            if line[:line.index(' ')] == ts:
                for asn in line[line.index(' ')+1:].split(' '):
                    cone.add(int(asn))
                return cone

print('Getting cones')

# Obtain the target's cones at both points in time
cone_sm = get_cone(sm_cones, TARGET)
cone_lg = get_cone(lg_cones, TARGET)

# Find the set difference
changed = cone_lg.copy()
for asn in cone_sm:
    changed.discard(asn)



# Given a paths file and an as-rel file, output paths annotated with relationship info
def annotate_paths(pathsfile, relsfile):

    # Make a dict that contains relationship information
    relsdict = {}
    with bz2.open(relsfile, 'r') as f:
        for line in f:
            line = line.decode('utf-8')
            # skip all lines that begin with '#'
            if line[0] == '#':
                continue

            # each line represents one relationship
            # store the relationship in a dict so it can be accessed quickly
            clsplit = line.split('|')
            for i in range(3):
                clsplit[i] = int(clsplit[i])
            if not clsplit[0] in relsdict:
                relsdict[clsplit[0]] = { clsplit[1]: clsplit[2] }
            else:
                relsdict[clsplit[0]][clsplit[1]] = clsplit[2]

    # Iterate through the paths file and annotate each path
    annotated_paths = []
    with bz2.open(pathsfile, 'r') as file:
        for current_line in file:
            current_line = current_line.decode()

            # Skip lines beginning with #
            if current_line[0] == '#':
                continue
            clsplit = current_line.split('|')

            # Convert ASNs to ints
            for i in range(len(clsplit)):
                clsplit[i] = int(clsplit[i])
            
            # Iterate through the path, annotating with relationships
            annotate = [clsplit[0]]
            for i in range(1, len(clsplit)):
                if clsplit[i-1] in relsdict and clsplit[i] in relsdict[clsplit[i-1]]:
                    if relsdict[clsplit[i-1]][clsplit[i]] == -1:
                        annotate.append('<')
                    elif relsdict[clsplit[i-1]][clsplit[i]] == 0:
                        annotate.append('-')
                    else:
                        annotate.append('>')
                else:
                    if clsplit[i] in relsdict:
                        if not clsplit[i-1] in relsdict[clsplit[i]]:
                            annotate.extend(['?', clsplit[i]])
                            continue
                        if relsdict[clsplit[i]][clsplit[i-1]] == -1:
                            annotate.append('>')
                        elif relsdict[clsplit[i]][clsplit[i-1]] == 0:
                            annotate.append('-')
                        else:
                            annotate.append('<')
                    else:
                        annotate.append('?')
                annotate.append(clsplit[i])
            annotated_paths.append(annotate)

    return annotated_paths

# Process the given paths, cropping them based on relationships
def crop_paths(annotated_paths):
    cropped_paths = []
    for path in annotated_paths:
        new_path = []
        if '<' in path:

            # If the first < relationship is preceded by -, include it
            if path[path.index('<') - 2] == '-':
                new_path = path[(path.index('<') - 1):]

            # Otherwise, exclude it
            else:
                new_path = path[(path.index('<') + 1):]
        
        # If path doesn't have <, skip it
        else:
            continue

        # Cropped paths should consist of only < relationships,
        # so paths with - or > should be split up
        if not ('-' in new_path or '>' in new_path):
            cropped_paths.append(new_path[::2])
        else:
            to_add_outer = []
            to_add_inner = []
            for elt in new_path:
                if type(elt) == int:
                    to_add_inner.append(elt)
                else:
                    if elt == '-' or elt == '>':
                        if len(to_add_inner) > 1:
                            to_add_outer.append(to_add_inner)
                        to_add_inner = []
            cropped_paths.extend(to_add_outer)
    return cropped_paths

# Generate a data structure using cropped paths that indicates how ASes access other ASes
def get_conduits(cpaths):
    conduits = {}
    for path in cpaths:

        # Loop through the path
        for i in range(len(path) - 1):

            # the current ASN is considered as a provider, and is a key in the (parent) dict
            # its value is a dict corresponding to it, i.e. a child dict
            current = path[i]
            if not current in conduits:
                conduits[current] = {}

            # the current ASN's direct customer is the conduit through which indirect customers pass
            conduit = path[i+1]

            # indirect customers get added as keys to the (child) dict corresponding to the provider
            for j in range(i+1, len(path)):
                sec = path[j]
                if not sec in conduits[current]:
                    conduits[current][sec] = set()
                
                # the conduit is added to a every set representing an indirect customer
                conduits[current][sec].add(conduit)
    return conduits

print('Processing paths (may take a while)')
annotated_paths_sm = annotate_paths(sm_paths, sm_rels)
conduits_sm = get_conduits(crop_paths(annotated_paths_sm))
annotated_paths_lg = annotate_paths(lg_paths, lg_rels)
conduits_lg = get_conduits(crop_paths(annotated_paths_lg))

# Given a target and an AS (the "secondary target") in its cone, try to find the "broken link" 
# i.e. why it stopped/started being included in the cone. Specifically, find the link that is
# in conduits_2 but not in conduits_1
def find_broken_links(sec, conduits_1, conduits_2):
    current = 0
    all_conduits = []
    link_stack = []

    # This algorithm attempts, using a depth-first search, to determine whether the 
    # appearance/disappearance of a link in the graph of ASes caused the secondary to be 
    # included/excluded from the cone of the target AS.

    # First, the conduits that gave the target access to the secondary are added to a stack
    for asn in conduits_2[TARGET][sec]:
        link_stack.append((TARGET, asn))
    
    # The BFS proceeds by iterating through the link stack
    while len(link_stack) != 0:

        # Pop the top link
        cur_link = link_stack.pop()
        current = cur_link[0]
        conduit = cur_link[1]

        # Add further links to the top of the stack
        if conduit != sec:
            for asn in conduits_2[conduit][sec]:
                link_stack.append((conduit, asn))

        # Check whether the current link is found in conduits_1. If it isn't, it's the broken link.
        if not (current in conduits_1 and conduit in conduits_1[current]):
            return 'link changed: {} < {}'.format(current, conduit)
        if not conduit in all_conduits: 
            all_conduits.append(conduit)
    
    # If all links in conduits_2 were also found in conduits_2, we instead look for a failure
    # to announce. The highest-level conduit that could've announced the secondary, but didn't,
    # is singled out.
    for asn in all_conduits:
        if asn in conduits_1[TARGET]:
            if sec in conduits_1[asn]:
                return 'failed to announce: {}'.format(asn)
        else:
            return 'indeterminate'

# Make a dict that holds every cause and how many ASes that cause was responsible for
causes = {}
# Another dict to summarize the causes
causes_summary = {'failed to announce': 0, 'link changed': 0, 'indeterminate': 0}
for asn in changed:
    cause = find_broken_links(asn, conduits_sm, conduits_lg)
    
    if cause[0] == 'f':
        causes_summary['failed to announce'] += 1
    elif cause[0] == 'l':
        causes_summary['link changed'] += 1
    else:
        causes_summary['indeterminate'] += 1
        
    if not cause in causes:
        causes[cause] = 0
    causes[cause] += 1

# Print the top 50 causes
print()
print('Results:')
n = 0
for cause, count in sorted(causes.items(), key=lambda r_c: r_c[1], reverse=True):
    print('{}, count: {}, percent of {}: {}%, percent of overall cone: {}%'.format(cause, count, word, str(100*count/len(changed))[:4], str(100*count/len(cone_lg))[:4]))
    n += 1
    if n > 50:
        break

# Print the summary of causes
print()
print('Summary of results:')
for cause, count in sorted(causes_summary.items(), key=lambda r_c: r_c[1], reverse=True):
    print('{}, count: {}, percent of {}: {}%, percent of overall cone: {}%'.format(cause, count, word, str(100*count/len(changed))[:5], str(100*count/len(cone_lg))[:5]))

print()
print('Processing paths in a different way...')
# Get a more inclusive cone by ignoring the rules for cropping paths
def get_inclusive_target_cone(annotated_paths):
    cone = set()
    for path in annotated_paths:
        if TARGET in path:
            for elt in path[path.index(TARGET) + 1:]:
                if elt == '>' or elt == '-' or elt == '?':
                    break
                if elt == '<':
                    continue
                cone.add(int(elt))
    return cone

# Find the intersection of the gained/lost ASNs and the ASNs in the inclusive cone
inclusive_targ_cone_changed = changed & get_inclusive_target_cone(annotated_paths_sm)

# Make a dict of peer to peer relationships that co-occur with ASNs in the intersection found above
consequential_peers = {}
for path in annotated_paths_lg:

    # If the target is preceded by a peer, then it wouldn't have been cropped, so that path could
    # be used to find the target's cone.
    if TARGET in path and path.index(TARGET) != 0 and path[path.index(TARGET) - 1] == '-':
        current_peer = path[path.index(TARGET) - 2]
        for asn in path[path.index(TARGET) + 2::2]:

            # if an ASN from the intersection is found in the path, add it to a set that correponds
            # to the current consequential peer-to-peer link
            if asn in inclusive_targ_cone_changed:
                if not current_peer in consequential_peers:
                    consequential_peers[current_peer] = set()
                consequential_peers[current_peer].add(asn)
                
print()
print("Consequential Peer-to-peer Links:")
print('(The percentages may not add up to 100% because of overlap)\n')
for k,v in sorted(consequential_peers.items(), key=lambda k_v: len(k_v[1]), reverse=True):
    print('{}-{} responsible for {} new inclusions ({}% of total)'.format(k, TARGET, len(v), str(100*len(v)/len(inclusive_targ_cone_changed))[0:4]))