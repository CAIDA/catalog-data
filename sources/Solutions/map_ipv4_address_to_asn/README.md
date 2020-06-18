## <ins> Mapping ipv4 address to AS path </ins> ##

# key/values
~~~
{
    "question": "How to find the AS path for a IPv4 address with Python?",
    "datasets": [
        [
            "dataset":"BGPStream",
            "joins":[
                ["AS Path IPv4","Prefix IPv4"]
            ]
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
Write a script that uses BGPStream's [PyBGPStream](https://bgpstream.caida.org/docs/tutorials/pybgpstream)
to download and store the AS path and prefixes into prefix-as_paths.dat.  Write a script using
[pyasn](https://pypi.org/project/pyasn/) that loads prefix-as_paths.dat, and then use it to map
between the prefix-as_paths.dat and your ips. Below are the relavent code snippets.

- [download-as_paths.py](download-as_paths.py)
- **pyasn** code snippet 
    ~~~
    import pysan
    asndb = pyasn.pyasn('prefix_as-path.dat')

    for ip in ips:
       asn_path,prefix =  asndb.lookup(ip)
       if asn:
         print (ip+"\t"+asn_path)
         # or do whatever process you need on the asn_path
    ~~~
