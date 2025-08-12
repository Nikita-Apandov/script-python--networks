'''
import subprocess

ip_list = ['8.8.8.8', '1.1.1.1']

for ip in ip_list:
    print(f"Pinging {ip}...")
    reply = subprocess.run(['ping', '-n', '3', ip], 
                           stdout=subprocess.PIPE, # перехват потока вывода 
                           stderr=subprocess.PIPE, # перехват потока ошибок 
                           #stdout=subprocess.DEVNULL, # удаление потока вывода 
                           encoding='cp866', # выбор кодировки расшифровки 
                           shell=True) # преобразования потока вывода в определенную кодировку
    print(reply.stdout + reply.stderr) # вывод потока вывода и ошибок 

    if reply.returncode == 0: # если команда отработала коректно выдает 0
        print(f"Адрес {ip} пингуется")
    else:
        print(f"Адрес {ip} не пингуется")


import os 
#os.mkdir('test')
os.listdir(".")

import ipaddress
ip1 = ipaddress.ip_address('19.10.10.1')
ip2 = ipaddress.ip_address('195.120.130.1')
ip1.is_global #проверяем чем является адрес в сети 
ip1.is_private #проверяем чем является адрес в сети 
ip1.is_multicast #проверяем чем является адрес в сети 

str(ip1) # сдалали строку из адресса 
ip1 < ip2 # можно выполнять каректные проверки 

import ipaddress
ip_list = ['18.23.34.6', '1.23.34.6', '148.23.34.6', '14.23.34.6',]
ip_list_new = [ipaddress.ip_address(ip) for ip in ip_list]
print(sorted(ip_list_new))

import ipaddress

sl = ipaddress.ip_network('10.10.10.0/24')
print(sl.broadcast_address) # отображение броуткаста сети
print(sl.with_hostmask) # вариант отображения маски сети
print(sl.with_netmask) # вариант отображения маски сети
print(sl.with_prefixlen) # вариант отображения маски сети
print(sl.num_addresses) # кол-во адресов в сети 

from tabulate import tabulate

sh_ip_int_br = [('FastEthernet0/0', '15.0.15.1', 'up', 'up'),
    ('FastEthernet0/1', '10.0.12.1', 'up', 'up'),
    ('FastEthernet0/2', '10.0.13.1', 'up', 'up'),
    ('Loopback0', '10.1.1.1', 'up', 'up'),
    ('Loopback100', '100.0.0.1', 'up', 'up')]
print(tabulate(sh_ip_int_br)) # делает таблици в коде

'''
# tack 12.1-3
import subprocess
from tabulate import tabulate
def network(ip_list):
    list1 = []
    list2 = []
    for ip in ip_list: 
        print(f'Ping {ip}')
        reply = subprocess.run(['ping', '-n', '3', ip], 
        stdout=subprocess.PIPE, 
        stderr=subprocess.PIPE) 
        
        if reply.returncode == 0:
            list1.append(ip)
        else:
            list2.append(ip)
    return (list1, list2)

def convert_ranges_to_ip_list(ip_list):
    result = []
    for item in ip_list:
        if '-' in item:
            # Разбиваем на части по дефису
            parts = item.split('-')
            start_ip = parts[0]
            
            # Проверяем, является ли вторая часть полным IP или только последним октетом
            if '.' in parts[1]:
                # Формат "10.1.1.1-10.1.1.10"
                end_ip = parts[1]
                last_octet = int(end_ip.split('.')[-1])
            else:
                # Формат "10.1.1.1-10"
                last_octet = int(parts[1])
            
            # Извлекаем первые три октета из начального IP
            base_ip = '.'.join(start_ip.split('.')[:-1])
            # Извлекаем последний октет из начально IP
            first_octet = int(start_ip.split('.')[-1])
            
            # Генерируем все IP в диапазоне
            for octet in range(first_octet, last_octet + 1):
                ip = f"{base_ip}.{octet}"
                result.append(ip)
        else:
            # Просто добавляем IP, если это не диапазон
            result.append(item)
    return result

def print_ip_table(reachable, unreachable):
    # Определяем максимальную длину списков
    max_len = max(len(reachable), len(unreachable))
    
    # Создаем список строк таблицы
    table_data = []
    for i in range(max_len):
        # Получаем текущие IP или пустую строку, если список закончился
        if i < len(reachable):
            reach_ip = reachable[i] 
        else:
            ""
        unreach_ip = unreachable[i] if i < len(unreachable) else ""
        table_data.append([reach_ip, unreach_ip])
    print(table_data)
    # Заголовки таблицы
    headers = ["Reachable", "Unreachable"]
    
    # Выводим таблицу с grid-форматом
    print(tabulate(table_data, headers=headers, tablefmt="grid"))


if __name__ == '__main__':
    ip_list = [
    '8.8.8.8',
    '1.1.1.1'
    ]
    converted_list = convert_ranges_to_ip_list(ip_list)
    reachable_ips, unreachable_ips = network(converted_list)
    
    print_ip_table(reachable_ips, unreachable_ips)
   
  








