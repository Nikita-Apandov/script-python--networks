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
with open('configyaml/dev_afto_new_pass.yaml', 'w') as f: 
    device =  [
        {
        "device_type": "asys",
        "host": "192.168.10.1",
        "username": "admin",
        "password": "12345678",
        "secret": "cisco",
        "commands": ["configure terminal", "aaa new-model", "username admin secret cisco", "end", "write"]
    },
    {
        "device_type": "laim",
        "host": "192.168.10.2",
        "username": "admin",
        "password": "12345678",
        "secret": "cisco",
        "commands": ["configure terminal", "aaa new-model", "username admin secret cisco", "end", "write"]
    },
    {
        "device_type": "star",
        "host": "192.168.10.3",
        "username": "admin",
        "password": "12345678",
        "secret": "cisco",
        "commands": ["configure terminal", "aaa new-model", "username admin secret cisco", "end", "write"]
    }
    ]
    
        
    yaml.dump(device, f) # запимать в фаил