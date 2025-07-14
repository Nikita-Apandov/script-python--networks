# задание 5.1 (a, b, c, d)
'''
london_co = {
    "r1": {
        "location": "21 New Globe Walk",
        "vendor": "Cisco",
        "model": "4451",
        "ios": "15.4",
        "ip": "10.255.0.1"
    },
    "r2": {
        "location": "21 New Globe Walk",
        "vendor": "Cisco",
        "model": "4451",
        "ios": "15.4",
        "ip": "10.255.0.2"
    },
    "sw1": {
        "location": "21 New Globe Walk",
        "vendor": "Cisco",
        "model": "3850",
        "ios": "3.6.XE",
        "ip": "10.255.0.101",
        "vlans": "10,20,30",
        "routing": True
    }
}
deva = ', '.join(london_co.keys())
device = input(f'Введите имя устройства({deva}): ')
print(london_co.get(device, 'Такого устройства нет'))
params = ', '.join(london_co[device].keys())
parameter = input(f'Введите имя параметра ({params}): ')
param_name = parameter.lower()
print(london_co[device].get(param_name, 'Такого параметра нет'))
'''
"""
#задание 5.2 (a)
# Запрос ввода сети у пользователя
ip_input = input("Введите IP-сеть в формате x.x.x.x/yy: ")

# Разделяем IP и маску
ip_part, mask_part = ip_input.split('/')
ip_octets = list(map(int, ip_part.split('.')))
mask_length = int(mask_part)

# Вычисляем маску в десятичном и двоичном формате
mask_bin = "1" * mask_length + "0" * (32 - mask_length)
mask_octets = [int(mask_bin[i:i+8], 2) for i in range(0, 32, 8)]

# Вывод информации о сети
print("Network:")
print(" ".join(str(octet) for octet in ip_octets))
print(" ".join(f"{octet:08b}" for octet in ip_octets))
print()
print("Mask:")
print(f"/{mask_length}")
print(" ".join(str(octet) for octet in mask_octets))
print(" ".join(mask_bin[i:i+8] for i in range(0, 32, 8)))



#задание 5.3 

switchort = input("Введите режим работы интерфейса (access/trunk): ") 
interface = input("Введите тип и номер интерфейса: ")
vlan = input("Введите номер влан(ов): ")
print(access_template.get(switchort, 'Такого устройства нет'))

access_template = [
    "switchport mode access", "switchport access vlan {}",
    "switchport nonegotiate", "spanning-tree portfast",
    "spanning-tree bpduguard enable"
]

trunk_template = [
    "switchport trunk encapsulation dot1q", "switchport mode trunk",
    "switchport trunk allowed vlan {}"
]

"""

########################################################################
# 5.1 (abcd)
london_co = {
    "r1": {
        "location": "21 New Globe Walk",
        "vendor": "Cisco",
        "model": "4451",
        "ios": "15.4",
        "ip": "10.255.0.1"
    },
    "r2": {
        "location": "21 New Globe Walk",
        "vendor": "Cisco",
        "model": "4451",
        "ios": "15.4",
        "ip": "10.255.0.2"
    },
    "sw1": {
        "location": "21 New Globe Walk",
        "vendor": "Cisco",
        "model": "3850",
        "ios": "3.6.XE",
        "ip": "10.255.0.101",
        "vlans": "10,20,30",
        "routing": True
    }
}
devaiss = ', '.join(london_co.keys())
sors = input(f"Введите имя устройства {devaiss}: ")
deva = ', '.join(london_co[sors].keys())
parametr = input(f"Введите имя параметра ({deva}): ")
para = parametr.lower()
out = london_co[sors].get(para, "Значения нет")
print(out)
#5.2 
octet = input("Введите IP-сети в формате xxx.xxx.xxx.xxx/xx: ")
