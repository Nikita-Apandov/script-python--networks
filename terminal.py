'''
# создание каталога
import os
os.mkdir('configtxt')
#########################
# создание файла и заполнение

with open('configtxt/sh_cdp_n_r3.txt', 'w') as f:
    mc = """
   R3>show cdp neighbors
Capability Codes: R - Router, T - Trans Bridge, B - Source Route Bridge
                  S - Switch, H - Host, I - IGMP, r - Repeater

Device ID        Local Intrfce     Holdtme    Capability  Platform  Port ID
SW1              Eth 0/0            131          S I      WS-C3750- Eth 0/3
R4               Eth 0/1            145        R S I      2811      Eth 0/0
R5               Eth 0/2            123        R S I      2811      Eth 0/0
    """
    f.write(mc) 
    '''