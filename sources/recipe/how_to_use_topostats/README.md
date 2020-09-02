~~~
{
    "id": "how_to_use_topostats",
    "name": "How to use topostats?",
    "visibility": "public",
    "description": "This package of programs calculates various statistics on network topologies.",
    "links": [{
        "to": "dataset:"
        }],
    "tags": [
        "topology",
        "software/tools",
        "ASN",
        "geolocation",
        "country"
    ]
}
~~~
## **<ins> Introduction </ins>**
This package of programs calculates various statistics on network topologies.
Download [topostats-1.1beta.tar.gz](https://www.caida.org/tools/utilities/topostats/dists/topostats-1.1beta.tar.gz)
Also available on [GitHub](https://github.com/CAIDA/topostats)



 
##  **<ins> Background </ins>**

### Programs
The 3 main programs included in this package are named `topology_stats`,
`distance`, and `betweenness`.  There are also 2 utility programs named
`components` and `preprocess-graph`, which are discussed further below.

The 'topology_stats' program computes:

- Average degree metrics:
  - number of nodes
  - number of edges
  - average node degree

- Degree distribution metrics:
  - max node degree
  - degree distribution power-law exponent
  - power-law maximum degree

- Joint degree distribution metrics:
  - normalized avg avg neighbor degree
  - normalized max avg neighbor degree
  - assortative coefficient

- Clustering metrics:
  - mean clustering
  - clustering coefficient

- Rich club connectivity metrics:
  - top clique size

- Coreness metrics:
  - min node coreness
  - average node coreness
  - max node coreness
  - core size
  - min degree in core
  - fringe size
  - max degree in fringe

The 'distance' program computes:

- Distance metrics:
  - average distance
  - std deviation of distance

- Eccentricity metrics:
  - average eccentricity
  - graph radius
  - graph diameter
  - min degree in center
  - max degree in periphery

The 'betweenness' program computes:

- Betweenness metrics:
  - min node/edge betweenness
  - average node/edge betweenness
  - max node/edge betweenness



### Requirements and compilation
### Input format
### How to use
### Example output

### Caveats
The exponent for the degree distribution assumes a power law and is
calculated from a simple linear fit of the logarithms of the CCDF
distribution.  This can lead to inaccurate results, as there may be
sections of the distribution that fit a power law more naturally than
others.  As a result, the theoretical maximum power law degree, which is
calculated directly from the degree distribution fit, can vary dramatically
from small changes in input data.


