'''
# строку ip в список 

ip = "192.168.100.1"
ip.split(".")

# метод чтения файла
f = open("file.txt","r")
for line in f: 
    print(line.rstrip)

# если надо из одного файла перенести значения в другой 
with open('r1.txt') as src, open('result.txt', 'w') as dest:
    for line in src:
        if line.startswith('service'):
            dest.write(line)

# прикол от свадьбы
day = int(input('Введите дату заступления: '))

while  day not in (24, 25): 
    print('Не верная дата, выберите число 24 или 25.')
    day = int(input('Введите дату заступления еще раз: '))
    
if day == 25:
    print('26 вы свободны, но пропускаете дату росписи.')
elif day == 24:
    print('Вы успеваете на дату росписи, но 26-27 вас могут вызвать на работу.')
result = input('Горько!')

# преобразование списка чисел в список строк
vlans = [1, 2, 3, 5]
vlans_str = []
for vl in vlans:
    vlans_str.append(str(vl))

# преобразование списка чисел в список строк второй вариант
vlans = [1, 2, 3, 5]
vlans_str = [str(vl) for vl in vlans]

# выбираем из списка строк элементы которые числа
data = ['12', '23', 'sdfsdf', '3242dfs', '134']
digits_only = []
for item in data: 
    if item.isdigit():
        digits_only.append(int(item))
# выбираем из списка строк элементы которые числа второй вариант
data = ['12', '23', 'sdfsdf', '3242dfs', '134']
digits_only = [int(item) for item in data if item.isdigit()]

# заспоковываем вложенный список
vlans = [[12,34,54], [1342,324,554], [132,324,564]]
data = []
for vlan in vlans: 
    for vl in vlan:
        data.append(int(vl))

# или лучше не увлекайся!
vlans = [[12,34,54], [1342,324,554], [132,324,564]]
data = [(int(vl)) for vlan in vlans for vl in vlan]
data = {(int(vl)) for vlan in vlans for vl in vlan} #а тут мы преобразовали в множество

# генерация словорей
data = {
    'iOs': '15.4',
    'iP': '10.10.10.1',
    'mAsk': '255.255.255.0'
}
data_new = {}
for key, value in data.items(): 
    data_new[key.lower()] = value 

# второй вариант
data_new = {key.lower(): value for key, value in data.items()}

# выводим только необходимые элементы из словоря 
keys = 'ios ip '.split()
{key: value for key, value in data_new.items() if key in keys}

# спинер загрузки
import time
spinner = '|/-\|/-\|/-\|'
for i in spinner: 
    print(f"\r{i}", end='', flush=True)
    time.sleep(0.2)

# метод сортировки ip адресов
def bin_ip(ip):
    octets = [int(o) for o in ip.split(".")]
    return ("{:08b}"*4).format(*octets)


ip_list = ['19.32.5.3', '13.56.3.23', '23.54.4.2', '135.32.64.2']
result = sorted(ip_list, key=bin_ip)
print(result)


# собираем данные в словарик

d_keys = ['hostname', 'location', 'vendor', 'model', 'IOS', 'IP']

data = {
    'r1': ['london_r1', '21 New Globe Walk', 'Cisco', '4451', '15.4', '10.255.0.1'],
    'r2': ['london_r2', '21 New Globe Walk', 'Cisco', '4451', '15.4', '10.255.0.2'],
    'sw1': ['london_sw1', '21 New Globe Walk', 'Cisco', '3850', '3.6.XE', '10.255.0.101']
}

london_co = {}

for k in data.keys():
    london_co[k] = dict(zip(d_keys, data[k]))

# использование функции map
nums = [1, 2, 3, 4, 5]
nums2 = [100, 200, 300, 400, 500]
list(map(lambda x, y: x*y, nums, nums2))
[100, 400, 900, 1600, 2500]

# поиск данных в логах с помощью регулярных вырожений 
import re 
match = r'\w+\.\w+\.\w+'
#match = r'\w{4}\.\w{4}\.\w{4}' # другой вариант
#match = r'\w\w\w\w\.\w\w\w\w\.\w\w\w\w' # другой вариант
#match = r'\w+[.:]\w+[.:]\w+' # другой вариант
with open('configtxt/cam_table.txt') as log2:
    for line in log2:
        output = re.search(match, line) # поиск мак адресса в лог файле
        if output:
            print(output.group())
        else:
            continue 
        #output = re.search(r'\w{4}\.\w{4}\.\w{4}', content) # другой вариант
        #output = re.search(r'\w\w\w\w\.\w\w\w\w\.\w\w\w\w', content) # другой вариант
        #output = re.search(r'\w+[.:]\w+[.:]\w+', content) # другой вариант
   

import re 
line = 'R1# show configure cmds' 
match = re.search(r'^.+[>#]', line)
print(match.group) # таким образом узнали имя устройста

# замена формата mac адресса с . на :
import re  
line = ' 100    01bb.c580.7000    DYNAMIC     Gi0/1'
result = re.sub(r'(\w+)+\.(\w+)+\.(\w+)', r'\1:\2:\3', line)    
print(result)
'''
# в один ключ список значений 
my_dict = {}

key = "interface1"
value = ("192.168.1.1", "255.255.255.0")

# Если ключа нет, создаём список, если есть — добавляем в список
if key not in my_dict:
    my_dict[key] = []
my_dict[key].append(value)

print(my_dict)
