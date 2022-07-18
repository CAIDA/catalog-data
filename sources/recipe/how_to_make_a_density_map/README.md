# How to create a density plot

~~~json
{
    "id" : "how_to_create_a_density_plot",
    "visibility" : "public",
    "name" : "How to create a density plot",
    "description" : "Using Geopandas to generate geoplots using data.",
    "links": [],
    "tags" : [
        "as relationship",
        "as rank"
    ],
    "authors":[
        {
            "person": "person:jonathan__lo",
            "organizations": ["CAIDA, San Diego Supercomputer Center, University of California San Diego"]
        }
    ]   
}
~~~

## Introduction

The following contains information on creating density maps, i.e. maps where the density of something is indicated by color or some other signifier. Two techniques will be explored: choropleths, in which a map is divided into regions (in this case countries) then each country is shaded based on some value, and heatmaps, which use [kernel density estimation (KDE)](https://en.wikipedia.org/wiki/Kernel_density_estimation) to produce smooth boundaries.

This recipe will demonstrate how to generate such maps using a package called [GeoPlot](https://residentmario.github.io/geoplot/), which combines the geodata capabilities of GeoPandas with the rendering capabilities of Seaborn.

## Generating a Choropleth

generate_choropleth.py is a very basic script that will produce a choropleth from a table that contains country codes and corresponding values. One may also wish to use GeoPlot directly to customize their choropleths.

coords_to_countries.py is another script that uses a package called reverse_geocode to convert a table of coordinate pairs to a table of country codes and values that can be used as input for generate_choropleth.py.

### generate_choropleth.py

#### Requirements

GeoPandas, GeoPlot, Pandas, Matplotlib, and Pycountry_Convert.

#### Usage

generate_choropleth.py takes as input a CSV file with two columns: one labelled 'country' which has country codes ([ISO 3166-1 A2](https://en.wikipedia.org/wiki/ISO_3166-1_alpha-2) and [ISO 3166-1 A3](https://en.wikipedia.org/wiki/ISO_3166-1_alpha-3) accepted), and one labelled 'weight' which has a value corresponding to each country (not every country has to have a value; countries with no value will be assigned a value of 0).

Run the script like this:
```
python generate_choropleth.py -f [name of input file] -t Title
```
(adding a title is optional)

### Using GeoPlot

GeoPlot's choropleth function, geoplot.choropleth(), requires as input a GeoDataFrame with a geometry column (i.e. a column containing, for each region, geometric information concerning the shape and location of that region) and a column that dictates how each region will be shaded. Conveniently, GeoPandas comes with a GeoDataFrame containing the geometries of the world's countries, which can be accessed with
```
geopandas.read_file(geopandas.datasets.get_path('naturalearth_lowres'))
```
An easy way to make a choropleth is merging *your* data with this built-in GeoDataFrame and then running geoplot.choropleth() on the merged table. Specify which column contains the density values with `hue` and specify the color of the map with `cmap`. See [documentation](https://residentmario.github.io/geoplot/api_reference.html#geoplot.geoplot.choropleth).

### coords_to_countries.py

#### Requirements

[Reverse_geocode](https://github.com/richardpenman/reverse_geocode)

Note: on some computers and some versions of Python this package runs into character encoding errors. If you encounter these errors, find where the source code of reverse_geocode is on your computer, delete \_\_init\_\_.py, and replace it with the version from here: [https://github.com/blushingpenguin/reverse_geocode/blob/specify_fs_encoding/\_\_init\_\_.py](https://github.com/blushingpenguin/reverse_geocode/blob/specify_fs_encoding/__init__.py)

#### Usage

This script takes as input a CSV file with a column for latitudes (labelled 'lat') and a column for longitudes (labelled 'long'). The input file can also have a weight column (i.e. a column counting the number of occurences of each coordinate pair) but doesn't have to. If the input file does have one, it should be labelled 'weight'.

Run the script like this:
```
python coords_to_countries.py -f [name of input file]
```
