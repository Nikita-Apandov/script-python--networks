
'''
Получение ключа и значения из одной строки вывода
result =  {}
with open("sh_ip.txt", "r") as file: 
    for line in file: 
        line_list = line.split()
        if line_list and line_list[1][0].isdigit(): # проверили что список не пуст и что первый символ второго элемента число
            interface = line_list[0]
            address = line_list[1]
            result[interface] = address # добавили в словарь

print(result)

Получение ключа и значения из разных строк вывода
result = {}
with open("octet.txt", "r") as file:
    for line in file: 
        if 'line protocol' in line:
            interface = line.split()[0]
        elif 'MTU is' in line:
            mtu = line.split()[-2]
            result[interface] = mtu
print(result)        

Если из вывода команды надо получить несколько параметров
result = {}
with open("octet.txt", "r") as file:
    for line in file: 
        if 'line protocol' in line:
            interface = line.split()[0]
            result[interface] = {}
        elif 'Internet address' in line:
            ip_address = line.split()[-1]
            result[interface]['ip'] = ip_address
        elif 'MTU is' in line:
            mtu = line.split()[-2]
            result[interface]['mtu'] = mtu
print(result)
# (вариант 2)print('{:15}{:17}{}'.format(interface, ip_address, mtu))

#####################################
# task 7.1
with open('ospf.txt', 'r') as file:
    for line in file:
        line_list = line.split()
        if line_list:
            pref = line_list[1]
            ad = line_list[2]
            hop = line_list[3]
            update = line_list[4]
            interface = line_list[5]
            
            print(f"""
Prefix                {pref}
AD/Metric             {ad.strip("[]")}
Next-Hop              {hop.rstrip(",")}
Last update           {update.rstrip(",")}
Outbound Interface    {interface.rstrip(",")}
""")

# task 7.2 a,b
from pprint import pprint

ignore = ["duplex", "alias", "configuration"]
 
with open('config_sw1.txt') as file, open('result.txt', 'w') as dest:
    for line in file:
        
        if '!' in line:
            continue
        elif any(word in line.lower() for word in ignore):
            continue    
        else:
            dest.write(line)
            print(line)
'''

#task 7.3 b не могу сделать a !!!
with open('cam_table.txt', 'r') as file: 
    vlan =input('Enter VLAN number: ')
    for line in file: 
        line_str = line.split()
        if 'DYNAMIC' and vlan in line_str:
            print(f'{line_str[0]:<10}{line_str[1]:<20}{line_str[3]:<10}')
        else: 
            print(f'VLAN {vlan} not found')
            
        

    
