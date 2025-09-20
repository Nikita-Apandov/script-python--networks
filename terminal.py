import yaml
'''
# создание каталога
import os
os.mkdir('configtxt')
#########################
# создание файла и заполнение


with open('configtxt/devices.txt', 'w') as f:
    mc = """
    device = {
        "device_type": "cisco_ios",
        "host": "192.168.10.1",
        "username": "admin",
        "password": "cisco",
        "secret": "cisco"
    }
    """
    f.write(mc) 
    '''
with open('configyaml/devices.yaml', 'w') as f: 
    device =  [
        {
        "device_type": "asys",
        "host": "192.168.10.1",
        "username": "admin",
        "password": "cisco",
        "secret": "cisco",
        "commands": ["show ip route", "show ip arp"]
    },
    {
        "device_type": "laim",
        "host": "192.168.10.2",
        "username": "admin",
        "password": "cisco",
        "secret": "cisco",
        "commands": ["show ip route", "show ip arp"]
    },
    {
        "device_type": "star",
        "host": "192.168.10.3",
        "username": "admin",
        "password": "cisco",
        "secret": "cisco",
        "commands": ["show ip route", "show ip arp"]
    }
    ]
    
        
    yaml.dump(device, f) # запимать в фаил