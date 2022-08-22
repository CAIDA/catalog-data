__author__ = "Richard Masser-Frye"
__email__ = "<rmasserf@ucsd.edu>"

import pandas as pd
import geopandas
import geoplot
import matplotlib
import matplotlib.pyplot
import sys
import argparse

######################################################################
## Parameters
######################################################################
parser = argparse.ArgumentParser()
parser.add_argument("-f", dest="fname", help="name of csv file", type=str)
parser.add_argument("-t", dest="title", help="title your map", type=str)
parser.add_argument("-us", dest="unitedstates", help="only show the US", action='store_true')
parser.add_argument("-b", dest="bandwidth", help="adjust the bandwidth; set to 0.15 by default", type=float)
args = parser.parse_args()

######################################################################
## Main code
######################################################################
BANDWIDTH = 0.15

MAP_NAME = 'world'
if args.unitedstates:
    MAP_NAME = 'contiguous_usa'
    BANDWIDTH = 0.7

if not args.bandwidth is None:
    BANDWIDTH = args.bandwidth

if args.fname is None:
    print("You need to specify a filename with -f")
    sys.exit()

# substantive part starts here:

df = pd.read_csv(args.fname)

# if the input table isn't weighted, this will add weights
# (code copied from add_coords_weight.py)
if not df.columns.str.contains('weight', regex=False).any():
    df = df.value_counts(sort=False).to_frame()
    df.reset_index(inplace=True)
    df.rename(axis='columns', mapper={0: 'weight'}, inplace=True)

# converting the dataframe to a geodataframe
gdf = geopandas.GeoDataFrame(df, geometry=geopandas.points_from_xy(df.long, df.lat))
gdf.drop(['lat', 'long'], axis=1, inplace=True)

# loads the map file from geoplot's resources
the_map = geopandas.read_file(geoplot.datasets.get_path(MAP_NAME))

# This plots the heatmap, and returns an axis object
# We need this object in order to plot the borders map on the same axes
ax = geoplot.kdeplot(gdf, shade=True, levels=10, cmap='Reds', figsize=(18, 12), bw_adjust=BANDWIDTH, weights=gdf['weight'])

# This plots the borders map (e.g. countries or US states) on the same axes
# that we used to plot the heatmap
geoplot.polyplot(the_map, ax=ax, zorder=1)

# Add a title
if not args.title is None:
    matplotlib.pyplot.title(args.title)

matplotlib.pyplot.savefig(fname=args.fname[0:-4]+'_kde_map.png', format='png')