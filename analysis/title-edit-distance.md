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
27
| ----- | -- | **Internet Topology Data Comparison** | 201205 | Paper|
|  9/ 1 | 27% | Internet Topology Data Kit | 201102 | Presentation|
25
| ----- | -- | **Otter: A general-purpose network visualization tool** | 199906 | Paper|
| 13/ 1 | 25% | Otter: General Purpose Network Viz Tool | 199808 | Presentation|
25
| ----- | -- | **A Basis for Systematic Analysis of Network Topologies: Technical Report** | 200604 | Paper|
| 18/ 1 | 25% | A Basis for Systematic Analysis of Network Topologies | 200605 | Presentation|
24
| ----- | -- | **Third Accountability and Transparency Review Team (ATRT3) Report - Minority Statement** | 202005 | Paper|
| 21/ 1 | 24% | Third Accountability and Transparency Review Team (ATRT3) Report | 202005 | Paper|
23
| ----- | -- | **Impact of Degree Correlations on Topology Generators** | 200508 | Paper|
| 12/ 1 | 23% | Degree correlations and topology generators | 200503 | Presentation|
23
| ----- | -- | **BGPStream: a software framework for live and historical BGP data analysis** | 201510 | Paper|
| 17/ 1 | 23% | BGPStream - An Open Source Framework for Live/Historical BGP Data Analysis | 201505 | Presentation|
22
| ----- | -- | **CAIDA: Visualizing the Internet** | 200101 | Paper|
|  7/ 1 | 22% | AS Core: Visualizing the Internet | 201103 | Presentation|
20
| ----- | -- | **A Robust System for Accurate Real-time Summaries of Internet Traffic: Technical Report** | 200506 | Paper|
| 18/ 2 | 20% | A Robust System for Accurate Real-time Summaries of Internet Traffic | 200506 | Paper|
| 18/ 2 | 20% | A Robust System for Accurate Real-time Summaries of Internet Traffic | 200506 | Presentation|
20
| ----- | -- | **Evolution of the Internet AS-Level Ecosystem** | 200902 | Paper|
|  9/ 1 | 20% | Evolution of the Internet Ecosystem | 200910 | Presentation|
20
| ----- | -- | **Experience in using MTurk for Network Measurement** | 201508 | Paper|
| 10/ 1 | 20% | Experience in using Mechanical Turk for Network Measurement | 201508 | Presentation|
20
| ----- | -- | **Toward a Theory of Harms in the Internet Ecosystem** | 201909 | Paper|
| 10/ 1 | 20% | Toward a theory of harms in the Internet | 201909 | Presentation|
19
| ----- | -- | **Two Days in the Life of the DNS Anycast Root Servers** | 200704 | Paper|
| 10/ 1 | 19% | Two days in the life of three DNS root servers | 200611 | Presentation|
18
| ----- | -- | **Inferring BGP Blackholing Activity in the Internet** | 201711 | Paper|
|  9/ 1 | 18% | Inferring BGP Blackholing in the Internet | 201711 | Presentation|
17
| ----- | -- | **Greedy Forwarding in Dynamic Scale-Free Networks Embedded in Hyperbolic Metric Spaces: Technical Report** | 200907 | Paper|
| 26/ 2 | 25% | Greedy Forwarding in Scale-Free Networks Embedded in Hyperbolic Metric Spaces | 200909 | Paper|
| 18/ 2 | 17% | Greedy Forwarding in Dynamic Scale-Free Networks Embedded in Hyperbolic Metric Spaces | 201003 | Paper|
15
| ----- | -- | **Systematic Topology Analysis and Generation Using Degree Correlations** | 200609 | Paper|
| 11/ 1 | 15% | dK-series: Systematic Topology Analysis and Generation Using Degree Correlations | 200606 | Presentation|
15
| ----- | -- | **Annotated Schema: Mapping Ontologies onto Dataset Schemas** | 202305 | Paper|
|  9/ 1 | 15% | Annotated Schema: Mapping Ontologies onto Dataset Schemas Slideset | 202305 | Presentation|
11
| ----- | -- | **Where .ru? Assessing the Impact of Conflict on Russian Domain Infrastructure** | 202210 | Paper|
|  9/ 1 | 11% | Where .ru? Assessing the Impact of Conflict on Russian Domain Infrastructure Slideset | 202210 | Presentation|
10
| ----- | -- | **Learning Regexes to Extract Router Names from Hostnames** | 201910 | Paper|
|  8/ 2 | 14% | Learning to Extract Router Names from Hostnames | 201910 | Presentation|
|  6/ 2 | 10% | Learning Regexes to Extract Network Names from Hostnames | 202112 | Paper|
10
| ----- | -- | **Internet-Scale IPv4 Alias Resolution with MIDAR** | 201304 | Paper|
|  5/ 1 | 10% | Internet-Scale Alias Resolution with MIDAR | 201002 | Presentation|
6
| ----- | -- | **The 10th Workshop on Active Internet Measurements (AIMS-10) Report** | 201810 | Paper|
|  4/ 1 |  6% | The 9th Workshop on Active Internet Measurements (AIMS-9) Report | 201710 | Paper|
4
| ----- | -- | **The 8th Workshop on Active Internet Measurements (AIMS8) Report** | 201610 | Paper|
|  3/ 2 |  4% | The 9th Workshop on Active Internet Measurements (AIMS-9) Report | 201710 | Paper|
|  3/ 2 |  4% | The 7th Workshop on Active Internet Measurements (AIMS-7) Report | 201601 | Paper|
4
| ----- | -- | **The 9th Workshop on Active Internet Measurements (AIMS-9) Report** | 201710 | Paper|
|  3/ 2 |  4% | The 8th Workshop on Active Internet Measurements (AIMS8) Report | 201610 | Paper|
|  4/ 2 |  6% | The 10th Workshop on Active Internet Measurements (AIMS-10) Report | 201810 | Paper|
4
| ----- | -- | **The 7th Workshop on Active Internet Measurements (AIMS-7) Report** | 201601 | Paper|
|  3/ 1 |  4% | The 8th Workshop on Active Internet Measurements (AIMS8) Report | 201610 | Paper|
4
| ----- | -- | **MAnycast2 - Using Anycast to Measure Anycast** | 202010 | Paper|
|  2/ 1 |  4% | MAnycast2 Using Anycast to Measure Anycast | 202010 | Presentation|
3
| ----- | -- | **Streams, Flows and Torrents** | 200104 | Paper|
|  1/ 1 |  3% | Streams Flows and Torrents | 200104 | Presentation|
3
| ----- | -- | **A Framework for Understanding and Applying Ethical Principles in Network and Security Research ** | 201001 | Paper|
|  3/ 1 |  3% | Framework for Understanding and Applying Ethical Principles in Network and Security Research | 201001 | Presentation|
3
| ----- | -- | **Inferring Multilateral Peering** | 201312 | Paper|
|  1/ 1 |  3% | Inferring Multilateral Peering  | 201312 | Presentation|
2
| ----- | -- | **Percolation in Self-Similar Networks ** | 201101 | Paper|
|  1/ 2 |  2% | Percolation in self-similar networks | 201106 | Presentation|
|  1/ 2 |  2% | Percolation in self-similar networks | 201103 | Presentation|
2
| ----- | -- | **Named Data Networking Next Phase (NDN-NP) Project May 2014 - April 2015 Annual Report** | 201506 | Paper|
|  2/ 2 |  2% | Named Data Networking Next Phase (NDN-NP) Project May 2016 - April 2017 Annual Report | 201711 | Paper|
|  2/ 2 |  2% | Named Data Networking Next Phase (NDN-NP) Project May 2015 - April 2016 Annual Report | 201606 | Paper|
2
| ----- | -- | **Periscope: Unifying Looking Glass Querying** | 201603 | Paper|
|  1/ 2 |  2% | Periscope:Unifying Looking Glass Querying | 201603 | Presentation|
|  1/ 2 |  2% | Periscope: Unifying Looking Glass querying  | 201512 | Presentation|
2
| ----- | -- | **Named Data Networking Next Phase (NDN-NP) Project May 2015 - April 2016 Annual Report** | 201606 | Paper|
|  2/ 2 |  2% | Named Data Networking Next Phase (NDN-NP) Project May 2014 - April 2015 Annual Report | 201506 | Paper|
|  2/ 2 |  2% | Named Data Networking Next Phase (NDN-NP) Project May 2016 - April 2017 Annual Report | 201711 | Paper|
2
| ----- | -- | **Named Data Networking Next Phase (NDN-NP) Project May 2016 - April 2017 Annual Report** | 201711 | Paper|
|  2/ 2 |  2% | Named Data Networking Next Phase (NDN-NP) Project May 2014 - April 2015 Annual Report | 201506 | Paper|
|  2/ 2 |  2% | Named Data Networking Next Phase (NDN-NP) Project May 2015 - April 2016 Annual Report | 201606 | Paper|
2
| ----- | -- | **Understanding and preparing for DNS evolution ** | 201004 | Paper|
|  1/ 1 |  2% | Understanding and Preparing for DNS Evolution | 201004 | Presentation|
2
| ----- | -- | **One-way Traffic Monitoring with iatmon** | 201203 | Paper|
|  1/ 1 |  2% | One way Traffic Monitoring with iatmon | 201205 | Presentation|
2
| ----- | -- | **AS Relationships, Customer Cones, and Validation** | 201310 | Paper|
|  1/ 1 |  2% | AS Relationships, Customer Cones, and Validation  | 201310 | Presentation|
2
| ----- | -- | **A Second Look at Detecting Third-Party Addresses in Traceroute Traces with the IP Timestamp Option** | 201403 | Paper|
|  2/ 1 |  2% | A second look at ‟Detecting third-party addresses in traceroute traces with the IP timestamp option“ | 201403 | Presentation|
2
| ----- | -- | **IPv6 AS Relationships, Cliques, and Congruence** | 201503 | Paper|
|  1/ 1 |  2% | IPv6 AS Relationships, Clique, and Congruence | 201503 | Presentation|
1
| ----- | -- | **Workshop on Internet Economics (WIE2017) Final Report** | 201807 | Paper|
|  1/ 2 |  1% | Workshop on Internet Economics (WIE2016) Final Report | 201707 | Paper|
|  1/ 2 |  1% | Workshop on Internet Economics (WIE2018) Final Report | 201904 | Paper|
1
| ----- | -- | **Measuring the Deployment of IPv6: Topology, Routing and Performance** | 201211 | Paper|
|  1/ 1 |  1% | Measuring the Deployment of IPv6: Topology, Routing, and Performance | 201211 | Presentation|
1
| ----- | -- | **Workshop on Internet Economics (WIE2016) Final Report** | 201707 | Paper|
|  1/ 1 |  1% | Workshop on Internet Economics (WIE2017) Final Report | 201807 | Paper|
1
| ----- | -- | **PacketLab: A Universal Measurement Endpoint Interface** | 201711 | Paper|
|  1/ 1 |  1% | PacketLab:A Universal Measurement Endpoint Interface | 201711 | Presentation|
1
| ----- | -- | **Workshop on Internet Economics (WIE2018) Final Report** | 201904 | Paper|
|  1/ 1 |  1% | Workshop on Internet Economics (WIE2017) Final Report | 201807 | Paper|
0
| ----- | -- | **Popularity versus Similarity in Growing Networks** | 201209 | Paper|
|  0/ 6 |  0% | Popularity versus Similarity in Growing Networks | 201211 | Presentation|
|  0/ 6 |  0% | Popularity versus Similarity in Growing Networks | 201110 | Presentation|
|  0/ 6 |  0% | Popularity versus Similarity in Growing Networks | 201111 | Presentation|
|  0/ 6 |  0% | Popularity versus Similarity in Growing Networks | 201203 | Presentation|
|  0/ 6 |  0% | Popularity versus Similarity in Growing Networks | 201202 | Presentation|
|  0/ 6 |  0% | Popularity versus Similarity in Growing Networks | 201303 | Presentation|
0
| ----- | -- | **Hyperbolic Geometry of Complex Networks** | 201010 | Paper|
|  0/ 4 |  0% | Hyperbolic geometry of complex networks | 201005 | Presentation|
|  0/ 4 |  0% | Hyperbolic geometry of complex networks | 200910 | Presentation|
|  0/ 4 |  0% | Hyperbolic geometry of complex networks | 201104 | Presentation|
|  6/ 4 | 15% | Hyperbolic geometry of large networks | 201202 | Presentation|
0
| ----- | -- | **Greedy Forwarding in Dynamic Scale-Free Networks Embedded in Hyperbolic Metric Spaces** | 201003 | Paper|
|  0/ 3 |  0% | Greedy Forwarding in Dynamic Scale-Free Networks Embedded in Hyperbolic Metric Spaces | 201003 | Presentation|
| 18/ 3 | 21% | Greedy Forwarding in Dynamic Scale-Free Networks Embedded in Hyperbolic Metric Spaces: Technical Report | 200907 | Paper|
|  8/ 3 |  9% | Greedy Forwarding in Scale-Free Networks Embedded in Hyperbolic Metric Spaces | 200906 | Presentation|
0
| ----- | -- | **Analysis of Country-wide Internet Outages Caused by Censorship** | 201111 | Paper|
|  0/ 3 |  0% | Analysis of Country-wide Internet Outages Caused by Censorship | 201207 | Presentation|
|  0/ 3 |  0% | Analysis of Country-wide Internet Outages Caused by Censorship | 201111 | Presentation|
|  0/ 3 |  0% | Analysis of Country-wide Internet Outages Caused by Censorship | 201112 | Presentation|
0
| ----- | -- | **Lost in Space: Improving Inference of IPv4 Address Space Utilization** | 201509 | Paper|
|  0/ 3 |  0% | Lost in Space: Improving Inference of IPv4 Address Space Utilization | 201410 | Paper|
|  0/ 3 |  0% | Lost in Space: Improving Inference of IPv4 Address Space Utilization | 201510 | Presentation|
|  0/ 3 |  0% | Lost in Space: Improving Inference of IPv4 Address Space Utilization | 201606 | Paper|
0
| ----- | -- | **ARTEMIS: Neutralizing BGP Hijacking within a Minute** | 201812 | Paper|
|  0/ 3 |  0% | ARTEMIS: Neutralizing BGP Hijacking within a Minute | 201807 | Presentation|
|  0/ 3 |  0% | ARTEMIS: Neutralizing BGP Hijacking within a Minute | 201803 | Presentation|
|  0/ 3 |  0% | ARTEMIS: Neutralizing BGP Hijacking within a Minute | 201805 | Presentation|
0
| ----- | -- | **IRR Hygiene in the RPKI Era** | 202203 | Paper|
|  0/ 3 |  0% | IRR Hygiene in the RPKI Era | 202111 | Paper|
|  0/ 3 |  0% | IRR Hygiene in the RPKI Era | 202110 | Presentation|
|  0/ 3 |  0% | IRR Hygiene in the RPKI Era | 202203 | Presentation|
0
| ----- | -- | **DNS Root/gTLD Performance Measurements** | 200112 | Paper|
|  0/ 2 |  0% | DNS Root/gTLD Performance Measurements | 200112 | Presentation|
|  6/ 2 | 15% | DNS/gTLD Performance Measurements  | 200112 | Presentation|
0
| ----- | -- | **Building a Better NetFlow** | 200409 | Paper|
|  0/ 2 |  0% | Building a Better NetFlow | 200409 | Presentation|
|  0/ 2 |  0% | Building a Better NetFlow | 200408 | Presentation|
0
| ----- | -- | **A Robust System for Accurate Real-time Summaries of Internet Traffic** | 200506 | Paper|
| 18/ 2 | 26% | A Robust System for Accurate Real-time Summaries of Internet Traffic: Technical Report | 200506 | Paper|
|  0/ 2 |  0% | A Robust System for Accurate Real-time Summaries of Internet Traffic | 200506 | Presentation|
0
| ----- | -- | **Navigability of Complex Networks** | 200901 | Paper|
|  0/ 2 |  0% | Navigability of complex networks | 201001 | Presentation|
|  8/ 2 | 25% | Navigability of Networks | 201005 | Presentation|
0
| ----- | -- | **Identification of influential spreaders in complex networks** | 201008 | Paper|
|  0/ 2 |  0% | Identification of Influential Spreaders in Complex Networks | 201103 | Presentation|
|  0/ 2 |  0% | Identification of Influential Spreaders in Complex Networks | 201005 | Presentation|
0
| ----- | -- | **A Value-based Framework for Internet Peering Agreements** | 201010 | Paper|
|  0/ 2 |  0% | A Value-based Framework for Internet Peering Agreements | 201009 | Presentation|
|  1/ 2 |  1% | A Value-based Framework for Internet Peering Agreements  | 201006 | Presentation|
0
| ----- | -- | **Extracting benefit from harm: using malware pollution to analyze the impact of political and geophysical events on the Internet** | 201201 | Paper|
|  0/ 2 |  0% | Extracting Benefit from Harm: Using Malware Pollution to Analyze the Impact of Political and Geophysical Events on the Internet | 201208 | Presentation|
|  0/ 2 |  0% | Extracting Benefit from Harm: Using Malware Pollution to Analyze the Impact of Political and Geophysical Events on the Internet | 201201 | Presentation|
0
| ----- | -- | **Analysis of a "/0" Stealth Scan from a Botnet** | 201211 | Paper|
|  0/ 2 |  0% | Analysis of a "/0" Stealth Scan from a Botnet | 201504 | Paper|
|  0/ 2 |  0% | Analysis of a "/0" Stealth Scan from a Botnet | 201211 | Presentation|
0
| ----- | -- | **Gaining Insight into AS-level Outages through Analysis of Internet Background Radiation** | 201304 | Paper|
|  0/ 2 |  0% | Gaining Insight into AS-level Outages through Analysis of Internet Background Radiation | 201212 | Paper|
|  0/ 2 |  0% | Gaining Insight into AS-level Outages through Analysis of Internet Background Radiation | 201304 | Presentation|
0
| ----- | -- | **Lost in Space: Improving Inference of IPv4 Address Space Utilization** | 201410 | Paper|
|  0/ 2 |  0% | Lost in Space: Improving Inference of IPv4 Address Space Utilization | 201606 | Paper|
|  0/ 2 |  0% | Lost in Space: Improving Inference of IPv4 Address Space Utilization | 201509 | Paper|
0
| ----- | -- | **Analysis of a "/0" Stealth Scan from a Botnet** | 201504 | Paper|
|  0/ 2 |  0% | Analysis of a "/0" Stealth Scan from a Botnet | 201211 | Paper|
|  0/ 2 |  0% | Analysis of a "/0" Stealth Scan from a Botnet | 201211 | Presentation|
0
| ----- | -- | **Adding Enhanced Services to the Internet: Lessons from History** | 201509 | Paper|
|  0/ 2 |  0% | Adding Enhanced Services to the Internet: Lessons from History | 201607 | Paper|
|  0/ 2 |  0% | Adding Enhanced Services to the Internet: Lessons from History | 201509 | Presentation|
0
| ----- | -- | **Lost in Space: Improving Inference of IPv4 Address Space Utilization** | 201606 | Paper|
|  0/ 2 |  0% | Lost in Space: Improving Inference of IPv4 Address Space Utilization | 201410 | Paper|
|  0/ 2 |  0% | Lost in Space: Improving Inference of IPv4 Address Space Utilization | 201509 | Paper|
0
| ----- | -- | **BGPStream: a software framework for live and historical BGP data analysis** | 201611 | Paper|
|  0/ 2 |  0% | BGPStream: A Software Framework for Live and Historical BGP Data Analysis | 201611 | Presentation|
|  1/ 2 |  1% | BGPStream: A Software Framework for Live and Historical BGP Data Analysis  | 201703 | Presentation|
0
| ----- | -- | **Detecting Peering Infrastructure Outages in the Wild** | 201708 | Paper|
|  0/ 2 |  0% | Detecting Peering Infrastructure Outages in the Wild | 201708 | Presentation|
|  0/ 2 |  0% | Detecting Peering Infrastructure Outages in the Wild | 201712 | Presentation|
0
| ----- | -- | **TCP Congestion Signatures** | 201711 | Paper|
|  0/ 2 |  0% | TCP Congestion Signatures | 201711 | Presentation|
|  0/ 2 |  0% | TCP Congestion Signatures | 201807 | Presentation|
0
| ----- | -- | **Investigating the Causes of Congestion on the African IXP substrate** | 201711 | Paper|
|  0/ 2 |  0% | Investigating the Causes of Congestion on the African IXP substrate | 201811 | Presentation|
|  0/ 2 |  0% | Investigating the Causes of Congestion on the African IXP substrate | 201711 | Presentation|
0
| ----- | -- | **Unresolved Issues: Prevalence, Persistence, and Perils of Lame Delegations** | 202010 | Paper|
|  8/ 2 | 10% | Unresolved Issues: Prevalence, Persistence, and Perils of Lame Delegations (Video) | 202010 | Media|
|  0/ 2 |  0% | Unresolved Issues: Prevalence, Persistence, and Perils of Lame Delegations | 202010 | Presentation|
0
| ----- | -- | **DynamIPs: Analyzing address assignment practices in IPv4 and IPv6** | 202012 | Paper|
|  8/ 2 | 12% | DynamIPs: Analyzing address assignment practices in IPv4 and IPv6 (Video) | 202012 | Media|
|  0/ 2 |  0% | DynamIPs: Analyzing address assignment practices in IPv4 and IPv6 | 202012 | Presentation|
0
| ----- | -- | **Challenges in measuring the Internet for the public Interest** | 202108 | Paper|
|  0/ 2 |  0% | Challenges in measuring the Internet for the public Interest | 202205 | Paper|
|  0/ 2 |  0% | Challenges in measuring the Internet for the public Interest | 202109 | Presentation|
0
| ----- | -- | **IRR Hygiene in the RPKI Era** | 202111 | Paper|
|  0/ 2 |  0% | IRR Hygiene in the RPKI Era | 202203 | Paper|
|  0/ 2 |  0% | IRR Hygiene in the RPKI Era | 202110 | Presentation|
0
| ----- | -- | **Learning Regexes to Extract Network Names from Hostnames** | 202112 | Paper|
|  6/ 2 | 10% | Learning Regexes to Extract Router Names from Hostnames | 201910 | Paper|
|  0/ 2 |  0% | Learning Regexes to Extract Network Names from Hostnames | 202112 | Presentation|
0
| ----- | -- | **Challenges in measuring the Internet for the public Interest** | 202205 | Paper|
|  0/ 2 |  0% | Challenges in measuring the Internet for the public Interest | 202108 | Paper|
|  0/ 2 |  0% | Challenges in measuring the Internet for the public Interest | 202109 | Presentation|
0
| ----- | -- | **GTrace - A Graphical Traceroute Tool** | 199911 | Paper|
|  0/ 1 |  0% | GTrace - A Graphical Traceroute Tool | 199911 | Presentation|
0
| ----- | -- | **Internet Expansion, Refinement, and Churn** | 200201 | Paper|
|  0/ 1 |  0% | Internet expansion, refinement, and churn | 200202 | Presentation|
0
| ----- | -- | **Distance Metrics in the Internet** | 200209 | Paper|
|  0/ 1 |  0% | Distance metrics in the Internet | 200209 | Presentation|
0
| ----- | -- | **Traceroute and BGP AS Path Incongruities** | 200303 | Paper|
|  0/ 1 |  0% | Traceroute and BGP AS Path Incongruities | 200306 | Presentation|
0
| ----- | -- | **Internet Quarantine: Requirements for Containing Self-Propagating Code** | 200304 | Paper|
|  0/ 1 |  0% | Internet Quarantine: Requirements for Containing Self-Propagating Code | 200304 | Presentation|
0
| ----- | -- | **On Third-party Addresses in Traceroute Paths** | 200304 | Paper|
|  0/ 1 |  0% | On Third-party Addresses in Traceroute Paths | 200304 | Presentation|
0
| ----- | -- | **Their share: diversity and disparity in IP traffic** | 200404 | Paper|
|  0/ 1 |  0% | Their Share: Diversity and Disparity in IP Traffic | 200404 | Presentation|
0
| ----- | -- | **The Spread of the Witty Worm** | 200408 | Paper|
|  0/ 1 |  0% | The Spread of the Witty Worm | 200407 | Presentation|
0
| ----- | -- | **Revisiting Internet AS-level Topology Discovery** | 200503 | Paper|
|  0/ 1 |  0% | Revisiting Internet AS-level Topology Discovery | 200503 | Presentation|
0
| ----- | -- | **Spectroscopy of traceroute delays** | 200503 | Paper|
|  0/ 1 |  0% | Spectroscopy of Traceroute Delays | 200503 | Presentation|
0
| ----- | -- | **Comparison of Public End-to-End Bandwidth Estimation Tools on High-Speed Links** | 200503 | Paper|
|  0/ 1 |  0% | Comparison of Public End-to-End Bandwidth Estimation tools on High-Speed Links | 200503 | Presentation|
0
| ----- | -- | **Inferring AS Relationships: Dead End or Lively Beginning?** | 200505 | Paper|
|  0/ 1 |  0% | Inferring AS Relationships: Dead End or Lively Beginning? | 200505 | Presentation|
0
| ----- | -- | **Passive Monitoring of DNS Anomalies** | 200707 | Paper|
|  0/ 1 |  0% | Passive Monitoring of DNS Anomalies | 200707 | Presentation|
0
| ----- | -- | **Traceroute Probe Method and Forward IP Path Inference** | 200810 | Paper|
|  0/ 1 |  0% | Traceroute Probe Method and Forward IP Path Inference | 200810 | Presentation|
0
| ----- | -- | **Greedy Forwarding in Scale-Free Networks Embedded in Hyperbolic Metric Spaces** | 200909 | Paper|
|  0/ 1 |  0% | Greedy Forwarding in Scale-Free Networks Embedded in Hyperbolic Metric Spaces | 200906 | Presentation|
0
| ----- | -- | **An Internet Data Sharing Framework For Balancing Privacy and Utility** | 200910 | Paper|
|  0/ 1 |  0% | An Internet Data Sharing Framework For Balancing Privacy and Utility | 200910 | Presentation|
0
| ----- | -- | **Estimating Routing Symmetry on Single Links by Passive Flow Measurements** | 201003 | Paper|
|  0/ 1 |  0% | Estimating Routing Symmetry on Single Links by Passive Flow Measurements | 201006 | Presentation|
0
| ----- | -- | **Evolution of the Internet AS-Level Ecosystem** | 201003 | Paper|
|  0/ 1 |  0% | Evolution of the Internet AS-Level Ecosystem | 200902 | Presentation|
0
| ----- | -- | **The Internet is Flat: Modeling the Transition from a Transit Hierarchy to a Peering Mesh** | 201012 | Paper|
|  0/ 1 |  0% | The Internet is Flat: Modeling the Transition from a Transit Hierarchy to a Peering Mesh | 201012 | Presentation|
0
| ----- | -- | **Measured Impact of Crooked Traceroute** | 201101 | Paper|
|  0/ 1 |  0% | Measured Impact of Crooked Traceroute | 201102 | Presentation|
0
| ----- | -- | **Tracking IPv6 Evolution: Data We Have and Data We Need** | 201107 | Paper|
|  0/ 1 |  0% | Tracking IPv6 evolution: Data We Have and Data We Need | 201108 | Presentation|
0
| ----- | -- | **Analysis of peering strategy adoption by transit providers in the Internet** | 201203 | Paper|
|  0/ 1 |  0% | Analysis of peering strategy adoption by transit providers in the Internet | 201205 | Presentation|
0
| ----- | -- | **Measuring the Evolution of Internet Peering Agreements** | 201205 | Paper|
|  0/ 1 |  0% | Measuring the Evolution of Internet Peering Agreements | 201205 | Presentation|
0
| ----- | -- | **Peering Strategy Adoption by Transit Providers in the Internet: A Game Theoretic Approach** | 201209 | Paper|
|  0/ 1 |  0% | Peering Strategy adoption by Transit Providers in the Internet: A Game Theoretic Approach | 201206 | Presentation|
0
| ----- | -- | **Analysis of Internet-wide Probing using Darknets** | 201210 | Paper|
|  0/ 1 |  0% | Analysis of Internet-wide Probing using Darknets | 201210 | Presentation|
0
| ----- | -- | **Network Cosmology** | 201211 | Paper|
|  0/ 1 |  0% | Network Cosmology | 201203 | Presentation|
0
| ----- | -- | **Gaining Insight into AS-level Outages through Analysis of Internet Background Radiation** | 201212 | Paper|
|  0/ 1 |  0% | Gaining Insight into AS-level Outages through Analysis of Internet Background Radiation | 201304 | Paper|
0
| ----- | -- | **IPv6 Alias Resolution via Induced Fragmentation** | 201303 | Paper|
|  0/ 1 |  0% | IPv6 Alias Resolution via Induced Fragmentation | 201303 | Presentation|
0
| ----- | -- | **Speedtrap: Internet-Scale IPv6 Alias Resolution** | 201310 | Paper|
|  0/ 1 |  0% | Speedtrap: Internet-Scale IPv6 Alias Resolution | 201310 | Presentation|
0
| ----- | -- | **A First Look at IPv4 Transfer Markets** | 201312 | Paper|
|  0/ 1 |  0% | A First Look at IPv4 Transfer Markets | 201312 | Presentation|
0
| ----- | -- | **A Coordinated View of the Temporal Evolution of Large-scale Internet Events** | 201401 | Paper|
|  0/ 1 |  0% | A Coordinated View of the Temporal Evolution of Large-scale Internet Events | 201401 | Media|
0
| ----- | -- | **Survey of End-to-End Mobile Network Measurement Testbeds** | 201411 | Paper|
|  0/ 1 |  0% | Survey of End-to-End Mobile Network Measurement Testbeds | 201601 | Paper|
0
| ----- | -- | **Challenges in Inferring Internet Interdomain Congestion** | 201411 | Paper|
|  0/ 1 |  0% | Challenges in Inferring Internet Interdomain Congestion | 201411 | Presentation|
0
| ----- | -- | **Analysis of Country-wide Internet Outages Caused by Censorship** | 201412 | Paper|
|  0/ 1 |  0% | Analysis of Country-wide Internet Outages Caused by Censorship | 201207 | Presentation|
0
| ----- | -- | **Measuring and Characterizing IPv6 Router Availability** | 201503 | Paper|
|  0/ 1 |  0% | Measuring and Characterizing IPv6 Router Availability | 201503 | Presentation|
0
| ----- | -- | **Leveraging Internet Background Radiation for Opportunistic Network Analysis** | 201510 | Paper|
|  0/ 1 |  0% | Leveraging Internet Background Radiation for Opportunistic Network Analysis | 201510 | Presentation|
0
| ----- | -- | **Mapping Peering Interconnections to a Facility** | 201512 | Paper|
|  0/ 1 |  0% | Mapping Peering Interconnections to a Facility | 201512 | Presentation|
0
| ----- | -- | **Survey of End-to-End Mobile Network Measurement Testbeds** | 201601 | Paper|
|  0/ 1 |  0% | Survey of End-to-End Mobile Network Measurement Testbeds | 201411 | Paper|
0
| ----- | -- | **NAT Revelio: Detecting NAT444 in the ISP** | 201603 | Paper|
|  0/ 1 |  0% | NAT Revelio: Detecting NAT444 in the ISP | 201603 | Presentation|
0
| ----- | -- | **Characterizing IPv6 control and data plane stability** | 201604 | Paper|
|  0/ 1 |  0% | Characterizing IPv6 control and data plane stability | 201604 | Presentation|
0
| ----- | -- | **Adding Enhanced Services to the Internet: Lessons from History** | 201607 | Paper|
|  0/ 1 |  0% | Adding Enhanced Services to the Internet: Lessons from History | 201509 | Paper|
0
| ----- | -- | **bdrmap: Inference of Borders Between IP Networks** | 201611 | Paper|
|  0/ 1 |  0% | bdrmap: Inference of Borders Between IP Networks | 201611 | Presentation|
0
| ----- | -- | **Millions of Targets Under Attack: a Macroscopic Characterization of the DoS Ecosystem** | 201711 | Paper|
|  0/ 1 |  0% | Millions of Targets Under Attack: a Macroscopic Characterization of the DoS Ecosystem | 201711 | Presentation|
0
| ----- | -- | **A Look at Router Geolocation in Public and Commercial Databases** | 201711 | Paper|
|  0/ 1 |  0% | A Look at Router Geolocation in Public and Commercial Databases | 201711 | Presentation|
0
| ----- | -- | **Challenges in Inferring Internet Congestion Using Throughput Measurements** | 201711 | Paper|
|  0/ 1 |  0% | Challenges in Inferring Internet Congestion Using Throughput Measurements | 201711 | Presentation|
0
| ----- | -- | **ARTEMIS: Neutralizing BGP Hijacking within a Minute** | 201801 | Paper|
|  0/ 1 |  0% | ARTEMIS: Neutralizing BGP Hijacking within a Minute | 201807 | Presentation|
0
| ----- | -- | **Policy Implications of Third-Party Measurement of Interdomain Congestion on the Internet** | 201803 | Paper|
|  0/ 1 |  0% | Policy Implications of Third-Party Measurement of Interdomain Congestion on the Internet | 201803 | Presentation|
0
| ----- | -- | **Studying the Evolution of Content Providers in the Internet Core** | 201806 | Paper|
|  0/ 1 |  0% | Studying the Evolution of Content Providers in the Internet Core | 201809 | Presentation|
0
| ----- | -- | **Inferring Persistent Interdomain Congestion** | 201808 | Paper|
|  0/ 1 |  0% | Inferring Persistent Interdomain Congestion | 201808 | Presentation|
0
| ----- | -- | **Dynam-IX: a Dynamic Interconnection eXchange** | 201808 | Paper|
|  0/ 1 |  0% | Dynam-IX: a Dynamic Interconnection eXchange | 201812 | Paper|
0
| ----- | -- | **A First Joint Look at DoS Attacks and BGP Blackholing in the Wild** | 201810 | Paper|
|  0/ 1 |  0% | A First Joint Look at DoS Attacks and BGP Blackholing in the Wild | 201811 | Presentation|
0
| ----- | -- | **Pushing the Boundaries with bdrmapIT: Mapping Router Ownership at Internet Scale** | 201811 | Paper|
|  0/ 1 |  0% | Pushing the Boundaries with bdrmapIT: Mapping Router Ownership at Internet Scale | 201811 | Presentation|
0
| ----- | -- | **Dynam-IX: a Dynamic Interconnection eXchange** | 201812 | Paper|
|  0/ 1 |  0% | Dynam-IX: a Dynamic Interconnection eXchange | 201808 | Paper|
0
| ----- | -- | **Stable and Practical AS Relationship Inference with ProbLink** | 201902 | Paper|
|  0/ 1 |  0% | Stable and Practical AS Relationship Inference with ProbLink | 201902 | Presentation|
0
| ----- | -- | **Blink: Fast Connectivity Recovery Entirely in the Data Plane** | 201902 | Paper|
|  0/ 1 |  0% | Blink: Fast Connectivity Recovery Entirely in the Data Plane | 201902 | Presentation|
0
| ----- | -- | **How to Find Correlated Internet Failures** | 201903 | Paper|
|  0/ 1 |  0% | How to find correlated Internet failures | 201903 | Presentation|
0
| ----- | -- | **Geo-Locating BGP prefixes** | 201906 | Paper|
|  0/ 1 |  0% | Geo-locating BGP prefixes | 201906 | Presentation|
0
| ----- | -- | **An Empirical Study of Mobile Network Behavior and Application Performance in the Wild** | 201906 | Paper|
|  0/ 1 |  0% | An Empirical Study of Mobile Network Behavior and Application Performance in the Wild | 201906 | Presentation|
0
| ----- | -- | **Residential Links Under the Weather** | 201908 | Paper|
|  0/ 1 |  0% | Residential Links Under the Weather | 201908 | Presentation|
0
| ----- | -- | **Profiling BGP Serial Hijackers: Capturing Persistent Misbehavior in the Global Routing Table** | 201910 | Paper|
|  0/ 1 |  0% | Profiling BGP Serial Hijackers: Capturing Persistent Misbehavior in the Global Routing Table | 201910 | Presentation|
0
| ----- | -- | **Network Hygiene, Incentives, and Regulation: Deployment of Source Address Validation in the Internet** | 201911 | Paper|
|  0/ 1 |  0% | Network Hygiene, Incentives, and Regulation: Deployment of Source Address Validation in the Internet | 201911 | Presentation|
0
| ----- | -- | **Challenges in Inferring Spoofed Traffic at IXPs** | 201912 | Paper|
|  0/ 1 |  0% | Challenges in Inferring Spoofed Traffic at IXPs | 201912 | Presentation|
0
| ----- | -- | **When parents and children disagree: Diving into DNS delegation inconsistency** | 202003 | Paper|
|  0/ 1 |  0% | When parents and children disagree: Diving into DNS delegation inconsistency | 202003 | Presentation|
0
| ----- | -- | **Unintended consequences: Effects of submarine cable deployment on Internet routing** | 202003 | Paper|
|  0/ 1 |  0% | Unintended consequences: Effects of submarine cable deployment on Internet routing | 202003 | Presentation|
0
| ----- | -- | **FlowTrace: A Framework for Active Bandwidth Measurements using In-band Packet Trains** | 202003 | Paper|
|  0/ 1 |  0% | FlowTrace: A Framework for Active Bandwidth Measurements using In-band Packet Trains | 202003 | Presentation|
0
| ----- | -- | **To Filter or not to Filter: Measuring the Benefits of Registering in the RPKI Today** | 202003 | Paper|
|  0/ 1 |  0% | To Filter or not to Filter: Measuring the Benefits of Registering in the RPKI Today | 202003 | Presentation|
0
| ----- | -- | **APPLE: Alias Pruning by Path Length Estimation** | 202003 | Paper|
|  0/ 1 |  0% | APPLE: Alias Pruning by Path Length Estimation | 202003 | Presentation|
0
| ----- | -- | **vrfinder: Finding Outbound Addresses in Traceroute** | 202006 | Paper|
|  0/ 1 |  0% | vrfinder: Finding Outbound Addresses in Traceroute | 202006 | Presentation|
0
| ----- | -- | **Trufflehunter: Cache Snooping Rare Domains at Large Public DNS Resolvers** | 202010 | Paper|
|  0/ 1 |  0% | Trufflehunter: Cache Snooping Rare Domains at Large Public DNS Resolvers | 202010 | Presentation|
0
| ----- | -- | **Learning to Extract and Use ASNs in Hostnames** | 202010 | Paper|
|  0/ 1 |  0% | Learning to Extract and Use ASNs in Hostnames | 202010 | Presentation|
0
| ----- | -- | **Measuring the impact of COVID-19 on cloud network performance** | 202011 | Paper|
|  0/ 1 |  0% | Measuring the impact of COVID-19 on cloud network performance | 202011 | Presentation|
0
| ----- | -- | **Trust Zones: A Path to a More Secure Internet Infrastructure** | 202102 | Paper|
|  0/ 1 |  0% | Trust Zones: A Path to a More Secure Internet Infrastructure | 202108 | Paper|
0
| ----- | -- | **Trust Zones: A Path to a More Secure Internet Infrastructure** | 202108 | Paper|
|  0/ 1 |  0% | Trust Zones: A Path to a More Secure Internet Infrastructure | 202102 | Paper|
0
| ----- | -- | **Risky BIZness: Risks Derived from Registrar Name Management** | 202111 | Paper|
|  0/ 1 |  0% | Risky BIZness: Risks Derived from Registrar Name Management | 202109 | Presentation|
0
| ----- | -- | **Measuring the network performance of Google Cloud Platform** | 202111 | Paper|
|  0/ 1 |  0% | Measuring the network performance of Google Cloud Platform | 202111 | Presentation|
0
| ----- | -- | **Learning to Extract Geographic Information from Internet Router Hostnames** | 202112 | Paper|
|  0/ 1 |  0% | Learning to Extract Geographic Information from Internet Router Hostnames | 202112 | Presentation|
0
| ----- | -- | **Jitterbug: A new framework for jitter-based congestion inference** | 202203 | Paper|
|  0/ 1 |  0% | Jitterbug: A new framework for jitter-based congestion inference | 202203 | Presentation|
0
| ----- | -- | **Design and Implementation of Web-based Speed Test Analysis Tool Kit** | 202203 | Paper|
|  0/ 1 |  0% | Design and Implementation of Web-based Speed Test Analysis Tool Kit | 202203 | Presentation|
0
| ----- | -- | **Stop, DROP, and ROA: Effectiveness of Defenses through the lens of DROP** | 202210 | Paper|
|  0/ 1 |  0% | Stop, DROP, and ROA: Effectiveness of Defenses through the lens of DROP | 202210 | Presentation|
0
| ----- | -- | **Retroactive Identification of Targeted DNS Infrastructure Hijacking** | 202210 | Paper|
|  0/ 1 |  0% | Retroactive Identification of Targeted DNS Infrastructure Hijacking | 202210 | Presentation|
0
| ----- | -- | **Mind Your MANRS: Measuring the MANRS Ecosystem** | 202210 | Paper|
|  0/ 1 |  0% | Mind Your MANRS: Measuring the MANRS Ecosystem | 202210 | Presentation|
0
| ----- | -- | **Investigating the impact of DDoS attacks on DNS infrastructure** | 202210 | Paper|
|  0/ 1 |  0% | Investigating the impact of DDoS attacks on DNS infrastructure | 202210 | Presentation|
