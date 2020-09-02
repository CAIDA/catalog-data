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
- Download [topostats-1.1beta.tar.gz](https://www.caida.org/tools/utilities/topostats/dists/topostats-1.1beta.tar.gz)
- Also available on [GitHub](https://github.com/CAIDA/topostats)



 
##  **<ins> Background </ins>**

### Programs
The 3 main programs included in this package are named `topology_stats`,
`distance`, and `betweenness`.  There are also 2 utility programs named
`components` and `preprocess-graph`, which are discussed further below.

The `topology_stats` program computes:
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

The `distance` program computes:
- Distance metrics:
  - average distance
  - std deviation of distance
- Eccentricity metrics:
  - average eccentricity
  - graph radius
  - graph diameter
  - min degree in center
  - max degree in periphery

The `betweenness` program computes:
- Betweenness metrics:
  - min node/edge betweenness
  - average node/edge betweenness
  - max node/edge betweenness

This package also includes two additional utilities.  The 'components'
program lets the user view the connected components in the input graph.
It also allows the user to extract the largest connected component
into a separate file for further analysis.  The 'distance' program,
in particular, only works on a connected graph, so the user should
create a file with just one connected component when running 'distance'.

The 'preprocess-graph' program converts an input graph into a format
needed by the 'distance', 'betweenness', and 'components' programs.

See below for details on how to use these programs.

### Requirements and compilation
This package requires the GNU Scientific Library (GSL)
(http://www.gnu.org/software/gsl/) and the Judy array library
(http://judy.sourceforge.net/).

It also requires perl for preprocessing input data and a modern C/C++
compiler.

If the required libraries are installed systemwide, then
~~~
    ./configure
    make
~~~
should be all that's required.  However, if a library is installed
somewhere that configure cannot find it, you can use
~~~
    ./configure --with-inclibprefix=<path_to_library>
~~~

### Input format
All the tools require that the input data be a list of links between nodes,
with one link per line and with each node being a number.  For example:
~~~
34 7456
525 2457
... etc
~~~
The 'topology_stats' program requires the input to be an *undirected*
graph; that is, there should only be a single line for any link in the
graph.

The 'distance', 'betweenness' and 'components' programs also require the
input to be an undirected graph, but the undirected graph must be
explicitly specified as a directed graph with symmetric links.  For
example, 'topology_stats' requires the input to look like
~~~
34 7456
~~~
to represent an undirected link between nodes 34 and 7456.  The 'distance',
'betweenness' and 'components' programs, however, require the input to look
like
~~~
34 7456
7456 34
~~~
Moreover, these programs require all links to be grouped by the source
node.  For example, to represent the links 34-7456, 34-9525, and 34-12528,
the input graph should look like
~~~
34 7456
34 9525
34 12528
7456 34
9525 34
12528 34
~~~
You can simply use the 'preprocess-graph' perl script to convert an
*undirected* graph in the format required by 'topology_stats' into
a graph file required by 'distance', 'betweenness' and 'components'.
For example,
~~~
    ./preprocess-graph < input_file > output_file
~~~

### How to use
The 'topology_stats' program requires the input file be the first and only
argument on the command line, and returns results on stdout:
~~~
    ./topology_stats input_file > output_file
~~~
There are options to dump some of the data used (for further analysis):
    -O <output filename> designates the prefix for dump filename, used below.
    -d dumps the CCDF of degree distribution, the clustering coefficients,
       and the average neighbor degrees.
    -l dumps the clustering coeffients and average neighbor degrees as above,
       but binned logarithmically.
    -v dumps the clustering coeffients and average neighbor degrees as above,
       but binned by number of data points, calculated backwards from the
       long tail.

The 'distance', 'betweenness', and 'components' programs read input data
from stdin and return results on stdout:
~~~
    ./distance < input_file > output_file
    ./betweenness < input_file > output_file
    ./components [-o component_file] < input_file
~~~


### Example output
The following are the results of running on the skitter dataset from
http://www.caida.org/research/topology/as_topo_comparisons/

'topology_stats' output:
~~~
Number of nodes:    9204
Number of edges:    28959
Avg node degree:    6.29269882659713
Max node degree:    2070
Degree dist exponent (via CCDF) [warning: can be inaccurate]:   2.13036587884151
Power-law maximum degree [warning: can be inaccurate]:  3212
Normalized avg avg neighbor degree: 0.0469423442421394
Normalized max avg neighbor degree: 0.0530352021237445
Assortative coefficient:    -0.235624710744895
Mean clustering:    0.456656295004884
Clustering coefficient: 0.0257810954106928
Top clique size:    16
Min node coreness:  0
Avg node coreness:  2.22761842677097
Max node coreness:  27
Core size:  47
Min degree in core: 68
Fringe size:    2460
Max degree in fringe:   5
~~~
'distance' output:
~~~
loaded 9204 nodes, 28959 undirected links, 42352206 pairs
... decreasing radius from 0 to 5 with node 1
... raising diameter from 0 to 5 with node 1
... raising diameter from 5 to 6 with node 9
... decreasing radius from 5 to 4 with node 22
... raising diameter from 6 to 7 with node 3287
... decreasing radius from 4 to 1 with node 21372
average distance = 3.115
std deviation of distance = 0.635
average eccentricity = 5.108
graph radius = 1
graph diameter = 7
min degree in graph center = 1
max degree in graph periphery = 1
~~~
'betweenness' output:
~~~
loaded 9204 nodes, 28959 undirected links, 42352206 pairs
min node betweenness = 0.0000e+00
average node betweenness = 2.2997e-04
max node betweenness = 2.4114e-01
min edge betweenness = 2.3617e-08
average edge betweenness = 1.0760e-04
max edge betweenness = 8.6025e-03
~~~
'components' output:
~~~
loaded 9204 nodes, 28959 undirected links
component at node 1: 9200 nodes, 28957 undirected links
component at node 21372: 2 nodes, 1 undirected links
component at node 21437: 2 nodes, 1 undirected links
3 components; largest at node ID 1
~~~


### Caveats
The exponent for the degree distribution assumes a power law and is
calculated from a simple linear fit of the logarithms of the CCDF
distribution.  This can lead to inaccurate results, as there may be
sections of the distribution that fit a power law more naturally than
others.  As a result, the theoretical maximum power law degree, which is
calculated directly from the degree distribution fit, can vary dramatically
from small changes in input data.


