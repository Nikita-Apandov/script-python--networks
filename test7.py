
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




'''
'''

            
        

 
    

# tack 7.1

with open('configtxt/ospf.txt') as f: 
    for line in f: 
        line_new = line.split()
        print(f"""
        Prefix                {line_new[1]}
        AD/Metric             {line_new[2].strip('[]')}
        Next-Hop              {line_new[4].rstrip(',')}
        Last update           {line_new[5].rstrip(',')}
        Outbound Interface    {line_new[6]}
        """)


            
# tack 7.2 (ab)
result = []
ignore = ["duplex", "alias", "configuration"]

with open('configtxt/config_sw1.txt') as f, open('configtxt/result.txt', 'w') as best: 
    for line in f: 
        line = line.strip()
        if any(word in line.lower() for word in ignore):
            continue
        elif line and not line.startswith('!'):
            best.write(f'{line}\n')
with open('configtxt/result.txt') as f: 
    print(f.read())
'''

#task 7.3 (a) это какой то кошмар, но получилось!
def get_vlan_number(line): 
    return int(line.split()[0])

config = []
with open('configtxt/cam_table.txt', 'r') as file: 

    for line in file: 
        if 'DYNAMIC' in line:

            config.append(line.strip())
        else: 
            continue

sorted_lines = sorted(config, key=get_vlan_number)

for line in sorted_lines:
    print(line)

#task 7.3 (b) 
with open('configtxt/cam_table.txt', 'r') as file: 
    vlan =input('Enter VLAN number: ')
    for line in file: 
        line_str = line.split()
        if 'DYNAMIC' and vlan in line_str:
            print(f'{line_str[0]:<10}{line_str[1]:<20}{line_str[3]:<10}')
        else: 
            continue