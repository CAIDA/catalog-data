## PANDA Metadata
We will be creating topics and solutions for PANDA.  A individual topic/solution should be useful on it's own. If it can not be understood without a greater context, it should be kept as part of a single page with that context. That said, when possible, it is better to break up a larger context into stand alone pieces and link against those pieces. Please review your current work and consider a topic and solution, or two, that you could contibute. 

process:
- create an issue with the topic title or question as it's title: [here](https://github.com/CAIDA/panda-metadata/issues)
   - assign the issue to yourself
- create a subdirectory with the same title/question with a README.md
   - start with metadata:
   ~~~
   {
       "question": "How to find the AS path for a IPv4 address with Python?",
       "datasets": [
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
   - fill in the context of the solution or topic
- put any relavate files (scripts/config/etc) in this subdirectory

example: [How do you map an IPv4 address to a ASN path in Python?](How%20do%20you%20map%20an%20IPv4%20address%20to%20a%20ASN%20path%20in%20Python%3F)


### Possible Topics:
- Introduction to PANDA
- Introductino to Internet Data

### Possible questions:
- How do I calculate the customer cone size of an ASN?
- What is the current packet size distribution? 
- How many IP addresses are allocated to Africa? 
- How do I download a json representing the values in asran.caida.org/asns?
- How do I get a full rib file from BGPSteam?
- How many ASs do not block spoofed source addresses?
- How do I get an AS's name?
- How do I get a list of prefixes belong to a given IXP?
- Is list of ASes (A,B,C,D>..) directly connected on today's BGP tables, and since when have they been?
