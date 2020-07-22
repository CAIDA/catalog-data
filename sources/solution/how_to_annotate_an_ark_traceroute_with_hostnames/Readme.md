~~~json
{
    "id":"solution:how_to_annotate_an_ark_traceroute_with_hostnames",
    "visibility": "public",
    "name": "How to annotate an ark traceroute with hostnames?",
    "description":"",
    "links": [{}],
    "tags": [
    ]
}
~~~
## **<ins> Introduction </ins>**


### Explanation of the data fields ###


    
## **<ins> Solution </ins>**
The following script returns a dictionary 

**usage**: `parse_ark.py -n nodes.bz2 -l links.bz2 -a nodes.as.bz2 -g nodes.geo.bz2`
 ~~~python
import argparse
            
~~~
##  **<ins> Background </ins>**

### What is a Traceroute?
 
### What is Scamper?
Scamper is designed to actively probe destinations in the Internet in parallel (at a specified packets-per-second rate) so that bulk data can be collected in a timely fashion. Scamper's native output file format is called warts: a warts file contains substantial meta data surrounding each individual measurement conducted, as well as substantial detail of responses received. The measurements conducted can range from simple to complex. An example of a simple measurement is where a single measurement method (e.g. traceroute) is used on a list of IP addresses to conduct a bulk measurement. A more complex measurement might be where the outcome of a previous test influences what happens next: for example, for each hop in a traceroute path, infer the address of the outgoing interface for the previous hop. Complex measurements are conducted by connecting to a running scamper process with a driver program which contains the logic.

Download source code from [here](https://www.caida.org/tools/measurement/scamper/code/scamper-cvs-20200717.tar.gz)   

    
### <ins> Caveats </ins>



