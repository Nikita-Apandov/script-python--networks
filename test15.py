import re
from pprint import pprint

#int_line = '''  #MacAddress          IpAddress     Lease(sec)  Type           VLAN  Interface
#------------------  ------------  ----------  -------------  ----  --------------------
#00:09:BB:3D:D6:58   10.1.10.2     86250       dhcp-snooping   10    FastEthernet0/1
#00:04:A3:3E:5B:69   10.1.5.2      63951       dhcp-snooping   5     FastEthernet0/10
#00:05:B3:7E:9B:60   10.1.5.4      63253       dhcp-snooping   5     FastEthernet0/9
#00:09:BC:3F:A6:50   10.1.10.6     76260       dhcp-snooping   10    FastEthernet0/3
#Total number of bindings: 4
'''

match = re.search(r'(?P<mac>\S+)\s+(?P<adderess>\S+)\s+\d+\s+\S+\s+(?P<vlan>\d+)\s+(?P<interface>\S+)', int_line)
#print(match.group('adderess'))
pprint(match.groupdict()) # создает словарь при выводе ключ "address" значение регулярное вырожение

regex = r'(\S+)\s+(\d+)'
result = {}
with open('configtxt/sh_ip.txt') as f:
    for line in f:
        
        match = re.search(regex, line)
        if match:
            intf = match.group(1)
            ip = match.group(2)
            result[intf] = ip
        else:
            continue
pprint(result)


# удобно для обработки конфига 
regex = (r"Device ID: (?P<device>\S+)"
         r"|IP address: (?P<ip>\S+)"
         r"|Platform: (?P<ios>\S+)"
         )
result = {}
with open('configtxt/show_cdp_neighbors_detall.txt') as f:
    for line in f: 
        match = re.search(regex, line)
        if match:   
           # print(f'{match.lastgroup=}')
            group = match.lastgroup
            value = match.group(group)
            if group == "device":
                result[value] = {}
                device = value
            else:
                result[device][group] = value
    print(result)
                
regex = r'(\S+)\s+(\d+.\d+.\d+.\d+)'
with open('configtxt/show_cdp_neighbors_detall.txt') as f:
    content = f.read()
    all_match = re.finditer(regex, content)
    for match in all_match:
        print(match.groups())



'''

