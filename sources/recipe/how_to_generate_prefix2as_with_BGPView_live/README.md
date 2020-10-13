# How to Generate an IPv4 Prefix2AS File Using BGPView with Kafka Livestreaming

~~~json
{
    "id": "how_to_generate_ipv4_prefix2as_with_BGPView_live",
    "visibility": "public",
    "name": "How to generate an ipv4 prefix2as file using BGPView with Kafka livestreaming",
    "description": "Configure BGPView to monitor BGPStream on kafka for 10 minutes, generate a prefix2as file, and parse the output.",
    "tags": [
        "ASN",
        "Topology"
        ],
    "authors": [
            {
                "person": "person:ben_du",
                "organizations": ["CAIDA, San Diego Supercomputer Center, University of California San Diego"]
            }
        ]
    
}
~~~

## Introduction

This recipe will generate a prefix2as file using BGP data collected over 30 minutes from all RIPE RIS and Routeviews collectors. The following
solution contains 2 scripts. The first is a shell script which will run the BGPView program for 30 minutes and generate a comprehensive prefix2as
consumer output file. The second is a python script which will parse the previous output and generate a final prefix2as file. The final output is
formatted the same as the ones provided in the [RouteViews Prefix to AS Mappings Dataset](https://www.caida.org/data/routing/routeviews-prefix2as.xml).

### Usage

Before running the solution, install BGPView with the following commands. [Detailed information and alternative installtion options](https://github.com/CAIDA/bgpview)
are also available.

```bash
curl https://pkg.caida.org/os/ubuntu/boostrap.sh | bash
sudo apt install bgpview
```

## Solution

The following shell script is part 1 of the solution. It instructs BGPView to monitor the BGP data source on kafka for 30 minutes (1800 seconds), and then
send data to the pfx2as consumer to generate a 30-minute snapshot. More details about the [pfx2as consumer](https://github.com/CAIDA/bgpview#pfx2as) are
available. 4 output files (2 for ipv4, 2 for ipv6) will be generated and we will be using the file with `pfx2as.v4.timestamp.gz`.

~~~shell
#!/bin/bash

set -e

OUTDIR="$1"

mkdir -p $OUTDIR/logs
mkdir -p $OUTDIR/pfx2as

./bgpview-consumer \
  -i "kafka -k bgpview.bgpstream.caida.org:9192 -n bgpview-prod -c 1800" \
  -b ascii \
  -c visibility \
  -c "pfx2as -i 1800 -o $OUTDIR/pfx2as -f dsv -v"
~~~

The following python script processes the pfx2as consumer raw output by grouping together prefixes with multiple origin ASes.
The lines marked with `modify here` are to be edited for input/output file paths.

~~~python
import gzip
import pandas as pd
import numpy as np

result = []
with gzip.open('output from previous part, for example, pfx2as.v4.timestamp.gz','rt') as file: # Modify here
    for line in file:
        if line.startswith('#'):
            continue
        data = line.strip().split('|')
        if len(data) < 7:
            continue
        result.append(data[1:])

df = pd.DataFrame(result, columns=['pfx', 'asn', 'full_cnt', 'partial_cnt', 'full_duration', 'partial_duration'])
df = df.groupby(['pfx']).agg({'asn':lambda x: '_'.join(x)}).reset_index()

df['len'] = df['pfx'].apply(lambda x: int(x[x.find('/')+1:]))
df['net'] = df['pfx'].apply(lambda x: x[:x.find('/')])

df[['net', 'len', 'asn']].to_csv('output file path', header=False, index=False, sep='\t') # Modify here
~~~