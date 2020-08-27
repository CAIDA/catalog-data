## <ins> Introduction </ins> ##




## <ins> Solution </ins> ## 

Visibility - Let the user select an arbitrary date. Once date is selected, download all data collected on that date. Create a mid_info function that creates a a dictionary mapping Monitor ID to city, country and ipv6 as links seen on that day. 



## <ins> Background </ins> ## 

### IPv6 address ###
• An *IPv6 address* is a 128-bit unique address that is used to recognize a computer network or a machine. All computers on the same data network share the same IPv6 address.\
• IPv6 addressing is a successor to IPv4 addressing. \
• An IPv4 address is 32 bit, whereas an IPv6 address is 128 bit. \
• **IPv6 Prefix** - The leftmost fields of the IPv6 address contain the prefix, which is used for routing IPv6 packets. \
• IPv6 prefixes have the following format:\
`prefix/length in bits` \
• e.g. Consider the IPv6 address : `2001:db8:3c4d:0015:0000:0000:1a2f:1a2b/48` \
• In this case, 48 is the length of the prefix, i.e. the IPv6 prefix is the first 48 bits of the IP address - `2001:db8:3c4d` \
• More information on IPv6 addresses and prefixes found [here]( https://docs.oracle.com/cd/E19253-01/816-4554/6maoq01nv/index.html ).

### IPv6 AS links ###
• **Direct link** : A direct AS link exists if two adjacent IP hops in a traceroute path map to two distinct ASes. \
• **Indirect link** : An indirect AS link exists if two ASes in an AS path are separated by a gap caused by either an unresponsive hop or an inability to
map an IP address to an AS number. \
• More information on the data format of the test datasets can be found in the metadata section at the top of the test datasets. 

## <ins> Caveats  </ins> ## 
