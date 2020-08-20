~~~
{
    "id": "how_to_parse_dataset_peeringdb",
    "visibility": "public",
    "name": "How to dataset PeeringDB?",
    "description": "Parse the data collected by PeeringDB and return a dictionary",
    "links": [{
        "to": "dataset:peeringdb"
        }],
    "tags": [
        "PeeringDB",
        "ASN",
        "topology",
        "geolocation"
    ]
}
~~~
## **<ins> Introduction </ins>**
The solution parse the data collected by PeeringDB and return a dictionary.

## **<ins> Solution </ins>**

The full script could be found in `parse_peeringdb.py` \
**Usage:** `python parse_peeringdb.py -d <input dataset> -get <objects type> -id <target id>`
- `-d`: *(Required)* Input dataset. Note that the script only supports dataset in `.sqlite` and `.json` format.
- `-get`: *(Required)* Type of the objects that you would like to retrieve 
- `-id`: *(Optional)* Id of the single object that you would like to retrieve 

Below are the methods used to read and parse data in `.json` file.   
~~~python 
# read data in json file
def get_json_data(filename):
    with open(filename) as f:
        data = json.load(f)
    return data

# Retrieves a list of designated type objects
def get_object(filename, type):
    data = get_json_data(filename)
    return data[type]['data']

# Retrieves a single designated type object by id
def get_single_object(filename, type, target_id):
    data = get_json_data(filename)
    for item in data[type]['data']:
        if item['id'] == target_id:
            return item

~~~
Below are the methods used to read and parse data in `.sqlite` file.   
~~~python 

import sqlite3

def get_sqlite_object(filename, type):
    connection = sqlite3.connect(filename)
    cursor = connection.cursor()

    # The result of a "cursor.execute" can be iterated over by row
    data = cursor.execute('SELECT * FROM ' + type + ';')
    names = [description[0] for description in cursor.description]
    obj = []
    for row in data:
        single_obj = {}
        for i in range(len(names)):
            single_obj[names[i]] = row[i]
        obj.append(single_obj)

    # Be sure to close the connection
    connection.close()
    return obj

def get_sqlite_single_object(filename, type, target_id):
    connection = sqlite3.connect(filename)
    cursor = connection.cursor()

    # The result of a "cursor.execute" can be iterated over by row
    data = cursor.execute('SELECT * FROM ' + type + ';')
    names = [description[0] for description in cursor.description]
    for row in data:
        if row[0] == target_id:
            single_obj = {}
            for i in range(len(names)):
                single_obj[names[i]] = row[i]
            connection.close()
            return single_obj
~~~

 
##  **<ins> Background </ins>**

### Dataset ###
#### PeeringDB
- An online database of peering policies, traffic volumes and geographic presence of participating networks. 
- PeeringDB, a non-profit member-based organization, has been established to support practical needs of network operators. However, it is also a valuable source of information for researchers. The first version of PeeringDB resided in a MySQL database, which was not scalable and lacked security features and data validation mechanisms. It presented potential risks of exposing contact information to spammers, and contained typos. Starting at the end of March 2016, PeeringDB switched to a new data schema and API.
- More information and download dataset [here](https://www.caida.org/data/peeringdb/)

#### Objects type in datasets

- Objects type in `.json` dataset:
- [PeeringDB API](https://www.peeringdb.com/apidocs/)

| Object     | Description |
|------------|-------------|
|  ix        |   Internet Exchange Point: the physical infrastructure through which Internet service providers (ISPs) and content delivery networks (CDNs) exchange Internet traffic between their networks |
|  fac       | Facility (Datacenter): a physical location where the IX has infrastructure, a single IX may have multiple facilities |
|  org       | Organization |
|  poc       | Network Point of Contact | 
|  net       | Network: network information |
|  ixfac     | Internet Exchange / Facility presence: combines facility and ix / net information |
|  ixlan     | Internet Exchange Network Information: abstraction of the physical ix |
|  ixpfx     | Internet Exchange Prefix: IPv4 / IPv6 range used on an ixlan |
|  netfac    | Network / Facility presence: combines net and facility information|
|  netixlan  |Network to Internet Exchange connection: combines ix and net information |

- Objects type in `.sqlite` dataset: 

| Object     | Description |
|------------|-------------|    
|  mgmtFacilities           |  Facility |
|  mgmtPublic               |  Internet Exchange Point|
|  mgmtPublicsFacilities    |  Internet Exchange / Facility presence: combines facility and ix / net information |
|  mgmtPublicsIPs           |  IP address of public| 
|  peerParticipants         |  Network |
|  peerParticipantsContacts |  Network Point of Contact  |
|  peerParticipantsPrivates |  Internet Exchange Network Information: abstraction of the physical ix |
|  peerParticipantsPublics  |  Network to Internet Exchange connection: combines ix and net information |


### sqlite3
- SQLite is a C library that provides a lightweight disk-based database that doesn’t require a separate server process and allows accessing the database using a nonstandard variant of the SQL query language. 
- The sqlite3 module was written by Gerhard Häring. It provides a SQL interface compliant with the DB-API 2.0 specification described by PEP 249.

- More information click [here](https://docs.python.org/3/library/sqlite3.html)


