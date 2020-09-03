# How to run the Spoofer client

~~~json
{
    "id" : "how_to_run_the_spoofer_client",
    "name" : "How to run the Spoofer client",
    "description" : "The steps required to download and run the Spoofer client",
    "links": [
        {"to":"group:spoofer"},
        {"to":"software:spoofer_client"}
    ],
    "tags" : [
        "security"
    ],
    "authors":[
        {
            "person": "koga__ryan",
            "organizations": ["CAIDA, San Diego Supercomputer Center, University of California San Diego"]
        }
    ]
}
~~~

On [the Spoofer download page](https://www.caida.org/projects/spoofer/#software), select the build that matches your operating system.  Once downloaded, the Windows and MacOS installers will step you through installation, while installing on Ubuntu uses the command `apt-add-repository ppa:spoofer-dev/spoofer`.  If none of those work, the source code can be downloaded to build it yourself.

Once installed, the client should begin automated testing, but the scheduler can be paused with the "Pause Scheduler" button and tests can be manually run with the "Start Tests" button.

## Background

### What is IP spoofing?
IP spoofing is the practice of forging various portions of the Internet Protocol (IP) header. Because a vast majority of Internet traffic, applications, and servers use IP, IP spoofing has important security implications.

### What is this project?

The Spoofer Project seeks to understand the Internet's vulnerability to different types of spoofed-source IP address attacks.  The Spoofer client program attempts to send a series of spoofed UDP packets to servers distributed throughout the world. These packets are designed to test:

* Different classes of spoofed IPv4 and IPv6 addresses, including private and routable
* Ability to spoof neighboring, adjacent addresses
* Ability to spoof inbound (towards the client) and outbound (from the client)
* Where along the path filtering is observed
* Presence of a NAT device along the path

### Where can I learn more?

Screenshots of the client in use:  https://www.caida.org/projects/spoofer/screenshots.xml
FAQ:  https://www.caida.org/projects/spoofer/faq.xml
