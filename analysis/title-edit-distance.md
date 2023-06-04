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

| dist/length | ratio  | name  | date | type |
|----|---|----|-----|----|
| | | **Otter: A general-purpose network visualization tool** | 1999-06 | Paper|
| 13/51 | 25% | Otter: General Purpose Network Viz Tool | 1998-08 | Presentation|
| | | **GTrace - A Graphical Traceroute Tool** | 1999-11 | Paper|
|  0/36 |  0% | GTrace - A Graphical Traceroute Tool | 1999-11 | Presentation|
| | | **CAIDA: Visualizing the Internet** | 2001-01 | Paper|
|  7/31 | 22% | AS Core: Visualizing the Internet | 2011-03 | Presentation|
| | | **Streams, Flows and Torrents** | 2001-04 | Paper|
|  1/27 |  3% | Streams Flows and Torrents | 2001-04 | Presentation|
| | | **DNS Root/gTLD Performance Measurements** | 2001-12 | Paper|
|  0/38 |  0% | DNS Root/gTLD Performance Measurements | 2001-12 | Presentation|
|  6/38 | 15% | DNS/gTLD Performance Measurements  | 2001-12 | Presentation|
| | | **Internet Expansion, Refinement, and Churn** | 2002-01 | Paper|
|  0/41 |  0% | Internet expansion, refinement, and churn | 2002-02 | Presentation|
| | | **Distance Metrics in the Internet** | 2002-09 | Paper|
|  0/32 |  0% | Distance metrics in the Internet | 2002-09 | Presentation|
| | | **Traceroute and BGP AS Path Incongruities** | 2003-03 | Paper|
|  0/40 |  0% | Traceroute and BGP AS Path Incongruities | 2003-06 | Presentation|
| | | **On Third-party Addresses in Traceroute Paths** | 2003-04 | Paper|
|  0/44 |  0% | On Third-party Addresses in Traceroute Paths | 2003-04 | Presentation|
| | | **Internet Quarantine: Requirements for Containing Self-Propagating Code** | 2003-04 | Paper|
|  0/70 |  0% | Internet Quarantine: Requirements for Containing Self-Propagating Code | 2003-04 | Presentation|
| | | **Their share: diversity and disparity in IP traffic** | 2004-04 | Paper|
|  0/50 |  0% | Their Share: Diversity and Disparity in IP Traffic | 2004-04 | Presentation|
| | | **The Spread of the Witty Worm** | 2004-08 | Paper|
|  0/28 |  0% | The Spread of the Witty Worm | 2004-07 | Presentation|
| | | **Building a Better NetFlow** | 2004-09 | Paper|
|  0/25 |  0% | Building a Better NetFlow | 2004-09 | Presentation|
|  0/25 |  0% | Building a Better NetFlow | 2004-08 | Presentation|
| | | **Comparison of Public End-to-End Bandwidth Estimation Tools on High-Speed Links** | 2005-03 | Paper|
|  0/78 |  0% | Comparison of Public End-to-End Bandwidth Estimation tools on High-Speed Links | 2005-03 | Presentation|
| | | **Spectroscopy of traceroute delays** | 2005-03 | Paper|
|  0/33 |  0% | Spectroscopy of Traceroute Delays | 2005-03 | Presentation|
| | | **Revisiting Internet AS-level Topology Discovery** | 2005-03 | Paper|
|  0/47 |  0% | Revisiting Internet AS-level Topology Discovery | 2005-03 | Presentation|
| | | **Inferring AS Relationships: Dead End or Lively Beginning?** | 2005-05 | Paper|
|  0/57 |  0% | Inferring AS Relationships: Dead End or Lively Beginning? | 2005-05 | Presentation|
| | | **A Robust System for Accurate Real-time Summaries of Internet Traffic** | 2005-06 | Paper|
| 18/68 | 26% | A Robust System for Accurate Real-time Summaries of Internet Traffic: Technical Report | 2005-06 | Paper|
|  0/68 |  0% | A Robust System for Accurate Real-time Summaries of Internet Traffic | 2005-06 | Presentation|
| | | **A Robust System for Accurate Real-time Summaries of Internet Traffic: Technical Report** | 2005-06 | Paper|
| 18/86 | 20% | A Robust System for Accurate Real-time Summaries of Internet Traffic | 2005-06 | Paper|
| 18/86 | 20% | A Robust System for Accurate Real-time Summaries of Internet Traffic | 2005-06 | Presentation|
| | | **Impact of Degree Correlations on Topology Generators** | 2005-08 | Paper|
| 12/52 | 23% | Degree correlations and topology generators | 2005-03 | Presentation|
| | | **A Basis for Systematic Analysis of Network Topologies: Technical Report** | 2006-04 | Paper|
| 18/71 | 25% | A Basis for Systematic Analysis of Network Topologies | 2006-05 | Presentation|
| | | **Systematic Topology Analysis and Generation Using Degree Correlations** | 2006-09 | Paper|
| 11/69 | 15% | dK-series: Systematic Topology Analysis and Generation Using Degree Correlations | 2006-06 | Presentation|
| | | **Two Days in the Life of the DNS Anycast Root Servers** | 2007-04 | Paper|
| 10/52 | 19% | Two days in the life of three DNS root servers | 2006-11 | Presentation|
| | | **Passive Monitoring of DNS Anomalies** | 2007-07 | Paper|
|  0/35 |  0% | Passive Monitoring of DNS Anomalies | 2007-07 | Presentation|
| | | **Traceroute Probe Method and Forward IP Path Inference** | 2008-10 | Paper|
|  0/53 |  0% | Traceroute Probe Method and Forward IP Path Inference | 2008-10 | Presentation|
| | | **Navigability of Complex Networks** | 2009-01 | Paper|
|  0/32 |  0% | Navigability of complex networks | 2010-01 | Presentation|
|  8/32 | 25% | Navigability of Networks | 2010-05 | Presentation|
| | | **Evolution of the Internet AS-Level Ecosystem** | 2009-02 | Paper|
|  9/44 | 20% | Evolution of the Internet Ecosystem | 2009-10 | Presentation|
| | | **Greedy Forwarding in Dynamic Scale-Free Networks Embedded in Hyperbolic Metric Spaces: Technical Report** | 2009-07 | Paper|
| 26/103 | 25% | Greedy Forwarding in Scale-Free Networks Embedded in Hyperbolic Metric Spaces | 2009-09 | Paper|
| 18/103 | 17% | Greedy Forwarding in Dynamic Scale-Free Networks Embedded in Hyperbolic Metric Spaces | 2010-03 | Paper|
| | | **Greedy Forwarding in Scale-Free Networks Embedded in Hyperbolic Metric Spaces** | 2009-09 | Paper|
|  0/77 |  0% | Greedy Forwarding in Scale-Free Networks Embedded in Hyperbolic Metric Spaces | 2009-06 | Presentation|
| | | **An Internet Data Sharing Framework For Balancing Privacy and Utility** | 2009-10 | Paper|
|  0/68 |  0% | An Internet Data Sharing Framework For Balancing Privacy and Utility | 2009-10 | Presentation|
| | | **A Framework for Understanding and Applying Ethical Principles in Network and Security Research ** | 2010-01 | Paper|
|  3/95 |  3% | Framework for Understanding and Applying Ethical Principles in Network and Security Research | 2010-01 | Presentation|
| | | **Evolution of the Internet AS-Level Ecosystem** | 2010-03 | Paper|
|  0/44 |  0% | Evolution of the Internet AS-Level Ecosystem | 2009-02 | Presentation|
| | | **Estimating Routing Symmetry on Single Links by Passive Flow Measurements** | 2010-03 | Paper|
|  0/72 |  0% | Estimating Routing Symmetry on Single Links by Passive Flow Measurements | 2010-06 | Presentation|
| | | **Greedy Forwarding in Dynamic Scale-Free Networks Embedded in Hyperbolic Metric Spaces** | 2010-03 | Paper|
|  0/85 |  0% | Greedy Forwarding in Dynamic Scale-Free Networks Embedded in Hyperbolic Metric Spaces | 2010-03 | Presentation|
| 18/85 | 21% | Greedy Forwarding in Dynamic Scale-Free Networks Embedded in Hyperbolic Metric Spaces: Technical Report | 2009-07 | Paper|
|  8/85 |  9% | Greedy Forwarding in Scale-Free Networks Embedded in Hyperbolic Metric Spaces | 2009-06 | Presentation|
| | | **Understanding and preparing for DNS evolution ** | 2010-04 | Paper|
|  1/46 |  2% | Understanding and Preparing for DNS Evolution | 2010-04 | Presentation|
| | | **Identification of influential spreaders in complex networks** | 2010-08 | Paper|
|  0/59 |  0% | Identification of Influential Spreaders in Complex Networks | 2011-03 | Presentation|
|  0/59 |  0% | Identification of Influential Spreaders in Complex Networks | 2010-05 | Presentation|
| | | **A Value-based Framework for Internet Peering Agreements** | 2010-10 | Paper|
|  0/55 |  0% | A Value-based Framework for Internet Peering Agreements | 2010-09 | Presentation|
|  1/55 |  1% | A Value-based Framework for Internet Peering Agreements  | 2010-06 | Presentation|
| | | **Hyperbolic Geometry of Complex Networks** | 2010-10 | Paper|
|  0/39 |  0% | Hyperbolic geometry of complex networks | 2010-05 | Presentation|
|  0/39 |  0% | Hyperbolic geometry of complex networks | 2009-10 | Presentation|
|  0/39 |  0% | Hyperbolic geometry of complex networks | 2011-04 | Presentation|
|  6/39 | 15% | Hyperbolic geometry of large networks | 2012-02 | Presentation|
| | | **The Internet is Flat: Modeling the Transition from a Transit Hierarchy to a Peering Mesh** | 2010-12 | Paper|
|  0/88 |  0% | The Internet is Flat: Modeling the Transition from a Transit Hierarchy to a Peering Mesh | 2010-12 | Presentation|
| | | **Measured Impact of Crooked Traceroute** | 2011-01 | Paper|
|  0/37 |  0% | Measured Impact of Crooked Traceroute | 2011-02 | Presentation|
| | | **Percolation in Self-Similar Networks ** | 2011-01 | Paper|
|  1/37 |  2% | Percolation in self-similar networks | 2011-06 | Presentation|
|  1/37 |  2% | Percolation in self-similar networks | 2011-03 | Presentation|
| | | **Tracking IPv6 Evolution: Data We Have and Data We Need** | 2011-07 | Paper|
|  0/54 |  0% | Tracking IPv6 evolution: Data We Have and Data We Need | 2011-08 | Presentation|
| | | **Analysis of Country-wide Internet Outages Caused by Censorship** | 2011-11 | Paper|
|  0/62 |  0% | Analysis of Country-wide Internet Outages Caused by Censorship | 2012-07 | Presentation|
|  0/62 |  0% | Analysis of Country-wide Internet Outages Caused by Censorship | 2011-11 | Presentation|
|  0/62 |  0% | Analysis of Country-wide Internet Outages Caused by Censorship | 2011-12 | Presentation|
| | | **Extracting benefit from harm: using malware pollution to analyze the impact of political and geophysical events on the Internet** | 2012-01 | Paper|
|  0/127 |  0% | Extracting Benefit from Harm: Using Malware Pollution to Analyze the Impact of Political and Geophysical Events on the Internet | 2012-08 | Presentation|
|  0/127 |  0% | Extracting Benefit from Harm: Using Malware Pollution to Analyze the Impact of Political and Geophysical Events on the Internet | 2012-01 | Presentation|
| | | **Analysis of peering strategy adoption by transit providers in the Internet** | 2012-03 | Paper|
|  0/74 |  0% | Analysis of peering strategy adoption by transit providers in the Internet | 2012-05 | Presentation|
| | | **One-way Traffic Monitoring with iatmon** | 2012-03 | Paper|
|  1/38 |  2% | One way Traffic Monitoring with iatmon | 2012-05 | Presentation|
| | | **Measuring the Evolution of Internet Peering Agreements** | 2012-05 | Paper|
|  0/54 |  0% | Measuring the Evolution of Internet Peering Agreements | 2012-05 | Presentation|
| | | **Internet Topology Data Comparison** | 2012-05 | Paper|
|  9/33 | 27% | Internet Topology Data Kit | 2011-02 | Presentation|
| | | **Peering Strategy Adoption by Transit Providers in the Internet: A Game Theoretic Approach** | 2012-09 | Paper|
|  0/89 |  0% | Peering Strategy adoption by Transit Providers in the Internet: A Game Theoretic Approach | 2012-06 | Presentation|
| | | **Popularity versus Similarity in Growing Networks** | 2012-09 | Paper|
|  0/48 |  0% | Popularity versus Similarity in Growing Networks | 2012-11 | Presentation|
|  0/48 |  0% | Popularity versus Similarity in Growing Networks | 2011-10 | Presentation|
|  0/48 |  0% | Popularity versus Similarity in Growing Networks | 2011-11 | Presentation|
|  0/48 |  0% | Popularity versus Similarity in Growing Networks | 2012-03 | Presentation|
|  0/48 |  0% | Popularity versus Similarity in Growing Networks | 2012-02 | Presentation|
|  0/48 |  0% | Popularity versus Similarity in Growing Networks | 2013-03 | Presentation|
| | | **Analysis of Internet-wide Probing using Darknets** | 2012-10 | Paper|
|  0/48 |  0% | Analysis of Internet-wide Probing using Darknets | 2012-10 | Presentation|
| | | **Analysis of a "/0" Stealth Scan from a Botnet** | 2012-11 | Paper|
|  0/45 |  0% | Analysis of a "/0" Stealth Scan from a Botnet | 2015-04 | Paper|
|  0/45 |  0% | Analysis of a "/0" Stealth Scan from a Botnet | 2012-11 | Presentation|
| | | **Measuring the Deployment of IPv6: Topology, Routing and Performance** | 2012-11 | Paper|
|  1/67 |  1% | Measuring the Deployment of IPv6: Topology, Routing, and Performance | 2012-11 | Presentation|
| | | **Network Cosmology** | 2012-11 | Paper|
|  0/17 |  0% | Network Cosmology | 2012-03 | Presentation|
| | | **Gaining Insight into AS-level Outages through Analysis of Internet Background Radiation** | 2012-12 | Paper|
|  0/87 |  0% | Gaining Insight into AS-level Outages through Analysis of Internet Background Radiation | 2013-04 | Paper|
| | | **IPv6 Alias Resolution via Induced Fragmentation** | 2013-03 | Paper|
|  0/47 |  0% | IPv6 Alias Resolution via Induced Fragmentation | 2013-03 | Presentation|
| | | **Internet-Scale IPv4 Alias Resolution with MIDAR** | 2013-04 | Paper|
|  5/47 | 10% | Internet-Scale Alias Resolution with MIDAR | 2010-02 | Presentation|
| | | **Gaining Insight into AS-level Outages through Analysis of Internet Background Radiation** | 2013-04 | Paper|
|  0/87 |  0% | Gaining Insight into AS-level Outages through Analysis of Internet Background Radiation | 2012-12 | Paper|
|  0/87 |  0% | Gaining Insight into AS-level Outages through Analysis of Internet Background Radiation | 2013-04 | Presentation|
| | | **AS Relationships, Customer Cones, and Validation** | 2013-10 | Paper|
|  1/48 |  2% | AS Relationships, Customer Cones, and Validation  | 2013-10 | Presentation|
| | | **Speedtrap: Internet-Scale IPv6 Alias Resolution** | 2013-10 | Paper|
|  0/47 |  0% | Speedtrap: Internet-Scale IPv6 Alias Resolution | 2013-10 | Presentation|
| | | **A First Look at IPv4 Transfer Markets** | 2013-12 | Paper|
|  0/37 |  0% | A First Look at IPv4 Transfer Markets | 2013-12 | Presentation|
| | | **Inferring Multilateral Peering** | 2013-12 | Paper|
|  1/30 |  3% | Inferring Multilateral Peering  | 2013-12 | Presentation|
| | | **A Coordinated View of the Temporal Evolution of Large-scale Internet Events** | 2014-01 | Paper|
|  0/75 |  0% | A Coordinated View of the Temporal Evolution of Large-scale Internet Events | 2014-01 | Media|
| | | **A Second Look at Detecting Third-Party Addresses in Traceroute Traces with the IP Timestamp Option** | 2014-03 | Paper|
|  2/98 |  2% | A second look at ‟Detecting third-party addresses in traceroute traces with the IP timestamp option“ | 2014-03 | Presentation|
| | | **Lost in Space: Improving Inference of IPv4 Address Space Utilization** | 2014-10 | Paper|
|  0/68 |  0% | Lost in Space: Improving Inference of IPv4 Address Space Utilization | 2016-06 | Paper|
|  0/68 |  0% | Lost in Space: Improving Inference of IPv4 Address Space Utilization | 2015-09 | Paper|
| | | **Challenges in Inferring Internet Interdomain Congestion** | 2014-11 | Paper|
|  0/55 |  0% | Challenges in Inferring Internet Interdomain Congestion | 2014-11 | Presentation|
| | | **Survey of End-to-End Mobile Network Measurement Testbeds** | 2014-11 | Paper|
|  0/56 |  0% | Survey of End-to-End Mobile Network Measurement Testbeds | 2016-01 | Paper|
| | | **Analysis of Country-wide Internet Outages Caused by Censorship** | 2014-12 | Paper|
|  0/62 |  0% | Analysis of Country-wide Internet Outages Caused by Censorship | 2012-07 | Presentation|
| | | **IPv6 AS Relationships, Cliques, and Congruence** | 2015-03 | Paper|
|  1/46 |  2% | IPv6 AS Relationships, Clique, and Congruence | 2015-03 | Presentation|
| | | **Measuring and Characterizing IPv6 Router Availability** | 2015-03 | Paper|
|  0/53 |  0% | Measuring and Characterizing IPv6 Router Availability | 2015-03 | Presentation|
| | | **Analysis of a "/0" Stealth Scan from a Botnet** | 2015-04 | Paper|
|  0/45 |  0% | Analysis of a "/0" Stealth Scan from a Botnet | 2012-11 | Paper|
|  0/45 |  0% | Analysis of a "/0" Stealth Scan from a Botnet | 2012-11 | Presentation|
| | | **Named Data Networking Next Phase (NDN-NP) Project May 2014 - April 2015 Annual Report** | 2015-06 | Paper|
|  2/85 |  2% | Named Data Networking Next Phase (NDN-NP) Project May 2016 - April 2017 Annual Report | 2017-11 | Paper|
|  2/85 |  2% | Named Data Networking Next Phase (NDN-NP) Project May 2015 - April 2016 Annual Report | 2016-06 | Paper|
| | | **Experience in using MTurk for Network Measurement** | 2015-08 | Paper|
| 10/49 | 20% | Experience in using Mechanical Turk for Network Measurement | 2015-08 | Presentation|
| | | **Adding Enhanced Services to the Internet: Lessons from History** | 2015-09 | Paper|
|  0/62 |  0% | Adding Enhanced Services to the Internet: Lessons from History | 2016-07 | Paper|
|  0/62 |  0% | Adding Enhanced Services to the Internet: Lessons from History | 2015-09 | Presentation|
| | | **Lost in Space: Improving Inference of IPv4 Address Space Utilization** | 2015-09 | Paper|
|  0/68 |  0% | Lost in Space: Improving Inference of IPv4 Address Space Utilization | 2014-10 | Paper|
|  0/68 |  0% | Lost in Space: Improving Inference of IPv4 Address Space Utilization | 2015-10 | Presentation|
|  0/68 |  0% | Lost in Space: Improving Inference of IPv4 Address Space Utilization | 2016-06 | Paper|
| | | **BGPStream: a software framework for live and historical BGP data analysis** | 2015-10 | Paper|
| 17/73 | 23% | BGPStream - An Open Source Framework for Live/Historical BGP Data Analysis | 2015-05 | Presentation|
| | | **Leveraging Internet Background Radiation for Opportunistic Network Analysis** | 2015-10 | Paper|
|  0/75 |  0% | Leveraging Internet Background Radiation for Opportunistic Network Analysis | 2015-10 | Presentation|
| | | **Mapping Peering Interconnections to a Facility** | 2015-12 | Paper|
|  0/46 |  0% | Mapping Peering Interconnections to a Facility | 2015-12 | Presentation|
| | | **The 7th Workshop on Active Internet Measurements (AIMS-7) Report** | 2016-01 | Paper|
|  3/64 |  4% | The 8th Workshop on Active Internet Measurements (AIMS8) Report | 2016-10 | Paper|
| | | **Survey of End-to-End Mobile Network Measurement Testbeds** | 2016-01 | Paper|
|  0/56 |  0% | Survey of End-to-End Mobile Network Measurement Testbeds | 2014-11 | Paper|
| | | **NAT Revelio: Detecting NAT444 in the ISP** | 2016-03 | Paper|
|  0/40 |  0% | NAT Revelio: Detecting NAT444 in the ISP | 2016-03 | Presentation|
| | | **Periscope: Unifying Looking Glass Querying** | 2016-03 | Paper|
|  1/42 |  2% | Periscope:Unifying Looking Glass Querying | 2016-03 | Presentation|
|  1/42 |  2% | Periscope: Unifying Looking Glass querying  | 2015-12 | Presentation|
| | | **Characterizing IPv6 control and data plane stability** | 2016-04 | Paper|
|  0/52 |  0% | Characterizing IPv6 control and data plane stability | 2016-04 | Presentation|
| | | **Lost in Space: Improving Inference of IPv4 Address Space Utilization** | 2016-06 | Paper|
|  0/68 |  0% | Lost in Space: Improving Inference of IPv4 Address Space Utilization | 2014-10 | Paper|
|  0/68 |  0% | Lost in Space: Improving Inference of IPv4 Address Space Utilization | 2015-09 | Paper|
| | | **Named Data Networking Next Phase (NDN-NP) Project May 2015 - April 2016 Annual Report** | 2016-06 | Paper|
|  2/85 |  2% | Named Data Networking Next Phase (NDN-NP) Project May 2014 - April 2015 Annual Report | 2015-06 | Paper|
|  2/85 |  2% | Named Data Networking Next Phase (NDN-NP) Project May 2016 - April 2017 Annual Report | 2017-11 | Paper|
| | | **Adding Enhanced Services to the Internet: Lessons from History** | 2016-07 | Paper|
|  0/62 |  0% | Adding Enhanced Services to the Internet: Lessons from History | 2015-09 | Paper|
| | | **The 8th Workshop on Active Internet Measurements (AIMS8) Report** | 2016-10 | Paper|
|  3/63 |  4% | The 9th Workshop on Active Internet Measurements (AIMS-9) Report | 2017-10 | Paper|
|  3/63 |  4% | The 7th Workshop on Active Internet Measurements (AIMS-7) Report | 2016-01 | Paper|
| | | **bdrmap: Inference of Borders Between IP Networks** | 2016-11 | Paper|
|  0/48 |  0% | bdrmap: Inference of Borders Between IP Networks | 2016-11 | Presentation|
| | | **BGPStream: a software framework for live and historical BGP data analysis** | 2016-11 | Paper|
|  0/73 |  0% | BGPStream: A Software Framework for Live and Historical BGP Data Analysis | 2016-11 | Presentation|
|  1/73 |  1% | BGPStream: A Software Framework for Live and Historical BGP Data Analysis  | 2017-03 | Presentation|
| | | **Workshop on Internet Economics (WIE2016) Final Report** | 2017-07 | Paper|
|  1/53 |  1% | Workshop on Internet Economics (WIE2017) Final Report | 2018-07 | Paper|
| | | **Detecting Peering Infrastructure Outages in the Wild** | 2017-08 | Paper|
|  0/52 |  0% | Detecting Peering Infrastructure Outages in the Wild | 2017-08 | Presentation|
|  0/52 |  0% | Detecting Peering Infrastructure Outages in the Wild | 2017-12 | Presentation|
| | | **The 9th Workshop on Active Internet Measurements (AIMS-9) Report** | 2017-10 | Paper|
|  3/64 |  4% | The 8th Workshop on Active Internet Measurements (AIMS8) Report | 2016-10 | Paper|
|  4/64 |  6% | The 10th Workshop on Active Internet Measurements (AIMS-10) Report | 2018-10 | Paper|
| | | **Challenges in Inferring Internet Congestion Using Throughput Measurements** | 2017-11 | Paper|
|  0/73 |  0% | Challenges in Inferring Internet Congestion Using Throughput Measurements | 2017-11 | Presentation|
| | | **Inferring BGP Blackholing Activity in the Internet** | 2017-11 | Paper|
|  9/50 | 18% | Inferring BGP Blackholing in the Internet | 2017-11 | Presentation|
| | | **Investigating the Causes of Congestion on the African IXP substrate** | 2017-11 | Paper|
|  0/67 |  0% | Investigating the Causes of Congestion on the African IXP substrate | 2018-11 | Presentation|
|  0/67 |  0% | Investigating the Causes of Congestion on the African IXP substrate | 2017-11 | Presentation|
| | | **A Look at Router Geolocation in Public and Commercial Databases** | 2017-11 | Paper|
|  0/63 |  0% | A Look at Router Geolocation in Public and Commercial Databases | 2017-11 | Presentation|
| | | **Millions of Targets Under Attack: a Macroscopic Characterization of the DoS Ecosystem** | 2017-11 | Paper|
|  0/85 |  0% | Millions of Targets Under Attack: a Macroscopic Characterization of the DoS Ecosystem | 2017-11 | Presentation|
| | | **Named Data Networking Next Phase (NDN-NP) Project May 2016 - April 2017 Annual Report** | 2017-11 | Paper|
|  2/85 |  2% | Named Data Networking Next Phase (NDN-NP) Project May 2014 - April 2015 Annual Report | 2015-06 | Paper|
|  2/85 |  2% | Named Data Networking Next Phase (NDN-NP) Project May 2015 - April 2016 Annual Report | 2016-06 | Paper|
| | | **PacketLab: A Universal Measurement Endpoint Interface** | 2017-11 | Paper|
|  1/53 |  1% | PacketLab:A Universal Measurement Endpoint Interface | 2017-11 | Presentation|
| | | **TCP Congestion Signatures** | 2017-11 | Paper|
|  0/25 |  0% | TCP Congestion Signatures | 2017-11 | Presentation|
|  0/25 |  0% | TCP Congestion Signatures | 2018-07 | Presentation|
| | | **ARTEMIS: Neutralizing BGP Hijacking within a Minute** | 2018-01 | Paper|
|  0/51 |  0% | ARTEMIS: Neutralizing BGP Hijacking within a Minute | 2018-07 | Presentation|
| | | **Policy Implications of Third-Party Measurement of Interdomain Congestion on the Internet** | 2018-03 | Paper|
|  0/88 |  0% | Policy Implications of Third-Party Measurement of Interdomain Congestion on the Internet | 2018-03 | Presentation|
| | | **Studying the Evolution of Content Providers in the Internet Core** | 2018-06 | Paper|
|  0/64 |  0% | Studying the Evolution of Content Providers in the Internet Core | 2018-09 | Presentation|
| | | **Workshop on Internet Economics (WIE2017) Final Report** | 2018-07 | Paper|
|  1/53 |  1% | Workshop on Internet Economics (WIE2016) Final Report | 2017-07 | Paper|
|  1/53 |  1% | Workshop on Internet Economics (WIE2018) Final Report | 2019-04 | Paper|
| | | **Dynam-IX: a Dynamic Interconnection eXchange** | 2018-08 | Paper|
|  0/44 |  0% | Dynam-IX: a Dynamic Interconnection eXchange | 2018-12 | Paper|
| | | **Inferring Persistent Interdomain Congestion** | 2018-08 | Paper|
|  0/43 |  0% | Inferring Persistent Interdomain Congestion | 2018-08 | Presentation|
| | | **The 10th Workshop on Active Internet Measurements (AIMS-10) Report** | 2018-10 | Paper|
|  4/66 |  6% | The 9th Workshop on Active Internet Measurements (AIMS-9) Report | 2017-10 | Paper|
| | | **A First Joint Look at DoS Attacks and BGP Blackholing in the Wild** | 2018-10 | Paper|
|  0/65 |  0% | A First Joint Look at DoS Attacks and BGP Blackholing in the Wild | 2018-11 | Presentation|
| | | **Pushing the Boundaries with bdrmapIT: Mapping Router Ownership at Internet Scale** | 2018-11 | Paper|
|  0/80 |  0% | Pushing the Boundaries with bdrmapIT: Mapping Router Ownership at Internet Scale | 2018-11 | Presentation|
| | | **ARTEMIS: Neutralizing BGP Hijacking within a Minute** | 2018-12 | Paper|
|  0/51 |  0% | ARTEMIS: Neutralizing BGP Hijacking within a Minute | 2018-07 | Presentation|
|  0/51 |  0% | ARTEMIS: Neutralizing BGP Hijacking within a Minute | 2018-03 | Presentation|
|  0/51 |  0% | ARTEMIS: Neutralizing BGP Hijacking within a Minute | 2018-05 | Presentation|
| | | **Dynam-IX: a Dynamic Interconnection eXchange** | 2018-12 | Paper|
|  0/44 |  0% | Dynam-IX: a Dynamic Interconnection eXchange | 2018-08 | Paper|
| | | **Blink: Fast Connectivity Recovery Entirely in the Data Plane** | 2019-02 | Paper|
|  0/60 |  0% | Blink: Fast Connectivity Recovery Entirely in the Data Plane | 2019-02 | Presentation|
| | | **Stable and Practical AS Relationship Inference with ProbLink** | 2019-02 | Paper|
|  0/60 |  0% | Stable and Practical AS Relationship Inference with ProbLink | 2019-02 | Presentation|
| | | **How to Find Correlated Internet Failures** | 2019-03 | Paper|
|  0/40 |  0% | How to find correlated Internet failures | 2019-03 | Presentation|
| | | **Workshop on Internet Economics (WIE2018) Final Report** | 2019-04 | Paper|
|  1/53 |  1% | Workshop on Internet Economics (WIE2017) Final Report | 2018-07 | Paper|
| | | **An Empirical Study of Mobile Network Behavior and Application Performance in the Wild** | 2019-06 | Paper|
|  0/85 |  0% | An Empirical Study of Mobile Network Behavior and Application Performance in the Wild | 2019-06 | Presentation|
| | | **Geo-Locating BGP prefixes** | 2019-06 | Paper|
|  0/25 |  0% | Geo-locating BGP prefixes | 2019-06 | Presentation|
| | | **Residential Links Under the Weather** | 2019-08 | Paper|
|  0/35 |  0% | Residential Links Under the Weather | 2019-08 | Presentation|
| | | **Toward a Theory of Harms in the Internet Ecosystem** | 2019-09 | Paper|
| 10/50 | 20% | Toward a theory of harms in the Internet | 2019-09 | Presentation|
| | | **Learning Regexes to Extract Router Names from Hostnames** | 2019-10 | Paper|
|  8/55 | 14% | Learning to Extract Router Names from Hostnames | 2019-10 | Presentation|
|  6/55 | 10% | Learning Regexes to Extract Network Names from Hostnames | 2021-12 | Paper|
| | | **Profiling BGP Serial Hijackers: Capturing Persistent Misbehavior in the Global Routing Table** | 2019-10 | Paper|
|  0/92 |  0% | Profiling BGP Serial Hijackers: Capturing Persistent Misbehavior in the Global Routing Table | 2019-10 | Presentation|
| | | **Network Hygiene, Incentives, and Regulation: Deployment of Source Address Validation in the Internet** | 2019-11 | Paper|
|  0/100 |  0% | Network Hygiene, Incentives, and Regulation: Deployment of Source Address Validation in the Internet | 2019-11 | Presentation|
| | | **Challenges in Inferring Spoofed Traffic at IXPs** | 2019-12 | Paper|
|  0/47 |  0% | Challenges in Inferring Spoofed Traffic at IXPs | 2019-12 | Presentation|
| | | **APPLE: Alias Pruning by Path Length Estimation** | 2020-03 | Paper|
|  0/46 |  0% | APPLE: Alias Pruning by Path Length Estimation | 2020-03 | Presentation|
| | | **To Filter or not to Filter: Measuring the Benefits of Registering in the RPKI Today** | 2020-03 | Paper|
|  0/83 |  0% | To Filter or not to Filter: Measuring the Benefits of Registering in the RPKI Today | 2020-03 | Presentation|
| | | **FlowTrace: A Framework for Active Bandwidth Measurements using In-band Packet Trains** | 2020-03 | Paper|
|  0/84 |  0% | FlowTrace: A Framework for Active Bandwidth Measurements using In-band Packet Trains | 2020-03 | Presentation|
| | | **Unintended consequences: Effects of submarine cable deployment on Internet routing** | 2020-03 | Paper|
|  0/82 |  0% | Unintended consequences: Effects of submarine cable deployment on Internet routing | 2020-03 | Presentation|
| | | **When parents and children disagree: Diving into DNS delegation inconsistency** | 2020-03 | Paper|
|  0/76 |  0% | When parents and children disagree: Diving into DNS delegation inconsistency | 2020-03 | Presentation|
| | | **Third Accountability and Transparency Review Team (ATRT3) Report - Minority Statement** | 2020-05 | Paper|
| 21/85 | 24% | Third Accountability and Transparency Review Team (ATRT3) Report | 2020-05 | Paper|
| | | **vrfinder: Finding Outbound Addresses in Traceroute** | 2020-06 | Paper|
|  0/50 |  0% | vrfinder: Finding Outbound Addresses in Traceroute | 2020-06 | Presentation|
| | | **Learning to Extract and Use ASNs in Hostnames** | 2020-10 | Paper|
|  0/45 |  0% | Learning to Extract and Use ASNs in Hostnames | 2020-10 | Presentation|
| | | **MAnycast2 - Using Anycast to Measure Anycast** | 2020-10 | Paper|
|  2/44 |  4% | MAnycast2 Using Anycast to Measure Anycast | 2020-10 | Presentation|
| | | **Trufflehunter: Cache Snooping Rare Domains at Large Public DNS Resolvers** | 2020-10 | Paper|
|  0/72 |  0% | Trufflehunter: Cache Snooping Rare Domains at Large Public DNS Resolvers | 2020-10 | Presentation|
| | | **Unresolved Issues: Prevalence, Persistence, and Perils of Lame Delegations** | 2020-10 | Paper|
|  8/74 | 10% | Unresolved Issues: Prevalence, Persistence, and Perils of Lame Delegations (Video) | 2020-10 | Media|
|  0/74 |  0% | Unresolved Issues: Prevalence, Persistence, and Perils of Lame Delegations | 2020-10 | Presentation|
| | | **Measuring the impact of COVID-19 on cloud network performance** | 2020-11 | Paper|
|  0/61 |  0% | Measuring the impact of COVID-19 on cloud network performance | 2020-11 | Presentation|
| | | **DynamIPs: Analyzing address assignment practices in IPv4 and IPv6** | 2020-12 | Paper|
|  8/65 | 12% | DynamIPs: Analyzing address assignment practices in IPv4 and IPv6 (Video) | 2020-12 | Media|
|  0/65 |  0% | DynamIPs: Analyzing address assignment practices in IPv4 and IPv6 | 2020-12 | Presentation|
| | | **Trust Zones: A Path to a More Secure Internet Infrastructure** | 2021-02 | Paper|
|  0/60 |  0% | Trust Zones: A Path to a More Secure Internet Infrastructure | 2021-08 | Paper|
| | | **Challenges in measuring the Internet for the public Interest** | 2021-08 | Paper|
|  0/60 |  0% | Challenges in measuring the Internet for the public Interest | 2022-05 | Paper|
|  0/60 |  0% | Challenges in measuring the Internet for the public Interest | 2021-09 | Presentation|
| | | **Trust Zones: A Path to a More Secure Internet Infrastructure** | 2021-08 | Paper|
|  0/60 |  0% | Trust Zones: A Path to a More Secure Internet Infrastructure | 2021-02 | Paper|
| | | **IRR Hygiene in the RPKI Era** | 2021-11 | Paper|
|  0/27 |  0% | IRR Hygiene in the RPKI Era | 2022-03 | Paper|
|  0/27 |  0% | IRR Hygiene in the RPKI Era | 2021-10 | Presentation|
| | | **Measuring the network performance of Google Cloud Platform** | 2021-11 | Paper|
|  0/58 |  0% | Measuring the network performance of Google Cloud Platform | 2021-11 | Presentation|
| | | **Risky BIZness: Risks Derived from Registrar Name Management** | 2021-11 | Paper|
|  0/59 |  0% | Risky BIZness: Risks Derived from Registrar Name Management | 2021-09 | Presentation|
| | | **Learning to Extract Geographic Information from Internet Router Hostnames** | 2021-12 | Paper|
|  0/73 |  0% | Learning to Extract Geographic Information from Internet Router Hostnames | 2021-12 | Presentation|
| | | **Learning Regexes to Extract Network Names from Hostnames** | 2021-12 | Paper|
|  6/56 | 10% | Learning Regexes to Extract Router Names from Hostnames | 2019-10 | Paper|
|  0/56 |  0% | Learning Regexes to Extract Network Names from Hostnames | 2021-12 | Presentation|
| | | **Design and Implementation of Web-based Speed Test Analysis Tool Kit** | 2022-03 | Paper|
|  0/67 |  0% | Design and Implementation of Web-based Speed Test Analysis Tool Kit | 2022-03 | Presentation|
| | | **IRR Hygiene in the RPKI Era** | 2022-03 | Paper|
|  0/27 |  0% | IRR Hygiene in the RPKI Era | 2021-11 | Paper|
|  0/27 |  0% | IRR Hygiene in the RPKI Era | 2021-10 | Presentation|
|  0/27 |  0% | IRR Hygiene in the RPKI Era | 2022-03 | Presentation|
| | | **Jitterbug: A new framework for jitter-based congestion inference** | 2022-03 | Paper|
|  0/64 |  0% | Jitterbug: A new framework for jitter-based congestion inference | 2022-03 | Presentation|
| | | **Challenges in measuring the Internet for the public Interest** | 2022-05 | Paper|
|  0/60 |  0% | Challenges in measuring the Internet for the public Interest | 2021-08 | Paper|
|  0/60 |  0% | Challenges in measuring the Internet for the public Interest | 2021-09 | Presentation|
| | | **Where .ru? Assessing the Impact of Conflict on Russian Domain Infrastructure** | 2022-10 | Paper|
|  9/76 | 11% | Where .ru? Assessing the Impact of Conflict on Russian Domain Infrastructure Slideset | 2022-10 | Presentation|
| | | **Investigating the impact of DDoS attacks on DNS infrastructure** | 2022-10 | Paper|
|  0/62 |  0% | Investigating the impact of DDoS attacks on DNS infrastructure | 2022-10 | Presentation|
| | | **Mind Your MANRS: Measuring the MANRS Ecosystem** | 2022-10 | Paper|
|  0/46 |  0% | Mind Your MANRS: Measuring the MANRS Ecosystem | 2022-10 | Presentation|
| | | **Retroactive Identification of Targeted DNS Infrastructure Hijacking** | 2022-10 | Paper|
|  0/67 |  0% | Retroactive Identification of Targeted DNS Infrastructure Hijacking | 2022-10 | Presentation|
| | | **Stop, DROP, and ROA: Effectiveness of Defenses through the lens of DROP** | 2022-10 | Paper|
|  0/71 |  0% | Stop, DROP, and ROA: Effectiveness of Defenses through the lens of DROP | 2022-10 | Presentation|
| | | **Annotated Schema: Mapping Ontologies onto Dataset Schemas** | 2023-05 | Paper|
|  9/57 | 15% | Annotated Schema: Mapping Ontologies onto Dataset Schemas Slideset | 2023-05 | Presentation|
