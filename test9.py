
from pprint import pprint 

#username = input('Введите имя пользователя: ')
#password = input('Введите пароль: ')
'''
def check_passwd(username, password):
    if type(username) != str or type(password) != str:
        raise ValueError('Надо передавать строки')
    if len(password) < 8:
        print('Пароль слишком короткий')
        return False
    elif username.lower() in password.lower():
        print('Пароль содержит имя пользователя')
        return False
    else:
        print(f'Пароль для пользователя {username} установлен')
        return True
data = [
    ['user1', '324325wewer345'],
    [34, 23],
    [34, 23],
    ['user2', 'sdfsdgsd'],
    ['user3', 'user3dsfjsdgs'],
]
correct_user = []
wrong_user = []
for user, passwd in data: 
    print(user, passwd)
    try:
        check = check_passwd(user, passwd)
    except ValueError as error:
        print(error)
    else:
        if check: 
            correct_user.append(user)
        else:
            wrong_user.append(user)
print(correct_user)
print(wrong_user)



from pprint import pprint
def get_intf(filename):
    result = {}
    with open(filename) as file:
        for line in file: 
            if 'line protocol' in line:
                interface = line.split()[0]
            elif 'MTU is' in line:
                mtu = line.split()[-2]
                result[interface] = mtu
                
    return result

#r1 = get_intf('octet.txt')
#pprint(r1) 
config_list = ("octet.txt", "result.txt", "sh_ip.txt")
for cfg in config_list:
    result = get_intf(cfg)
    pprint(result)

######################################
def check_passwd(username, password, min_len=8, check_numbers=False):
    print(f'{username} {password} {min_len=}')
    if len(password) < min_len:
        print('Пароль слишком короткий')
        return False
    elif username.lower() in password.lower():
        print('Пароль содержит имя пользователя')
        return False
    elif check_numbers and len(set('1234567890') & set(password)) < 3:
        print('пароль должен содержать не менее 3 чисел')
        return False
    else:
        print(f'Пароль для пользователя {username} установлен')
        return True
    
check_passwd('admin', 'adsfsdgsdfgsdf234234234')
###############################################

# task 9.1 (a)

def config_access(access_mode, access_config, port_security, security=True):
    config = []
    for intr, vlan in access_config.items():
        config.append(f'{intr}')
        for command in access_mode:
            if command.endswith("access vlan"):
                config.append(f' {command} {vlan}')
            else:
                config.append(f' {command}')
        
        if security:
            for command_security in port_security:
                config.append(f' {command_security}')
    return config


access_mode_template = [
"switchport mode access", "switchport access vlan",
"switchport nonegotiate", "spanning-tree portfast",
"spanning-tree bpduguard enable"
]
access_config = {
"FastEthernet0/12": 10,
"FastEthernet0/14": 11,
"FastEthernet0/16": 17
}

port_security_template = [
"switchport port-security maximum 2",
"switchport port-security violation restrict",
"switchport port-security"
]

result = config_access(access_mode_template, access_config, port_security_template)
pprint(result)


# tack 9.2 

def generate_trunk_config(trunk_mode, trank_config):
    config_dict = {}
    for inter, vlans in trank_config.items(): 
        config = []
        
        for trunk in trunk_mode:        
            if trunk.endswith('allowed vlan'):
                vlan_str = ','.join(str(vlan) for vlan in vlans)
                config.append(f' {trunk} {vlan_str}')
            else:
                config.append(f' {trunk}')
        config_dict[inter] = config
    return config_dict

trunk_mode_template = [
"switchport mode trunk", "switchport trunk native vlan 999",
"switchport trunk allowed vlan"
]

trunk_config = {
"FastEthernet0/1": [10, 20, 30],
"FastEthernet0/2": [11, 30],
"FastEthernet0/4": [17]
}

result = generate_trunk_config(trunk_mode_template, trunk_config)
pprint(result)


# tack 9.3 (a не было конфига для обработки)

def get_int_vlan_map(config):
    config_dict = {}
    interface = ''
    for line in config: 
        if 'interface gigabitEthernet ' in line:
            interface = line.strip()
        elif 'access vlan' in line:
            line = line.split()
            vlan = line[-1]
            config_dict[interface] = vlan
        elif 'allowed vlan' in line:
            line = line.split(' ')
            vlans = line[-1].split(',')
            vlan_str = ', '.join(str(vlan) for vlan in vlans)
            config_dict[interface] = vlan_str.strip()
    return config_dict

with open('configtxt/comutator.txt') as config:     
    result = get_int_vlan_map(config)
    pprint(result)

'''

# tack 9.4 (что бы понять нужно немного подумать)

def convert_config_to_dict(config):
    config_dict = {}
    interface = ""
    configure = [] # вынесли из цикла 
    for line in config: 
        if 'interface Ethernet' in line:
            # сохраняем предыдущий интерфейс перед началом нового 
            if interface and configure:
                config_dict[interface] = configure
            # начинаем новый интерфейс 
            interface = line.strip()
            configure = [] # новый список для нового интерфейса 
        elif interface: # добавляем только если есть активный интерфейс 
            if 'switchport' in line:
                configure.append(line)
            elif 'duplex auto' in line:
                configure.append(line)
            elif 'spanning-tree' in line:
                configure.append(line)
    return config_dict

with open('configtxt/config_sw1.txt') as config_filename: 
    result = convert_config_to_dict(config_filename)
    pprint(result)