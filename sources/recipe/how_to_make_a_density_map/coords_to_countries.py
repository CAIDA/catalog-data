######################################################################
# Note: If you're getting the error
#
# 'charmap' codec can't decode byte 0x81 in position 464
#
# Find __init__.py (the source code for reverse_geocode) and replace
# it with this:
# https://github.com/blushingpenguin/reverse_geocode/blob/specify_fs_encoding/__init__.py
######################################################################

import argparse
import sys
import reverse_geocode as rgeo
import pandas as pd

######################################################################
## Parameters
######################################################################
parser = argparse.ArgumentParser()
parser.add_argument("-f", dest="fname", help="name of csv file", type=str)
args = parser.parse_args()

######################################################################
## Main code
######################################################################

if args.fname is None:
    print("You need to specify a filename with -f")
    sys.exit()

df = pd.read_csv(args.fname, header=0)

# if the input table isn't weighted, this will add weights
# (code copied from add_coords_weight.py)
if not df.columns.str.contains('weight', regex=False).any():
    df = df.value_counts(sort=False).to_frame()
    df.reset_index(inplace=True)
    df.rename(axis='columns', mapper={0: 'weight'}, inplace=True)

# this line is really convoluted because rgeo.search() is supposed to
# take a list of pairs, but here we only give it one
df['country'] = df.apply(lambda row: rgeo.search([(row['lat'], row['long'])])[0]['country_code'], axis=1)
df.drop(['lat', 'long'], inplace=True, axis=1)

# combine the weights of each point by country
df = df.groupby(['country']).sum()

# save it as csv
df.to_csv(path_or_buf=args.fname[0:-4]+'_countries.csv')
