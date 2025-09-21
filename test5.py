
#5.1 (abcd)
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
devices = ', '.join(london_co.keys()) # собрали список ключей в одну строку с указанным разделителем 
spicok = input(f'Введите имя устройства из списка {devices}: ')
device = ', '.join(london_co[spicok].keys()) 
parametr = input(f'Введите параметер устройства из списка {device}: ')
param = parametr.lower() # преобразуем в нижний регистор
out = london_co[spicok].get(param, 'Вы ввели на верный параметр') # если есть выводим значение, если нет выводим предупреждение
print(out)

#5.2 ( a) очень трудно я не понимаю)!
network = input("Введите IP-сети в формате xxx.xxx.xxx.xxx/xx: ")
new = network.split('/')
octet = new[0].split('.')
#octet = bin(int(new[0].replace('.', '')))
mask = '1' * int(new[1]) + '0' * (32 - int(new[1])) # нельзя умножать строку на строку!

mask_one = int(mask[0:8], 2)
mask_two = int(mask[8:16], 2) # конвентируем из двоичной системы в десятичную
mask_three = int(mask[16:24], 2)
mask_four = int(mask[24:32], 2)

print(f'''
Network:
{octet[0]:<10}{octet[1]:<10}{octet[2]:<10}{octet[3]:<10}
{int(octet[0]):08b}  {int(octet[1]):08b}  {int(octet[2]):08b}  {int(octet[3]):08b}

Mask:
/{new[1]}
{mask[0:8]:<10}{mask[8:16]:<10}{mask[16:24]:<10}{mask[24:32]:<10} 
{mask_one:<10}{mask_two:<10}{mask_three:<10}{mask_four:<10}
''')

# 5.3 (a) это гениальный способ обойти циклы с помощью словарей!
access_template = [
"switchport mode access", "switchport access vlan {}",
"switchport nonegotiate", "spanning-tree portfast",
"spanning-tree bpduguard enable"
]
trunk_template = [
"switchport trunk encapsulation dot1q", "switchport mode trunk",
"switchport trunk allowed vlan {}"
]

template = {
    'access': access_template,
    'trunk': trunk_template
}

questions = {
    'access': 'Введите номер VLAN: ',
    'trunk': 'Введите разрешенные VLANы: '
}

mode = input("Введите режим работы интерфейса (access/trunk): ") 
interface = input("Введите тип и номер интерфейса: ")
vlan = input(questions[mode])
print(f'interface: {interface}')
print('\n'.join(template[mode]).format(vlan))
   
