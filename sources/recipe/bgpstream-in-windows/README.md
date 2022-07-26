# How to install and use BGPStream on Windows

~~~json
{
    "id" : "bgpstream-in-windows",
    "visibility" : "public",
    "name" : "How to install BGPStream on Windows",
    "description" : "Installing BGPStream on a device running Windows 10 or 11.",
    "links": [],
    "tags" : [],
    "authors":[
        {
            "person": "person:masserfrye__richard",
            "organizations": ["CAIDA, San Diego Supercomputer Center, University of California San Diego"]
        }
    ]   
}
~~~

## Introduction

BGPStream, a framework for analyzing BGP data, does not have a distribution for Microsoft Windows. Despite this, one can still install and run BGPStream
on Windows with the help of Windows Subsystem for Linux (WSL).

## Instructions

### Installing WSL with Ubuntu

1. Run PowerShell as administrator (search "powershell" in the Windows search bar, then click "Run as administrator")
2. Type the following command, then hit enter:
```
wsl --install -d ubuntu
```
3. Restart your computer.

### Installing libBGPStream and PyBGPStream

1. Open Ubuntu from the Start menu, if it's not already open. Install libBGPStream with these two commands:
```
curl -s https://pkg.caida.org/os/$(lsb_release -si|awk '{print tolower($0)}')/bootstrap.sh | bash
sudo apt update; sudo apt-get install bgpstream
```
2. Install Python. First, run `sudo apt update` if you haven't done so recently. (If you just did the last step, this is unnecessary.)

- For Python 2, use the command `sudo apt install python2-minimal`
- For Python 3, use the command `sudo apt install python3`

3. Install PyBGPStream:

- For Python 2, use the command `sudo apt-get install python-pybgpstream`
- For Python 3, use the command `sudo apt-get install python3-pybgpstream`


## Background

### What is BGPStream?

BGPStream is a collection of tools that assist in analyzing data related to Border Gateway Protocols (BGP). Of particular importance is libBGPStream, the set of libraries underlying the overall framework, and PyBGPStream, a Python API for BGPStream.
