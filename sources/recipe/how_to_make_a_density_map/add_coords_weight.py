import pandas as pd
import argparse

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

# combine duplicate lines and count the number of times each line appears
df = df.value_counts(sort=False).to_frame()

df.to_csv(path_or_buf=args.fname[0:-4]+'_with_weights.csv', index=False)