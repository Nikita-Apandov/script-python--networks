import re
from pprint import pprint
'''
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
'''
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

