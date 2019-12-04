# untested!
This solution has not be tested.

# key/values
~~~
{
    "question": "How do you found an ASN's country?",
    "solution":
    "datasets": [
        [
            "dataset":"AS Organization",
            "joins":[["AS","City"]]
        ]
    ],
    "topics": [
        "measurement methodology",
        "topology",
        "software/tools"
    ]
}
~~~

# solution

The AS Organization files contain two different types of entries: AS numbers and
organizations.  The two data types are divided by lines that start with
'# format....'. An example can be found below.   The country value is stored on the organization
field.  Create a hash mapping organizations to country and use that to match from ASN to 
organization to country.

- example input file
~~~
# format: org_id|changed|name|country|source
LVLT-ARIN|20120130|Level 3 Communications, Inc.|US|ARIN
# format: aut|changed|aut_name|org_id|opaque_id|source
1|20120224|LVLT-1|LVLT-ARIN|e5e3b9c13678dfc483fb1f819d70883c_ARIN|ARIN
~~~
