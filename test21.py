import textfsm
from tabulate import tabulate
'''
# Скрипт для обработки вывода команды 
output = '''
#traceroute 90.0.0.9 source 33.0.0.2
#Type escape sequence to abort.
#Tracing the route to 90.0.0.9
#VRF info: (vrf in name/id, vrf out name/id)
# 1 10.0.12.1 1 msec 0 msec 0 msec
# 2 15.0.0.5 0 msec 5 msec 4 msec
# 3 57.0.0.7 4 msec 1 msec 4 msec
# 4 79.0.0.9 4 msec * 1 msec
'''
with open('traceroute.template') as template:
    fsm = textfsm.TextFSM(template)
    result = fsm.ParseText(output)

print(fsm.header)
print(result)

# привила для парсинга скрипта
Value ID (\d+)
Value Hop ([\d.]+)

Start
 ^ +${ID} +${Hop} -> Record
'''

with open('traceroute.template') as template, open('configtxt/show_cdp_neighbors_detall.txt') as output:
    fsm = textfsm.TextFSM(template)
    header = fsm.header
    result = fsm.ParseText(output.read())

print(result)
print(tabulate(result, headers=header))