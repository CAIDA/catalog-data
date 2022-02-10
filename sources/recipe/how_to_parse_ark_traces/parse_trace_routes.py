import sys
import json
import socket

def simple_ip_path(ark_trace):
    
    simple_trace_path_text = '-> traceroute to {} ({}), {} hops max, {} byte packets\n'
    simple_hop_path_text = '\t{}) Hop Address: {} ({}) | RTT: {:.3f} ms'
    
    trace_dst_ip = ark_trace['dst']
    trace_dst_name = socket.getfqdn(ark_trace['dst'])
    trace_hop_count = ark_trace['hop_count']
    trace_byte_packets = ark_trace['probe_count']
    
    path_counter = 1
    
    print(simple_trace_path_text.format(trace_dst_name, trace_dst_ip, 
                                        trace_hop_count, trace_byte_packets))
    print('{')
    
    hops = ark_trace['hops']
    
    for hop in hops:
        
        hop_addr_ip = hop['addr']
        hop_addr_name = socket.getfqdn(hop['addr'])
          
        hop_rtt = hop['rtt']
        
        print(simple_hop_path_text.format(path_counter, hop_addr_name, hop_addr_ip, hop_rtt))
        path_counter += 1
    
    print('}')


def read_warts_file():
    
    # read one line at a time from std in
    warts_json_file = sys.stdin
    # ignore first line
    next(warts_json_file)
    
    print('\n')
    # process it a line at a time
    for warts_line in warts_json_file:
        ark_trace = json.loads(warts_line)
        simple_ip_path(ark_trace)
        
def main():
    
    read_warts_file()

if __name__ == "__main__":
    main()