'''
# tack 15.1
def get_ip_from_cfg(file):
    ips = []
    regex = r'ip address (\d+.\d+.\d+.\d+)\s+(\d+.\d+.\d+.\d+)'
    with open(file) as f: 
        for line in f:
            match = re.search(regex, line)
            if match:
                ip = match.group(1)
                mask = match.group(2)
                ips.append((ip, mask))

    return ips

if __name__ == '__main__':
    config = 'configtxt/config_r1.txt'
    result = get_ip_from_cfg(config)
    print(result)

# tack 15.1 a-b
def get_ip_from_cfg(file):
    ips = {}
    regex = (r'(?P<intr>interface Ethernet\S/\S)'               
             r'|ip address (?P<ip>\d+\.\d+\.\d+\.\d+) '  
             r'(?P<mask>\d+\.\d+\.\d+\.0)')  
    with open(file) as f: 
        for line in f:
            line = line.strip()
            match = re.search(regex, line)
            if match:   
                group = match.lastgroup
                value = match.group(group)
                print(group)
                if group == "intr":
                    device = value
                else:
                    ip = match.group('ip')
                    mask = match.group('mask')
                    if device not in ips:
                        ips[device] = []
                    ips[device].append((ip, mask))
    return ips

if __name__ == '__main__':
    config = 'configtxt/config_r2.txt'
    result = get_ip_from_cfg(config)
    print(result)
    

# tack 15.2 
def parse_sh_ip_int_br(file):
    conf = []
    regex = r'(?P<int>FastEther\S+\d)\s+(?P<ip>\d+.\d+.\d+.\d+)\s+\S+\s+\S+\s+(?P<stat>up|down)\s+(?P<prot>up|down)'
    with open(file) as f: 
        for line in f: 
            line = line.strip()
            match = re.search(regex, line)
            if match:
                int = match.group('int')
                ip = match.group('ip')
                stat = match.group('stat')
                prot = match.group('prot')
                conf.append((((int, ip, stat, prot))))
    return conf

if __name__ == '__main__':
    config = 'configtxt/sh_ip_int_br.txt'
    result = parse_sh_ip_int_br(config)
    pprint(result)
    

# task 15.2a
def convert_to_dict(headers, data):
    out = []
    for record in data:
        entry = dict(zip(headers, record))
        out.append(entry)
    return out

if __name__ == '__main__':
    headers = ["hostname", "ios", "platform"]
    data = [
    ("R1", "12.4(24)T1", "Cisco 3825"),
    ("R2", "15.2(2)T1", "Cisco 2911"),
    ("SW1", "12.2(55)SE9", "Cisco WS-C2960-8TC-L"),
]
    result = convert_to_dict(headers, data)
    pprint(result)
  
# task 15.3
def convert_ios_nat_to_asa(nat_cisco, nat_asa):
    with open(nat_cisco) as c, open(nat_asa, 'w') as a:
        for line in c: 
            line = line.strip()
            if not line.startswith('ip nat inside source static'):
                continue
            parts = line.split()
            protocol = parts[5]  # tcp или udp
            inside_ip = parts[6]
            inside_port = parts[7]
            outside_interface = parts[9]
            outside_port = parts[10]
            # Формируем строку ASA NAT
            asa_rule = f"object network NAT_{inside_ip}_{inside_port}\n"
            asa_rule += f" host {inside_ip}\n"
            asa_rule += f" nat ({outside_interface},outside) static interface service {protocol} {inside_port} {outside_port}\n"
            # Записываем правило в файл ASA
            a.write(asa_rule + '\n')
    return 
if __name__ == '__main__':
    nat_cisco = 'configtxt/cisco_nat_config.txt'
    nat_asa = 'configtxt/asa_nat_config.txt'
    result = convert_ios_nat_to_asa(nat_cisco, nat_asa)
    pprint(nat_asa)
     
# task 15.4
import re
from pprint import pprint

def get_ints_without_description(config):
    out = []
    # Отдельные regex для интерфейса и IP адреса
    regex_interface = re.compile(r'^interface (\S+)')
    regex_ip = re.compile(r'^ip address (\d+\.\d+\.\d+\.\d+) (\d+\.\d+\.\d+\.0)')
    
    with open(config) as f:
        lines = f.readlines()
    
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        int_match = regex_interface.match(line)
        
        if int_match:
            # Проверяем есть ли 'description' в следующих 3 строках
            has_description = False
            for j in range(i + 1, min(i + 4, len(lines))):
                if 'description' in lines[j].lower():
                    has_description = True
                    break
            if has_description:
                i += 1
                continue
            
            # Если description нет, ищем IP адрес в следующем блоке
            ip_addr = None
            mask = None
            for k in range(i + 1, len(lines)):
                m = regex_ip.match(lines[k].strip())
                if m:
                    ip_addr = m.group(1)
                    mask = m.group(2)
                    break
            
            interf = int_match.group(1)
            out.append((interf, ip_addr, mask))
        
        i += 1
    
    return out

if __name__ == '__main__':
    config = 'configtxt/config_r1.txt'
    result = get_ints_without_description(config)
    pprint(result)
 '''
# task 15.5
def generate_description_from_cdp(config):
    out = {}
    regex = re.compile(
        r'(?P<device>\S+)\s+'
        r'(?P<inter>Eth\s*\S+)\s+'
        r'\d+\s+'                    # Holdtime - число, пропускаем
        r'[\w\s]+\s+'                # Capability - буквы/пробелы, пропускаем
        r'\S+\s+'                    # Platform - пропускаем
        r'(?P<port>Eth\s*\S+)'      # Port ID
    )
    with open(config) as f: 
        for line in f: 
            int_match = regex.search(line)
            if int_match:
                device = int_match.group('device')
                inter = int_match.group('inter')
                port = int_match.group('port')
                out[inter] = (f'Description Connected to {device} port {port}')
    return out


if __name__ == '__main__':
    config = 'configtxt/sh_cdp_n_sw1.txt'
    result = generate_description_from_cdp(config)
    pprint(result)