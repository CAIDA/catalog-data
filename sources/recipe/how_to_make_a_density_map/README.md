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

The following has two notebooks. One creates a [Kernel Density Estimate (KDE)](https://en.wikipedia.org/wiki/Kernel_density_estimation) geoplot based on Ookla Server locations. Data is loaded from a Mongo database. The other notebook creates a [Multivariate Map](https://en.wikipedia.org/wiki/Multivariate_map). Data contains Users and ASes.

## Usage

The notebook using [Geopandas](https://geopandas.org/en/stable/) and [Geoplot](https://residentmario.github.io/geoplot/). This means that you will need to set up a virtual environment if you are using a Jupyter Notebook. It is possible to just import Geopandas without the virtual environment if you are just running inside a Python script. Personally, I used [this](https://medium.com/analytics-vidhya/fastest-way-to-install-geopandas-in-jupyter-notebook-on-windows-8f734e11fa2b) Medium article by [Tanish Gupta](https://tanish-gupta.medium.com/) to set up my environment.

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