import sys
import json
import socket

def simple_ip_path(ark_trace):
    
    simple_trace_path_text = '-> traceroute to {} ({}), {} hops max\n'
    simple_hop_path_text = '\t{}) Hop Address: {} ({}) | RTT: {:.4} ms | TTL: {} ms'
    
    trace_dst_ip = ark_trace['dst']
    trace_dst_name = socket.getfqdn(ark_trace['dst'])
    trace_hop_count = ark_trace['hop_count']
    
    path_counter = 1
    
    print(simple_trace_path_text.format(trace_dst_name, trace_dst_ip, trace_hop_count))
    print('{')
    
    for hop in ark_trace['hops']:
        
        hop_addr_ip = hop['addr']
        hop_addr_name = socket.getfqdn(hop['addr'])
          
        hop_rtt = hop['rtt']
        hop_ttl = hop['reply_ttl']
        
        
        print(simple_hop_path_text.format(path_counter, hop_addr_name, hop_addr_ip, hop_rtt, hop_ttl))
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
