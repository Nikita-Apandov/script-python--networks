
# tack 11.1 and 11.2 
'''
from pprint import pprint

def parse_cdp_neighbors(command_output):
    result = {}
    lines = command_output.strip().split('\n')
    device = lines[0].split('>')[0]
    for i, line in enumerate(lines):
        if line.startswith('Device'):
            header_line = i 
            break 
        
    for line in lines[header_line + 1:]:
        if not line.strip():
            continue
        parts = line.split()
        neighbor = parts[0]
        local_intf = parts[1] + parts[2]
        remote_intf = parts[-2] + parts[-1]
        result[(device, local_intf)] = (neighbor, remote_intf)
    return result

def create_network_map(filenames):
    network_map = {}
    for file in filenames:
        with open(file) as f:
            cdp_output = f.read()
            parsed = parse_cdp_neighbors(cdp_output)
            network_map.update(parsed)
    return network_map

if __name__ == "__main__":
    infiles = [
    "configtxt/sh_cdp_n_sw1.txt",
    "configtxt/sh_cdp_n_r1.txt",
    "configtxt/sh_cdp_n_r2.txt",
    "configtxt/sh_cdp_n_r3.txt",
    ]
    topology = create_network_map(infiles)
    pprint(topology)
'''

#tack 11.2a 


     