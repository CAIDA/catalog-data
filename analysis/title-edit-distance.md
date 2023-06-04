exe:./scripts/check-title-distance.py
issue:[Put related objects in access](https://github.com/CAIDA/catalog-data/issues/565)
This is analysis of using edit distance on the names of the original paper and related
papers, media, and presentations.

The questions is how many false positives we generated .
Here is a list of papers that match.

**dist**: edit distance
**length**: length of the original paper
**ratio**: 100* distance / length
**name**: the first name is the paper, all following names are from related objects

<span sytel='font-size:-1'>

| dist/length | ratio  | name  | date | type |
|----|---|----|-----|----|
35
| ----- | -- | **Duality between equilibrium and growing networks** | 201308 | Paper|
| 17/48 | 35% | Duality Between Static and Dynamic Networks | 201310 | Presentation|
33
| ----- | -- | **QUINCE: A unified crowdsourcing-based QoE measurement platform** | 201908 | Paper|
| 21/62 | 33% | QUINCE: A gamified crowdsourcing QoE assessment framework | 201803 | Presentation|
32
| ----- | -- | **Third Accountability and Transparency Review Team (ATRT3) Report** | 202005 | Paper|
| 21/64 | 32% | Third Accountability and Transparency Review Team (ATRT3) Report - Minority Statement | 202005 | Paper|
30
| ----- | -- | **Internet measurement and data analysis: topology, workload, performance and routing statistics** | 199903 | Paper|
| 29/94 | 30% | Internet measurement: topology, workload, performance and routing | 199812 | Presentation|
27
| ----- | -- | **Internet Topology Data Comparison** | 201205 | Paper|
|  9/33 | 27% | Internet Topology Data Kit | 201102 | Presentation|
| 10/33 | 30% | Internet Topology Data Kit Update | 201208 | Presentation|
25
| ----- | -- | **Otter: A general-purpose network visualization tool** | 199906 | Paper|
| 13/51 | 25% | Otter: General Purpose Network Viz Tool | 199808 | Presentation|
25
| ----- | -- | **A Basis for Systematic Analysis of Network Topologies: Technical Report** | 200604 | Paper|
| 18/71 | 25% | A Basis for Systematic Analysis of Network Topologies | 200605 | Presentation|
24
| ----- | -- | **Third Accountability and Transparency Review Team (ATRT3) Report - Minority Statement** | 202005 | Paper|
| 21/85 | 24% | Third Accountability and Transparency Review Team (ATRT3) Report | 202005 | Paper|
23
| ----- | -- | **Impact of Degree Correlations on Topology Generators** | 200508 | Paper|
| 12/52 | 23% | Degree correlations and topology generators | 200503 | Presentation|
23
| ----- | -- | **BGPStream: a software framework for live and historical BGP data analysis** | 201510 | Paper|
| 17/73 | 23% | BGPStream - An Open Source Framework for Live/Historical BGP Data Analysis | 201505 | Presentation|
22
| ----- | -- | **CAIDA: Visualizing the Internet** | 200101 | Paper|
|  7/31 | 22% | AS Core: Visualizing the Internet | 201103 | Presentation|
20
| ----- | -- | **A Robust System for Accurate Real-time Summaries of Internet Traffic: Technical Report** | 200506 | Paper|
| 18/86 | 20% | A Robust System for Accurate Real-time Summaries of Internet Traffic | 200506 | Paper|
| 18/86 | 20% | A Robust System for Accurate Real-time Summaries of Internet Traffic | 200506 | Presentation|
20
| ----- | -- | **Evolution of the Internet AS-Level Ecosystem** | 200902 | Paper|
|  9/44 | 20% | Evolution of the Internet Ecosystem | 200910 | Presentation|
20
| ----- | -- | **Experience in using MTurk for Network Measurement** | 201508 | Paper|
| 10/49 | 20% | Experience in using Mechanical Turk for Network Measurement | 201508 | Presentation|
20
| ----- | -- | **Toward a Theory of Harms in the Internet Ecosystem** | 201909 | Paper|
| 10/50 | 20% | Toward a theory of harms in the Internet | 201909 | Presentation|
19
| ----- | -- | **Two Days in the Life of the DNS Anycast Root Servers** | 200704 | Paper|
| 10/52 | 19% | Two days in the life of three DNS root servers | 200611 | Presentation|
18
| ----- | -- | **Inferring BGP Blackholing Activity in the Internet** | 201711 | Paper|
|  9/50 | 18% | Inferring BGP Blackholing in the Internet | 201711 | Presentation|
17
| ----- | -- | **Greedy Forwarding in Dynamic Scale-Free Networks Embedded in Hyperbolic Metric Spaces: Technical Report** | 200907 | Paper|
| 26/103 | 25% | Greedy Forwarding in Scale-Free Networks Embedded in Hyperbolic Metric Spaces | 200909 | Paper|
| 18/103 | 17% | Greedy Forwarding in Dynamic Scale-Free Networks Embedded in Hyperbolic Metric Spaces | 201003 | Paper|
15
| ----- | -- | **Systematic Topology Analysis and Generation Using Degree Correlations** | 200609 | Paper|
| 11/69 | 15% | dK-series: Systematic Topology Analysis and Generation Using Degree Correlations | 200606 | Presentation|
15
| ----- | -- | **Annotated Schema: Mapping Ontologies onto Dataset Schemas** | 202305 | Paper|
|  9/57 | 15% | Annotated Schema: Mapping Ontologies onto Dataset Schemas Slideset | 202305 | Presentation|
11
| ----- | -- | **Where .ru? Assessing the Impact of Conflict on Russian Domain Infrastructure** | 202210 | Paper|
|  9/76 | 11% | Where .ru? Assessing the Impact of Conflict on Russian Domain Infrastructure Slideset | 202210 | Presentation|
10
| ----- | -- | **Learning Regexes to Extract Router Names from Hostnames** | 201910 | Paper|
|  8/55 | 14% | Learning to Extract Router Names from Hostnames | 201910 | Presentation|
|  6/55 | 10% | Learning Regexes to Extract Network Names from Hostnames | 202112 | Paper|
10
| ----- | -- | **Internet-Scale IPv4 Alias Resolution with MIDAR** | 201304 | Paper|
|  5/47 | 10% | Internet-Scale Alias Resolution with MIDAR | 201002 | Presentation|
6
| ----- | -- | **The 10th Workshop on Active Internet Measurements (AIMS-10) Report** | 201810 | Paper|
|  4/66 |  6% | The 9th Workshop on Active Internet Measurements (AIMS-9) Report | 201710 | Paper|
4
| ----- | -- | **The 8th Workshop on Active Internet Measurements (AIMS8) Report** | 201610 | Paper|
|  3/63 |  4% | The 9th Workshop on Active Internet Measurements (AIMS-9) Report | 201710 | Paper|
|  3/63 |  4% | The 7th Workshop on Active Internet Measurements (AIMS-7) Report | 201601 | Paper|
4
| ----- | -- | **The 9th Workshop on Active Internet Measurements (AIMS-9) Report** | 201710 | Paper|
|  3/64 |  4% | The 8th Workshop on Active Internet Measurements (AIMS8) Report | 201610 | Paper|
|  4/64 |  6% | The 10th Workshop on Active Internet Measurements (AIMS-10) Report | 201810 | Paper|
4
| ----- | -- | **The 7th Workshop on Active Internet Measurements (AIMS-7) Report** | 201601 | Paper|
|  3/64 |  4% | The 8th Workshop on Active Internet Measurements (AIMS8) Report | 201610 | Paper|
4
| ----- | -- | **MAnycast2 - Using Anycast to Measure Anycast** | 202010 | Paper|
|  2/44 |  4% | MAnycast2 Using Anycast to Measure Anycast | 202010 | Presentation|
3
| ----- | -- | **Streams, Flows and Torrents** | 200104 | Paper|
|  1/27 |  3% | Streams Flows and Torrents | 200104 | Presentation|
3
| ----- | -- | **A Framework for Understanding and Applying Ethical Principles in Network and Security Research ** | 201001 | Paper|
|  3/95 |  3% | Framework for Understanding and Applying Ethical Principles in Network and Security Research | 201001 | Presentation|
3
| ----- | -- | **Inferring Multilateral Peering** | 201312 | Paper|
|  1/30 |  3% | Inferring Multilateral Peering  | 201312 | Presentation|
2
| ----- | -- | **Percolation in Self-Similar Networks ** | 201101 | Paper|
|  1/37 |  2% | Percolation in self-similar networks | 201106 | Presentation|
|  1/37 |  2% | Percolation in self-similar networks | 201103 | Presentation|
2
| ----- | -- | **Named Data Networking Next Phase (NDN-NP) Project May 2014 - April 2015 Annual Report** | 201506 | Paper|
|  2/85 |  2% | Named Data Networking Next Phase (NDN-NP) Project May 2016 - April 2017 Annual Report | 201711 | Paper|
|  2/85 |  2% | Named Data Networking Next Phase (NDN-NP) Project May 2015 - April 2016 Annual Report | 201606 | Paper|
2
| ----- | -- | **Periscope: Unifying Looking Glass Querying** | 201603 | Paper|
|  1/42 |  2% | Periscope:Unifying Looking Glass Querying | 201603 | Presentation|
|  1/42 |  2% | Periscope: Unifying Looking Glass querying  | 201512 | Presentation|
2
| ----- | -- | **Named Data Networking Next Phase (NDN-NP) Project May 2015 - April 2016 Annual Report** | 201606 | Paper|
|  2/85 |  2% | Named Data Networking Next Phase (NDN-NP) Project May 2014 - April 2015 Annual Report | 201506 | Paper|
|  2/85 |  2% | Named Data Networking Next Phase (NDN-NP) Project May 2016 - April 2017 Annual Report | 201711 | Paper|
2
| ----- | -- | **Named Data Networking Next Phase (NDN-NP) Project May 2016 - April 2017 Annual Report** | 201711 | Paper|
|  2/85 |  2% | Named Data Networking Next Phase (NDN-NP) Project May 2014 - April 2015 Annual Report | 201506 | Paper|
|  2/85 |  2% | Named Data Networking Next Phase (NDN-NP) Project May 2015 - April 2016 Annual Report | 201606 | Paper|
2
| ----- | -- | **Understanding and preparing for DNS evolution ** | 201004 | Paper|
|  1/46 |  2% | Understanding and Preparing for DNS Evolution | 201004 | Presentation|
2
| ----- | -- | **One-way Traffic Monitoring with iatmon** | 201203 | Paper|
|  1/38 |  2% | One way Traffic Monitoring with iatmon | 201205 | Presentation|
2
| ----- | -- | **AS Relationships, Customer Cones, and Validation** | 201310 | Paper|
|  1/48 |  2% | AS Relationships, Customer Cones, and Validation  | 201310 | Presentation|
2
| ----- | -- | **A Second Look at Detecting Third-Party Addresses in Traceroute Traces with the IP Timestamp Option** | 201403 | Paper|
|  2/98 |  2% | A second look at ‟Detecting third-party addresses in traceroute traces with the IP timestamp option“ | 201403 | Presentation|
2
| ----- | -- | **IPv6 AS Relationships, Cliques, and Congruence** | 201503 | Paper|
|  1/46 |  2% | IPv6 AS Relationships, Clique, and Congruence | 201503 | Presentation|
1
| ----- | -- | **Workshop on Internet Economics (WIE2017) Final Report** | 201807 | Paper|
|  1/53 |  1% | Workshop on Internet Economics (WIE2016) Final Report | 201707 | Paper|
|  1/53 |  1% | Workshop on Internet Economics (WIE2018) Final Report | 201904 | Paper|
1
| ----- | -- | **Measuring the Deployment of IPv6: Topology, Routing and Performance** | 201211 | Paper|
|  1/67 |  1% | Measuring the Deployment of IPv6: Topology, Routing, and Performance | 201211 | Presentation|
1
| ----- | -- | **Workshop on Internet Economics (WIE2016) Final Report** | 201707 | Paper|
|  1/53 |  1% | Workshop on Internet Economics (WIE2017) Final Report | 201807 | Paper|
1
| ----- | -- | **PacketLab: A Universal Measurement Endpoint Interface** | 201711 | Paper|
|  1/53 |  1% | PacketLab:A Universal Measurement Endpoint Interface | 201711 | Presentation|
1
| ----- | -- | **Workshop on Internet Economics (WIE2018) Final Report** | 201904 | Paper|
|  1/53 |  1% | Workshop on Internet Economics (WIE2017) Final Report | 201807 | Paper|
0
| ----- | -- | **Popularity versus Similarity in Growing Networks** | 201209 | Paper|
|  0/48 |  0% | Popularity versus Similarity in Growing Networks | 201211 | Presentation|
|  0/48 |  0% | Popularity versus Similarity in Growing Networks | 201110 | Presentation|
|  0/48 |  0% | Popularity versus Similarity in Growing Networks | 201111 | Presentation|
|  0/48 |  0% | Popularity versus Similarity in Growing Networks | 201203 | Presentation|
|  0/48 |  0% | Popularity versus Similarity in Growing Networks | 201202 | Presentation|
|  0/48 |  0% | Popularity versus Similarity in Growing Networks | 201303 | Presentation|
0
| ----- | -- | **Hyperbolic Geometry of Complex Networks** | 201010 | Paper|
|  0/39 |  0% | Hyperbolic geometry of complex networks | 201005 | Presentation|
|  0/39 |  0% | Hyperbolic geometry of complex networks | 200910 | Presentation|
|  0/39 |  0% | Hyperbolic geometry of complex networks | 201104 | Presentation|
|  6/39 | 15% | Hyperbolic geometry of large networks | 201202 | Presentation|
0
| ----- | -- | **Greedy Forwarding in Dynamic Scale-Free Networks Embedded in Hyperbolic Metric Spaces** | 201003 | Paper|
|  0/85 |  0% | Greedy Forwarding in Dynamic Scale-Free Networks Embedded in Hyperbolic Metric Spaces | 201003 | Presentation|
| 18/85 | 21% | Greedy Forwarding in Dynamic Scale-Free Networks Embedded in Hyperbolic Metric Spaces: Technical Report | 200907 | Paper|
|  8/85 |  9% | Greedy Forwarding in Scale-Free Networks Embedded in Hyperbolic Metric Spaces | 200906 | Presentation|
0
| ----- | -- | **Analysis of Country-wide Internet Outages Caused by Censorship** | 201111 | Paper|
|  0/62 |  0% | Analysis of Country-wide Internet Outages Caused by Censorship | 201207 | Presentation|
|  0/62 |  0% | Analysis of Country-wide Internet Outages Caused by Censorship | 201111 | Presentation|
|  0/62 |  0% | Analysis of Country-wide Internet Outages Caused by Censorship | 201112 | Presentation|
0
| ----- | -- | **Analysis of a "/0" Stealth Scan from a Botnet** | 201211 | Paper|
| 14/45 | 31% | Analysis of an Internet-wide Stealth Scan from a Botnet | 201212 | Presentation|
|  0/45 |  0% | Analysis of a "/0" Stealth Scan from a Botnet | 201504 | Paper|
|  0/45 |  0% | Analysis of a "/0" Stealth Scan from a Botnet | 201211 | Presentation|
0
| ----- | -- | **Analysis of a "/0" Stealth Scan from a Botnet** | 201504 | Paper|
|  0/45 |  0% | Analysis of a "/0" Stealth Scan from a Botnet | 201211 | Paper|
| 14/45 | 31% | Analysis of an Internet-wide Stealth Scan from a Botnet | 201212 | Presentation|
|  0/45 |  0% | Analysis of a "/0" Stealth Scan from a Botnet | 201211 | Presentation|
0
| ----- | -- | **Lost in Space: Improving Inference of IPv4 Address Space Utilization** | 201509 | Paper|
|  0/68 |  0% | Lost in Space: Improving Inference of IPv4 Address Space Utilization | 201410 | Paper|
|  0/68 |  0% | Lost in Space: Improving Inference of IPv4 Address Space Utilization | 201510 | Presentation|
|  0/68 |  0% | Lost in Space: Improving Inference of IPv4 Address Space Utilization | 201606 | Paper|
0
| ----- | -- | **ARTEMIS: Neutralizing BGP Hijacking within a Minute** | 201812 | Paper|
|  0/51 |  0% | ARTEMIS: Neutralizing BGP Hijacking within a Minute | 201807 | Presentation|
|  0/51 |  0% | ARTEMIS: Neutralizing BGP Hijacking within a Minute | 201803 | Presentation|
|  0/51 |  0% | ARTEMIS: Neutralizing BGP Hijacking within a Minute | 201805 | Presentation|
0
| ----- | -- | **IRR Hygiene in the RPKI Era** | 202203 | Paper|
|  0/27 |  0% | IRR Hygiene in the RPKI Era | 202111 | Paper|
|  0/27 |  0% | IRR Hygiene in the RPKI Era | 202110 | Presentation|
|  0/27 |  0% | IRR Hygiene in the RPKI Era | 202203 | Presentation|
0
| ----- | -- | **DNS Root/gTLD Performance Measurements** | 200112 | Paper|
|  0/38 |  0% | DNS Root/gTLD Performance Measurements | 200112 | Presentation|
|  6/38 | 15% | DNS/gTLD Performance Measurements  | 200112 | Presentation|
0
| ----- | -- | **Building a Better NetFlow** | 200409 | Paper|
|  0/25 |  0% | Building a Better NetFlow | 200409 | Presentation|
|  0/25 |  0% | Building a Better NetFlow | 200408 | Presentation|
0
| ----- | -- | **A Robust System for Accurate Real-time Summaries of Internet Traffic** | 200506 | Paper|
| 18/68 | 26% | A Robust System for Accurate Real-time Summaries of Internet Traffic: Technical Report | 200506 | Paper|
|  0/68 |  0% | A Robust System for Accurate Real-time Summaries of Internet Traffic | 200506 | Presentation|
0
| ----- | -- | **Navigability of Complex Networks** | 200901 | Paper|
|  0/32 |  0% | Navigability of complex networks | 201001 | Presentation|
|  8/32 | 25% | Navigability of Networks | 201005 | Presentation|
0
| ----- | -- | **Greedy Forwarding in Scale-Free Networks Embedded in Hyperbolic Metric Spaces** | 200909 | Paper|
|  0/77 |  0% | Greedy Forwarding in Scale-Free Networks Embedded in Hyperbolic Metric Spaces | 200906 | Presentation|
| 26/77 | 33% | Greedy Forwarding in Dynamic Scale-Free Networks Embedded in Hyperbolic Metric Spaces: Technical Report | 200907 | Paper|
0
| ----- | -- | **Identification of influential spreaders in complex networks** | 201008 | Paper|
|  0/59 |  0% | Identification of Influential Spreaders in Complex Networks | 201103 | Presentation|
|  0/59 |  0% | Identification of Influential Spreaders in Complex Networks | 201005 | Presentation|
0
| ----- | -- | **A Value-based Framework for Internet Peering Agreements** | 201010 | Paper|
|  0/55 |  0% | A Value-based Framework for Internet Peering Agreements | 201009 | Presentation|
|  1/55 |  1% | A Value-based Framework for Internet Peering Agreements  | 201006 | Presentation|
0
| ----- | -- | **Extracting benefit from harm: using malware pollution to analyze the impact of political and geophysical events on the Internet** | 201201 | Paper|
|  0/127 |  0% | Extracting Benefit from Harm: Using Malware Pollution to Analyze the Impact of Political and Geophysical Events on the Internet | 201208 | Presentation|
|  0/127 |  0% | Extracting Benefit from Harm: Using Malware Pollution to Analyze the Impact of Political and Geophysical Events on the Internet | 201201 | Presentation|
0
| ----- | -- | **Gaining Insight into AS-level Outages through Analysis of Internet Background Radiation** | 201304 | Paper|
|  0/87 |  0% | Gaining Insight into AS-level Outages through Analysis of Internet Background Radiation | 201212 | Paper|
|  0/87 |  0% | Gaining Insight into AS-level Outages through Analysis of Internet Background Radiation | 201304 | Presentation|
0
| ----- | -- | **Speedtrap: Internet-Scale IPv6 Alias Resolution** | 201310 | Paper|
|  0/47 |  0% | Speedtrap: Internet-Scale IPv6 Alias Resolution | 201310 | Presentation|
| 17/47 | 36% | Large Scale IPv6 Alias Resolution | 201301 | Presentation|
0
| ----- | -- | **A Coordinated View of the Temporal Evolution of Large-scale Internet Events** | 201401 | Paper|
|  0/75 |  0% | A Coordinated View of the Temporal Evolution of Large-scale Internet Events | 201401 | Media|
| 26/75 | 34% | A Coordinated View of Large-Scale Internet Events | 201211 | Presentation|
0
| ----- | -- | **Lost in Space: Improving Inference of IPv4 Address Space Utilization** | 201410 | Paper|
|  0/68 |  0% | Lost in Space: Improving Inference of IPv4 Address Space Utilization | 201606 | Paper|
|  0/68 |  0% | Lost in Space: Improving Inference of IPv4 Address Space Utilization | 201509 | Paper|
0
| ----- | -- | **Adding Enhanced Services to the Internet: Lessons from History** | 201509 | Paper|
|  0/62 |  0% | Adding Enhanced Services to the Internet: Lessons from History | 201607 | Paper|
|  0/62 |  0% | Adding Enhanced Services to the Internet: Lessons from History | 201509 | Presentation|
0
| ----- | -- | **Lost in Space: Improving Inference of IPv4 Address Space Utilization** | 201606 | Paper|
|  0/68 |  0% | Lost in Space: Improving Inference of IPv4 Address Space Utilization | 201410 | Paper|
|  0/68 |  0% | Lost in Space: Improving Inference of IPv4 Address Space Utilization | 201509 | Paper|
0
| ----- | -- | **BGPStream: a software framework for live and historical BGP data analysis** | 201611 | Paper|
|  0/73 |  0% | BGPStream: A Software Framework for Live and Historical BGP Data Analysis | 201611 | Presentation|
|  1/73 |  1% | BGPStream: A Software Framework for Live and Historical BGP Data Analysis  | 201703 | Presentation|
0
| ----- | -- | **Detecting Peering Infrastructure Outages in the Wild** | 201708 | Paper|
|  0/52 |  0% | Detecting Peering Infrastructure Outages in the Wild | 201708 | Presentation|
|  0/52 |  0% | Detecting Peering Infrastructure Outages in the Wild | 201712 | Presentation|
0
| ----- | -- | **TCP Congestion Signatures** | 201711 | Paper|
|  0/25 |  0% | TCP Congestion Signatures | 201711 | Presentation|
|  0/25 |  0% | TCP Congestion Signatures | 201807 | Presentation|
0
| ----- | -- | **Investigating the Causes of Congestion on the African IXP substrate** | 201711 | Paper|
|  0/67 |  0% | Investigating the Causes of Congestion on the African IXP substrate | 201811 | Presentation|
|  0/67 |  0% | Investigating the Causes of Congestion on the African IXP substrate | 201711 | Presentation|
0
| ----- | -- | **Unresolved Issues: Prevalence, Persistence, and Perils of Lame Delegations** | 202010 | Paper|
|  8/74 | 10% | Unresolved Issues: Prevalence, Persistence, and Perils of Lame Delegations (Video) | 202010 | Media|
|  0/74 |  0% | Unresolved Issues: Prevalence, Persistence, and Perils of Lame Delegations | 202010 | Presentation|
0
| ----- | -- | **DynamIPs: Analyzing address assignment practices in IPv4 and IPv6** | 202012 | Paper|
|  8/65 | 12% | DynamIPs: Analyzing address assignment practices in IPv4 and IPv6 (Video) | 202012 | Media|
|  0/65 |  0% | DynamIPs: Analyzing address assignment practices in IPv4 and IPv6 | 202012 | Presentation|
0
| ----- | -- | **Challenges in measuring the Internet for the public Interest** | 202108 | Paper|
|  0/60 |  0% | Challenges in measuring the Internet for the public Interest | 202205 | Paper|
|  0/60 |  0% | Challenges in measuring the Internet for the public Interest | 202109 | Presentation|
0
| ----- | -- | **IRR Hygiene in the RPKI Era** | 202111 | Paper|
|  0/27 |  0% | IRR Hygiene in the RPKI Era | 202203 | Paper|
|  0/27 |  0% | IRR Hygiene in the RPKI Era | 202110 | Presentation|
0
| ----- | -- | **Learning Regexes to Extract Network Names from Hostnames** | 202112 | Paper|
|  6/56 | 10% | Learning Regexes to Extract Router Names from Hostnames | 201910 | Paper|
|  0/56 |  0% | Learning Regexes to Extract Network Names from Hostnames | 202112 | Presentation|
0
| ----- | -- | **Challenges in measuring the Internet for the public Interest** | 202205 | Paper|
|  0/60 |  0% | Challenges in measuring the Internet for the public Interest | 202108 | Paper|
|  0/60 |  0% | Challenges in measuring the Internet for the public Interest | 202109 | Presentation|
0
| ----- | -- | **GTrace - A Graphical Traceroute Tool** | 199911 | Paper|
|  0/36 |  0% | GTrace - A Graphical Traceroute Tool | 199911 | Presentation|
0
| ----- | -- | **Internet Expansion, Refinement, and Churn** | 200201 | Paper|
|  0/41 |  0% | Internet expansion, refinement, and churn | 200202 | Presentation|
0
| ----- | -- | **Distance Metrics in the Internet** | 200209 | Paper|
|  0/32 |  0% | Distance metrics in the Internet | 200209 | Presentation|
0
| ----- | -- | **Traceroute and BGP AS Path Incongruities** | 200303 | Paper|
|  0/40 |  0% | Traceroute and BGP AS Path Incongruities | 200306 | Presentation|
0
| ----- | -- | **Internet Quarantine: Requirements for Containing Self-Propagating Code** | 200304 | Paper|
|  0/70 |  0% | Internet Quarantine: Requirements for Containing Self-Propagating Code | 200304 | Presentation|
0
| ----- | -- | **On Third-party Addresses in Traceroute Paths** | 200304 | Paper|
|  0/44 |  0% | On Third-party Addresses in Traceroute Paths | 200304 | Presentation|
0
| ----- | -- | **Their share: diversity and disparity in IP traffic** | 200404 | Paper|
|  0/50 |  0% | Their Share: Diversity and Disparity in IP Traffic | 200404 | Presentation|
0
| ----- | -- | **The Spread of the Witty Worm** | 200408 | Paper|
|  0/28 |  0% | The Spread of the Witty Worm | 200407 | Presentation|
0
| ----- | -- | **Revisiting Internet AS-level Topology Discovery** | 200503 | Paper|
|  0/47 |  0% | Revisiting Internet AS-level Topology Discovery | 200503 | Presentation|
0
| ----- | -- | **Spectroscopy of traceroute delays** | 200503 | Paper|
|  0/33 |  0% | Spectroscopy of Traceroute Delays | 200503 | Presentation|
0
| ----- | -- | **Comparison of Public End-to-End Bandwidth Estimation Tools on High-Speed Links** | 200503 | Paper|
|  0/78 |  0% | Comparison of Public End-to-End Bandwidth Estimation tools on High-Speed Links | 200503 | Presentation|
0
| ----- | -- | **Inferring AS Relationships: Dead End or Lively Beginning?** | 200505 | Paper|
|  0/57 |  0% | Inferring AS Relationships: Dead End or Lively Beginning? | 200505 | Presentation|
0
| ----- | -- | **Passive Monitoring of DNS Anomalies** | 200707 | Paper|
|  0/35 |  0% | Passive Monitoring of DNS Anomalies | 200707 | Presentation|
0
| ----- | -- | **Traceroute Probe Method and Forward IP Path Inference** | 200810 | Paper|
|  0/53 |  0% | Traceroute Probe Method and Forward IP Path Inference | 200810 | Presentation|
0
| ----- | -- | **An Internet Data Sharing Framework For Balancing Privacy and Utility** | 200910 | Paper|
|  0/68 |  0% | An Internet Data Sharing Framework For Balancing Privacy and Utility | 200910 | Presentation|
0
| ----- | -- | **Estimating Routing Symmetry on Single Links by Passive Flow Measurements** | 201003 | Paper|
|  0/72 |  0% | Estimating Routing Symmetry on Single Links by Passive Flow Measurements | 201006 | Presentation|
0
| ----- | -- | **Evolution of the Internet AS-Level Ecosystem** | 201003 | Paper|
|  0/44 |  0% | Evolution of the Internet AS-Level Ecosystem | 200902 | Presentation|
0
| ----- | -- | **The Internet is Flat: Modeling the Transition from a Transit Hierarchy to a Peering Mesh** | 201012 | Paper|
|  0/88 |  0% | The Internet is Flat: Modeling the Transition from a Transit Hierarchy to a Peering Mesh | 201012 | Presentation|
0
| ----- | -- | **Measured Impact of Crooked Traceroute** | 201101 | Paper|
|  0/37 |  0% | Measured Impact of Crooked Traceroute | 201102 | Presentation|
0
| ----- | -- | **Tracking IPv6 Evolution: Data We Have and Data We Need** | 201107 | Paper|
|  0/54 |  0% | Tracking IPv6 evolution: Data We Have and Data We Need | 201108 | Presentation|
0
| ----- | -- | **Analysis of peering strategy adoption by transit providers in the Internet** | 201203 | Paper|
|  0/74 |  0% | Analysis of peering strategy adoption by transit providers in the Internet | 201205 | Presentation|
0
| ----- | -- | **Measuring the Evolution of Internet Peering Agreements** | 201205 | Paper|
|  0/54 |  0% | Measuring the Evolution of Internet Peering Agreements | 201205 | Presentation|
0
| ----- | -- | **Peering Strategy Adoption by Transit Providers in the Internet: A Game Theoretic Approach** | 201209 | Paper|
|  0/89 |  0% | Peering Strategy adoption by Transit Providers in the Internet: A Game Theoretic Approach | 201206 | Presentation|
0
| ----- | -- | **Analysis of Internet-wide Probing using Darknets** | 201210 | Paper|
|  0/48 |  0% | Analysis of Internet-wide Probing using Darknets | 201210 | Presentation|
0
| ----- | -- | **Network Cosmology** | 201211 | Paper|
|  0/17 |  0% | Network Cosmology | 201203 | Presentation|
0
| ----- | -- | **Gaining Insight into AS-level Outages through Analysis of Internet Background Radiation** | 201212 | Paper|
|  0/87 |  0% | Gaining Insight into AS-level Outages through Analysis of Internet Background Radiation | 201304 | Paper|
0
| ----- | -- | **IPv6 Alias Resolution via Induced Fragmentation** | 201303 | Paper|
|  0/47 |  0% | IPv6 Alias Resolution via Induced Fragmentation | 201303 | Presentation|
0
| ----- | -- | **A First Look at IPv4 Transfer Markets** | 201312 | Paper|
|  0/37 |  0% | A First Look at IPv4 Transfer Markets | 201312 | Presentation|
0
| ----- | -- | **Survey of End-to-End Mobile Network Measurement Testbeds** | 201411 | Paper|
|  0/56 |  0% | Survey of End-to-End Mobile Network Measurement Testbeds | 201601 | Paper|
0
| ----- | -- | **Challenges in Inferring Internet Interdomain Congestion** | 201411 | Paper|
|  0/55 |  0% | Challenges in Inferring Internet Interdomain Congestion | 201411 | Presentation|
0
| ----- | -- | **Analysis of Country-wide Internet Outages Caused by Censorship** | 201412 | Paper|
|  0/62 |  0% | Analysis of Country-wide Internet Outages Caused by Censorship | 201207 | Presentation|
0
| ----- | -- | **Measuring and Characterizing IPv6 Router Availability** | 201503 | Paper|
|  0/53 |  0% | Measuring and Characterizing IPv6 Router Availability | 201503 | Presentation|
0
| ----- | -- | **Leveraging Internet Background Radiation for Opportunistic Network Analysis** | 201510 | Paper|
|  0/75 |  0% | Leveraging Internet Background Radiation for Opportunistic Network Analysis | 201510 | Presentation|
0
| ----- | -- | **Mapping Peering Interconnections to a Facility** | 201512 | Paper|
|  0/46 |  0% | Mapping Peering Interconnections to a Facility | 201512 | Presentation|
0
| ----- | -- | **Survey of End-to-End Mobile Network Measurement Testbeds** | 201601 | Paper|
|  0/56 |  0% | Survey of End-to-End Mobile Network Measurement Testbeds | 201411 | Paper|
0
| ----- | -- | **NAT Revelio: Detecting NAT444 in the ISP** | 201603 | Paper|
|  0/40 |  0% | NAT Revelio: Detecting NAT444 in the ISP | 201603 | Presentation|
0
| ----- | -- | **Characterizing IPv6 control and data plane stability** | 201604 | Paper|
|  0/52 |  0% | Characterizing IPv6 control and data plane stability | 201604 | Presentation|
0
| ----- | -- | **Adding Enhanced Services to the Internet: Lessons from History** | 201607 | Paper|
|  0/62 |  0% | Adding Enhanced Services to the Internet: Lessons from History | 201509 | Paper|
0
| ----- | -- | **bdrmap: Inference of Borders Between IP Networks** | 201611 | Paper|
|  0/48 |  0% | bdrmap: Inference of Borders Between IP Networks | 201611 | Presentation|
0
| ----- | -- | **Millions of Targets Under Attack: a Macroscopic Characterization of the DoS Ecosystem** | 201711 | Paper|
|  0/85 |  0% | Millions of Targets Under Attack: a Macroscopic Characterization of the DoS Ecosystem | 201711 | Presentation|
0
| ----- | -- | **A Look at Router Geolocation in Public and Commercial Databases** | 201711 | Paper|
|  0/63 |  0% | A Look at Router Geolocation in Public and Commercial Databases | 201711 | Presentation|
0
| ----- | -- | **Challenges in Inferring Internet Congestion Using Throughput Measurements** | 201711 | Paper|
|  0/73 |  0% | Challenges in Inferring Internet Congestion Using Throughput Measurements | 201711 | Presentation|
0
| ----- | -- | **ARTEMIS: Neutralizing BGP Hijacking within a Minute** | 201801 | Paper|
|  0/51 |  0% | ARTEMIS: Neutralizing BGP Hijacking within a Minute | 201807 | Presentation|
0
| ----- | -- | **Policy Implications of Third-Party Measurement of Interdomain Congestion on the Internet** | 201803 | Paper|
|  0/88 |  0% | Policy Implications of Third-Party Measurement of Interdomain Congestion on the Internet | 201803 | Presentation|
0
| ----- | -- | **Studying the Evolution of Content Providers in the Internet Core** | 201806 | Paper|
|  0/64 |  0% | Studying the Evolution of Content Providers in the Internet Core | 201809 | Presentation|
0
| ----- | -- | **Inferring Persistent Interdomain Congestion** | 201808 | Paper|
|  0/43 |  0% | Inferring Persistent Interdomain Congestion | 201808 | Presentation|
0
| ----- | -- | **Dynam-IX: a Dynamic Interconnection eXchange** | 201808 | Paper|
|  0/44 |  0% | Dynam-IX: a Dynamic Interconnection eXchange | 201812 | Paper|
0
| ----- | -- | **A First Joint Look at DoS Attacks and BGP Blackholing in the Wild** | 201810 | Paper|
|  0/65 |  0% | A First Joint Look at DoS Attacks and BGP Blackholing in the Wild | 201811 | Presentation|
0
| ----- | -- | **Pushing the Boundaries with bdrmapIT: Mapping Router Ownership at Internet Scale** | 201811 | Paper|
|  0/80 |  0% | Pushing the Boundaries with bdrmapIT: Mapping Router Ownership at Internet Scale | 201811 | Presentation|
0
| ----- | -- | **Dynam-IX: a Dynamic Interconnection eXchange** | 201812 | Paper|
|  0/44 |  0% | Dynam-IX: a Dynamic Interconnection eXchange | 201808 | Paper|
0
| ----- | -- | **Stable and Practical AS Relationship Inference with ProbLink** | 201902 | Paper|
|  0/60 |  0% | Stable and Practical AS Relationship Inference with ProbLink | 201902 | Presentation|
0
| ----- | -- | **Blink: Fast Connectivity Recovery Entirely in the Data Plane** | 201902 | Paper|
|  0/60 |  0% | Blink: Fast Connectivity Recovery Entirely in the Data Plane | 201902 | Presentation|
0
| ----- | -- | **How to Find Correlated Internet Failures** | 201903 | Paper|
|  0/40 |  0% | How to find correlated Internet failures | 201903 | Presentation|
0
| ----- | -- | **Geo-Locating BGP prefixes** | 201906 | Paper|
|  0/25 |  0% | Geo-locating BGP prefixes | 201906 | Presentation|
0
| ----- | -- | **An Empirical Study of Mobile Network Behavior and Application Performance in the Wild** | 201906 | Paper|
|  0/85 |  0% | An Empirical Study of Mobile Network Behavior and Application Performance in the Wild | 201906 | Presentation|
0
| ----- | -- | **Residential Links Under the Weather** | 201908 | Paper|
|  0/35 |  0% | Residential Links Under the Weather | 201908 | Presentation|
0
| ----- | -- | **Profiling BGP Serial Hijackers: Capturing Persistent Misbehavior in the Global Routing Table** | 201910 | Paper|
|  0/92 |  0% | Profiling BGP Serial Hijackers: Capturing Persistent Misbehavior in the Global Routing Table | 201910 | Presentation|
0
| ----- | -- | **Network Hygiene, Incentives, and Regulation: Deployment of Source Address Validation in the Internet** | 201911 | Paper|
|  0/100 |  0% | Network Hygiene, Incentives, and Regulation: Deployment of Source Address Validation in the Internet | 201911 | Presentation|
0
| ----- | -- | **Challenges in Inferring Spoofed Traffic at IXPs** | 201912 | Paper|
|  0/47 |  0% | Challenges in Inferring Spoofed Traffic at IXPs | 201912 | Presentation|
0
| ----- | -- | **When parents and children disagree: Diving into DNS delegation inconsistency** | 202003 | Paper|
|  0/76 |  0% | When parents and children disagree: Diving into DNS delegation inconsistency | 202003 | Presentation|
0
| ----- | -- | **Unintended consequences: Effects of submarine cable deployment on Internet routing** | 202003 | Paper|
|  0/82 |  0% | Unintended consequences: Effects of submarine cable deployment on Internet routing | 202003 | Presentation|
0
| ----- | -- | **FlowTrace: A Framework for Active Bandwidth Measurements using In-band Packet Trains** | 202003 | Paper|
|  0/84 |  0% | FlowTrace: A Framework for Active Bandwidth Measurements using In-band Packet Trains | 202003 | Presentation|
0
| ----- | -- | **To Filter or not to Filter: Measuring the Benefits of Registering in the RPKI Today** | 202003 | Paper|
|  0/83 |  0% | To Filter or not to Filter: Measuring the Benefits of Registering in the RPKI Today | 202003 | Presentation|
0
| ----- | -- | **APPLE: Alias Pruning by Path Length Estimation** | 202003 | Paper|
|  0/46 |  0% | APPLE: Alias Pruning by Path Length Estimation | 202003 | Presentation|
0
| ----- | -- | **vrfinder: Finding Outbound Addresses in Traceroute** | 202006 | Paper|
|  0/50 |  0% | vrfinder: Finding Outbound Addresses in Traceroute | 202006 | Presentation|
0
| ----- | -- | **Trufflehunter: Cache Snooping Rare Domains at Large Public DNS Resolvers** | 202010 | Paper|
|  0/72 |  0% | Trufflehunter: Cache Snooping Rare Domains at Large Public DNS Resolvers | 202010 | Presentation|
0
| ----- | -- | **Learning to Extract and Use ASNs in Hostnames** | 202010 | Paper|
|  0/45 |  0% | Learning to Extract and Use ASNs in Hostnames | 202010 | Presentation|
0
| ----- | -- | **Measuring the impact of COVID-19 on cloud network performance** | 202011 | Paper|
|  0/61 |  0% | Measuring the impact of COVID-19 on cloud network performance | 202011 | Presentation|
0
| ----- | -- | **Trust Zones: A Path to a More Secure Internet Infrastructure** | 202102 | Paper|
|  0/60 |  0% | Trust Zones: A Path to a More Secure Internet Infrastructure | 202108 | Paper|
0
| ----- | -- | **Trust Zones: A Path to a More Secure Internet Infrastructure** | 202108 | Paper|
|  0/60 |  0% | Trust Zones: A Path to a More Secure Internet Infrastructure | 202102 | Paper|
0
| ----- | -- | **Risky BIZness: Risks Derived from Registrar Name Management** | 202111 | Paper|
|  0/59 |  0% | Risky BIZness: Risks Derived from Registrar Name Management | 202109 | Presentation|
0
| ----- | -- | **Measuring the network performance of Google Cloud Platform** | 202111 | Paper|
|  0/58 |  0% | Measuring the network performance of Google Cloud Platform | 202111 | Presentation|
0
| ----- | -- | **Learning to Extract Geographic Information from Internet Router Hostnames** | 202112 | Paper|
|  0/73 |  0% | Learning to Extract Geographic Information from Internet Router Hostnames | 202112 | Presentation|
0
| ----- | -- | **Jitterbug: A new framework for jitter-based congestion inference** | 202203 | Paper|
|  0/64 |  0% | Jitterbug: A new framework for jitter-based congestion inference | 202203 | Presentation|
0
| ----- | -- | **Design and Implementation of Web-based Speed Test Analysis Tool Kit** | 202203 | Paper|
|  0/67 |  0% | Design and Implementation of Web-based Speed Test Analysis Tool Kit | 202203 | Presentation|
0
| ----- | -- | **Stop, DROP, and ROA: Effectiveness of Defenses through the lens of DROP** | 202210 | Paper|
|  0/71 |  0% | Stop, DROP, and ROA: Effectiveness of Defenses through the lens of DROP | 202210 | Presentation|
0
| ----- | -- | **Retroactive Identification of Targeted DNS Infrastructure Hijacking** | 202210 | Paper|
|  0/67 |  0% | Retroactive Identification of Targeted DNS Infrastructure Hijacking | 202210 | Presentation|
0
| ----- | -- | **Mind Your MANRS: Measuring the MANRS Ecosystem** | 202210 | Paper|
|  0/46 |  0% | Mind Your MANRS: Measuring the MANRS Ecosystem | 202210 | Presentation|
0
| ----- | -- | **Investigating the impact of DDoS attacks on DNS infrastructure** | 202210 | Paper|
|  0/62 |  0% | Investigating the impact of DDoS attacks on DNS infrastructure | 202210 | Presentation|
