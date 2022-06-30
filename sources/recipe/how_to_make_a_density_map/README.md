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

The following contains information on creating density maps: maps where the density of some type of thing is indicated by color or some other signifier. Two examples will be explored: first, a [Kernel Density Estimate (KDE)](https://en.wikipedia.org/wiki/Kernel_density_estimation) geoplot based on the locations of Ookla servers, loaded from a Mongo database containing coordinate pairs. Second, a [Bivariate Map](https://en.wikipedia.org/wiki/Multivariate_map) (i.e., choropleth with another set of data overlaid) visualizing data of which countries ASes reside in and which countries CAIDA users reside in.


## Usage

These notebooks use [Geopandas](https://geopandas.org/en/stable/) and [Geoplot](https://residentmario.github.io/geoplot/). This means that you will need to set up a virtual environment if you are using a Jupyter Notebook. It is possible to just import Geopandas without the virtual environment if you are just running inside a Python script. Personally, I used [this](https://medium.com/analytics-vidhya/fastest-way-to-install-geopandas-in-jupyter-notebook-on-windows-8f734e11fa2b) Medium article by [Tanish Gupta](https://tanish-gupta.medium.com/) to set up my environment.

To run the notebook:
1. Activate the conda virtual env that has Geopandas by running the following command in Anaconda Prompt
~~~bash
 conda activate yourenv
~~~
2. Launch notebook menu using:
~~~bash
jupyter notebook
~~~
3. Navigate to notebook and run

## Code

Below is the helper method used to parse a MongoDB JSON object data. It comes from [this](https://stackoverflow.com/a/60850425/16590177)  Stack Overflow answer. This method enables to load the data into a normal JSON format which we read into a Pandas data frame.

~~~Python
def read_mongoextjson_file(filename):
    with open(filename, "r", encoding='utf8') as f:
        # read the entire input; in a real application,
        # you would want to read a chunk at a time
        bsondata = '['+f.read()+']'

        # convert the TenGen JSON to Strict JSON
        # here, I just convert the ObjectId and Date structures,
        # but it's easy to extend to cover all structures listed at
        # http://www.mongodb.org/display/DOCS/Mongo+Extended+JSON
        jsondata = re.sub(r'ObjectId\s*\(\s*\"(\S+)\"\s*\)',
                          r'{"$oid": "\1"}',
                          bsondata)
        jsondata = re.sub(r'ISODate\s*\(\s*(\S+)\s*\)',
                          r'{"$date": \1}',
                          jsondata)
        jsondata = re.sub(r'NumberInt\s*\(\s*(\S+)\s*\)',
                          r'{"$numberInt": "\1"}',
                          jsondata)

        # now we can parse this as JSON, and use MongoDB's object_hook
        # function to get rich Python data structures inside a dictionary
        data = json.loads(jsondata, object_hook=json_util.object_hook)

        return data
~~~

<br>
When using the Geopandas package, the documentation does not discuss multivariate maps. However, you can use base maps then plot on top of them. In the below example, a choropleth map is plotted first in `ax`. Then, a point plot is plotted on top of the `ax`.

~~~Python
scheme_one = mc.FisherJenks(merged['num_users'], k=7)

ax = gplt.choropleth(
    merged,
    hue='num_users',
    scheme=scheme_one,
    cmap='Blues',
    legend=True,
    figsize=(18,14)
)
gplt.pointplot(
    merged_centroids,
    ax=ax,
    scale='num_ASes',
    color='red',
    legend=True,
    limits=(3, 30),
    legend_values=[400, 200, 100, 50, 25, 10],
    legend_labels=['≤ 400 ASes', '≤ 200 ASes', '≤ 100 ASes', '≤ 50 ASes', '≤ 25 ASes', '≤ 10 ASes']
)
~~~

Since, Geopandas is built on top of Matplotlib, you can utilize underlying  Matplotlib functions for legends an plots.

~~~Python
plt.title("ASes and Users by Country")
ax.get_legend().set_title("Users")
plt.savefig('ases_and_users_by_country.png')
~~~

The code will return: ![](https://cdn.discordapp.com/attachments/942218891952783421/951328638517800990/ases_and_users_by_country.png)



## Background

Say you have some list of things and their locations, and you want to use these data to make some kind of map. [Geopandas](https://geopandas.org/en/stable/) and [Geoplot](https://residentmario.github.io/geoplot/) are tools to do this. This recipe provides examples for two (broad) kinds of map: heatmaps, using kernel density estimation, and choropleths.

What is kernel density estimation? Kernel density estimation (KDE) is a statistical technique for taking a set of points plotted on some space, and then calculating the density of the points in a continuous fashion. Because the resulting density estimates are continuous, we get a nice smooth heatmap which shows generally where the points from our data set are and where they aren't. KDE is best suited for data sets where the somewhat precise location of each point is known; for example, if a data set contained only the country as a location, it would be more appropriate to use a choropleth instead.

What is a choropleth? A choropleth is another kind of density map. Unlike heatmaps, though, choropleths only track density within given regions. For example, a choropleth of the United States might split the country up into individual states, or individual counties, and then assign each state or county a shade of color depending on some statistic related to that state or county. Importantly, density choropleths do not differentiate between different parts of the same region. A choropleth of the United States showing population density between states would *not* show the viewer that Los Angeles County has a higher population density than Death Valley.

What is a multivariate map?

A multivariate map is, for our purposes, a choropleth that displays the densities of more than one type of object. This can be done using different colors or a combination of a color and another indicator, like a [proportional symbol](https://en.wikipedia.org/wiki/Proportional_symbol_map). One possible use of a multivariate map is to give the viewer an intuitive sense of the correlation (or lack thereof) between two or more variables.

### Caveats

There is an inability to control the granularity when plotting a KDE geoplot using Geoplot. To remedy this, I...
1. Plotted points continent by continent and saved the figs to `.png` files.
2. Drew [transparencies](https://en.wikipedia.org/wiki/Transparency_(graphic)) everywhere on the image except for the mapped area and country borders.
3. Overlay the images and create a legend/scale using [Figma](https://www.figma.com/).

An issue I faced when doing this was the scale. When I plotted continent by continent, each continent would have the same max level of density (regardless of actual density relative to each other).
![](https://cdn.discordapp.com/attachments/579707526610681857/941869510544220160/unknown.png)

> Notice how Africa has the same density as Europe and other continents

To fix this, I created individual color scales based on the number of servers on each continent relative to the continent that has the most servers (South America). This allowed the scale to be accurate.
![](https://cdn.discordapp.com/attachments/579707526610681857/941930535377313852/unknown.png)
> Africa is considerably less intense compared to before

### Potential Improvements
1. The world map could have a higher level of granularity. However, this would mean plotting a KDE geoplot for every single country and following the process listed above.
2. It is possible to automate the transparency and overlay part using some sort of image processing package. 
3. Due to convenience of the packages, I filtered out some countries (Kosovo (XK), East Timor (TL), etc.) . It would be possible to hard code these situations.
