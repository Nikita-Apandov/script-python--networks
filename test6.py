"""
username = input('Введите имя пользователя: ')
password = input('Введите пароль: ')

if len(password) < 8:
    print('Пароль слишком короткий')
elif username in password:
    print('Пароль содержит имя пользователя')
else:
    print('Пароль для пользователя {} установлен'.format(username))
    print(f'Пароль для пользователя {username} установлен')

#Приобразование строки в число 
ip = "192.168.100.1"
ip.split(".") 
octets = ip.split(".")
octets_int = []
for octet in octets: 
    octets_int.append(int(octet))
print(octets_int)

# Перебор интерфейсов
for number in range(10):
    print(f"interface Ge10/{number}")
"""
# Совмещение for & if  
access_template = ['switchport mode access',
                     'switchport access vlan',
                    'spanning-tree portfast',
                    'spanning-tree bpduguard enable']

access = {'0/12': 10, '0/14': 11, '0/16': 17, '0/17': 150}

for intf, vlan in access.items():
     print('interface FastEthernet' + intf)
     for command in access_template:
         if command.endswith('access vlan'):
             print(' {} {}'.format(command, vlan))
         else:
             print(' {}'.format(command))

# Запрашиваем пароль от пользователя 
username = input("Введите имя пользователя: ")
password = input("Введите пароль: ")

while (
    len(password) < 8 or username.lower() in password.lower()
    or len(set("0123456789")) & set(password) < 3 
): 
    print(f"Пароль для {username} не прошел проверки")
    password = input("Введите пароль еще раз: ")

print(f"Пароль для {username} прошел все проверки")

#работа с исключениями 
# -*- coding: utf-8 -*-

try:
    a = input("Введите первое число: ")
    b = input("Введите второе число: ")
    result = int(a)/int(b)
except (ValueError, ZeroDivisionError):
    print("Что-то пошло не так...")
else:
    print("Результат в квадрате: ", result**2)
finally: 
    print("Вот и сказочке конец, а кто слушал - молодец.")
    

# задание 6.1
mac = ["aabb:cc80:7000", "aabb:dd80:7340", "aabb:ee80:7000", "aabb:ff80:7000"]
for result in mac:
    result.replace(':', '.')
    print(result.replace(':', '.'))

# задание 6.2 (a, b)
while True:
    ip = input("Введите адрес сети: ")
    octets = ip.split(".")

    # Проверяем, что 4 октета
    if len(octets) != 4:
        print(f"{ip} Не корректен: должно быть 4 октета")
        continue

    valid = True
    for octet in octets:
        if not octet.isdigit():
            valid = False
            break
        if not 0 <= int(octet) <= 255:
            valid = False
            break

    if valid:
        break
    else:
        print(f"{ip} Не корректен: октеты должны быть числами от 0 до 255")

print(f"{ip} является корректным")

octets_int = []
for octet in octets: 
    octets_int.append(int(octet))
if 1 <= octets_int[0] <= 223:
    print(f"{ip}: unicast") 
elif 224 <= octets_int[0] <= 239:
    print(f"{ip}: multicast")
elif octets_int == [255, 255, 255, 255]:
    print(f"{ip}: local broadcast")      
elif octets_int == [0, 0, 0, 0]:
    print(f"{ip}: unassigned")
else: 
    print(f"{ip}: unused")

#задание 6.3

trunk_template = [
    "switchport trunk encapsulation dot1q",
    "switchport mode trunk",
    "switchport trunk allowed vlan",
]
trunk = {"0/1": ["add", "10", "20"], 
         "0/2": ["only", "11", "30"], 
         "0/4": ["del", "17"]}

for intf, vlan in trunk.items():
    print(f"interface FastEthernet {intf}")
    action = vlan[0]
    vlans = ",".join(vlan[1:])
    if action == "add":
        vlan_cmd = f"add {vlans}"

    elif action == "only":
        vlan_cmd = vlans
    elif action == "del":
        vlan_cmd = f"remove {vlans}"
    else: 
        vlan_cmd = vlans
    for command in trunk_template:
        if command.endswith("allowed vlan"):
            print(f" {command} {vlan_cmd}")
        else: 
            print(f" {command}")