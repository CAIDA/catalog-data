import pandas as pd
import geopandas as gpd
from shapely.geometry import Point
import argparse
import sys

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

world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))

# putting the higher GDP countries earlier in the list, for optimization
# (I benchmarked this and it works)
world.sort_values(ascending=False, by='gdp_md_est', ignore_index=True, inplace=True)

def coord2country(lat, long):
    
    the_point = gpd.GeoSeries([Point(long, lat)])
    
    # each row is a country; iterate through them to find
    # which country the point is in
    for row in world.itertuples():
        if the_point.within(row.geometry)[0]:
            return row.iso_a3
        
    return 'notfound'

# if the input table isn't weighted, this will add weights
# (code copied from add_coords_weight.py)
if not df.columns.str.contains('weight', regex=False).any():
    df = df.value_counts(sort=False).to_frame()
    df.reset_index(inplace=True)
    df.rename(axis='columns', mapper={0: 'weight'}, inplace=True)

# iterate through the input file assigning a country to each point
df['country'] = df.apply(lambda row: coord2country(lat=row['lat'], long=row['long']), axis=1)
df.drop(['lat', 'long'], inplace=True, axis=1)

# combine the weights of each point by country
df = df.groupby(['country']).sum()

df.to_csv(path_or_buf=args.fname[0:-4]+'_countries.csv')