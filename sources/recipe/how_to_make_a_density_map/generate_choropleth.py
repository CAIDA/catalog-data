# Copyright (c) 2023 The Regents of the University of California
# All Rights Reserved

__author__ = "Richard Masser-Frye"
__email__ = "<rmasserf@ucsd.edu>"

import pandas as pd
import matplotlib.pyplot as plt
import geopandas as gpd
import geoplot as gplt
import pycountry_convert as pcc
import argparse
import sys
import matplotlib
import matplotlib.pyplot
import mapclassify

INCOMPATIBLE_CODES = ['KOS', 'CYN', '-99']
NUM_BINS = 8

######################################################################
## Parameters
######################################################################
parser = argparse.ArgumentParser()
parser.add_argument("-f", dest="fname", help="name of csv file", type=str)
parser.add_argument("-t", dest="title", help="title your map", type=str)
parser.add_argument("-b", dest="bins", help="how many shades", type=int)
args = parser.parse_args()

######################################################################
## Main code
######################################################################

if args.fname is None:
    print("You need to specify a filename with -f")
    sys.exit()

if not args.bins is None:
    NUM_BINS = args.bins

df = pd.read_csv(args.fname, header=0)
world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))

left_merge = 'iso_a3'

# In case the input file uses A2 country codes
if len(df['country'][0]) == 2:
    # Drop problematic rows
    # ie rows that will cause an error when you try to convert their A3 codes
    # Sorry Kosovo, North Cyprus, and Somaliland...
    rows_to_drop = world[world['iso_a3'].isin(INCOMPATIBLE_CODES)].index
    world.drop(rows_to_drop, inplace=True)

    # Add A2 codes to the database of countries to facilitate merging
    world['iso_a2'] = world.apply(lambda row: pcc.country_alpha3_to_country_alpha2(row['iso_a3']), axis=1)
    world.drop('iso_a3', axis=1, inplace=True)
    left_merge = 'iso_a2'

# Merge the database of countries with the input data
# fillna(0) assigns 0 to countries with no input
merged = world.merge(df, how='left', left_on=left_merge, right_on='country').fillna(0)

# Create "bins" for the values to be sorted into
# This makes the plot look a lot better trust me
fj = mapclassify.FisherJenks(y=merged['weight'], k=NUM_BINS)

# Plot the choropleth
gplt.choropleth(merged, hue='weight', cmap='Reds', figsize=(18,14), scheme=fj, legend=True)

# Add a title
if not args.title is None:
    matplotlib.pyplot.title(args.title)

matplotlib.pyplot.savefig(fname=args.fname[0:-4]+'_choropleth.png', format='png')