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
parser.add_argument("-b", dest="bandwidth", help="adjust the bandwidth; set to 0.15 by default", type=int)
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

df = pd.read_csv(args.fname)

# converting the dataframe to a geodataframe
gdf = geopandas.GeoDataFrame(df, geometry=geopandas.points_from_xy(df.long, df.lat))
gdf.drop(['lat', 'long'], axis=1, inplace=True)

world_map = geopandas.read_file(geoplot.datasets.get_path(MAP_NAME))

# This plots the heatmap
ax = geoplot.kdeplot(gdf, shade=True, levels=10, cmap='Reds', figsize=(18, 12), bw_adjust=BANDWIDTH, weights=gdf['weight'])

# This plots the map borders behind it (e.g. countries or US states)
geoplot.polyplot(world_map, ax=ax, zorder=1)

if not args.title is None:
    matplotlib.pyplot.title(args.title)

matplotlib.pyplot.savefig(fname=args.fname[0:-4]+'_kde_map.png', format='png')