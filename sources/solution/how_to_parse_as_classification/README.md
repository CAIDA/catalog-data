# How to Parse AS Classification

~~~json
{
    "id" : "how_to_parse_as_classification",
    "visibility" : "public",
    "name" : "How to Parse AS Classification",
    "description" : "Map each value of a given .as2type file to its asn.",
    "links": [{"to":"dataset:as_classification"}],
    "tags" : [
        "ASN",
        "as classification",
        "IPv4"
    ]   
}
~~~

## **<ins>Introduction</ins>**

The following solution shows how to parse a given AS Classification file (.as2types), and map each asn to the values found. A [script](as_2_class.py) has been given which takes in a single AS Classification file (-f), and an optional flag that prints out given asns to STDOUT (-a). The script can take in either .txt or encoded .gz file so you don't have to decompress the file.

### Usage

To use this script, you will need to have a .as2types file, which can be downloaded [here](https://www.caida.org/data/as-classification/).

To just parse the given .as2types file and just updated a dictionary labeled ```as_2_data```, use this input:

```bash
python3 as_2_class.py -f 20200101.as2types.txt.gz
```

If you would like to run this script, and print values of asns from ```as_2_data``` to STDOUT, use this input:

```bash
python3 as_2_class.py -f 20200101.as2types.txt.gz -a 1,2,3
```

## **<ins>Solution</ins>**

Below are code snippets from the available script showing how to parse a given .as2types file. The script parses the given file, and maps each asn found to its values in a dictionary labeled, ```as_2_data```. The first snippet shows how to parse a single line from an opened .as2types file. This is assuming the line has been decoded (if from a .gz file).

~~~Python
# Parse a given line to map the current asn to its values.
def parse_as_2_types_line(curr_line):
    global as_2_data

    # Edge Case: Skip commented out lines.
    if curr_line[0] == "#":
        return

    # Remove any trailing characters.
    curr_line = curr_line.rstrip()

    # Split the current line into its three values.
    asn, source, classification = curr_line.split("|")

    # Updated as_2_data with the current line's values.
    as_2_data[asn] = {
        "asn" : asn,
        "source" : source,
        "class" : classification
    }
~~~

Below is a method for printing a value from ```as_2_data``` to STDOUT. The user can use this for testing, or to convert the initial file format to a json formatted file. The solution script calls this on all asns given to the (-a) flag.

~~~Python
# Prints the given asn's json data to STDOUT.
def get_asn(asn):
    global as_2_data
    
    # Edge Case: Don't access the dictionary if asn not in as_2_data.
    if asn not in as_2_data:
        print("{} not in as_2_data".format(asn))
    else:
        print(json.dumps(as_2_data[asn])
~~~

Below is a helper method offered to update ```as_2_data``` with a given asn, key, and value. This method is not directly used in the script, although could be used by the user to update ```as_2_data``` with individual values. Implementations of this method could allow a user to give an input of each value to be placed inside ```as_2_data``` manually.

~~~Python
# Given an asn, update as_2_data with the given key and value.
def update_as2data(asn, key, value):
    global as_2_data

    # Edge Case: Insert the asn if it doesn't already exist.
    if asn not in as_2_data:
        as_2_data[asn] = {}
    as_2_data[asn][key] = value
~~~

## **<ins>Background</ins>**

### What is AS Classification?

  - AS Classification is file type that maps and AS to an assumed type of business (class).
  - This data is used to train a machine-learning classifier.
  - Using the self-reported data from [PeeringDB](https://www.peeringdb.com/), this data catagorizes PeeringDB classifications into three catagories, combining some of PeeringDB's classification into one classification.
  - More information about AS Classification can be found [here](https://www.caida.org/data/as-classification/)

### What do the Source and Classifications mean?

|Source|Description|
|:-----|:----------|
|CAIDA_class|Classification was an inference from the machine-learning classifier.|
|peerDB_class|AS classification was obtained directly from the PeeringDB database.|

|Class|Description|
|:----|:----------|
|Transit/Access|ASes which was inferred to be either a transit and/or access provider.|
|Content|ASes which provide content hosting and distribution systems.|
|Enterprise|Various organizations, universities and companies at the network edge that are mostly users, rather than providers of Internet access, transit or content.|

### Caveats

 - Half of the ground-truth data is used to validate the machine-learning classifier. The Positive Predictive Value (PPV) of the classifier is currently 70%.

### File Format

For the purpose of this solution, any data that is commented out is not needed, and should be ignored.

~~~test
# ....
<AS>|<Source>|<Class>
~~~
