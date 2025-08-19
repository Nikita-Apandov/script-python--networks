import csv
from pprint import pprint
import re
'''
s = 'привет'
pa = s.encode('utf-8')# преобразовали в байты 

sa = pa.decode('utf-8') # вернули в строки 
print(sa)

import csv
import pprint
with open('configcsv/ospf.csv') as f: 
    read = list(csv.DictReader(f))
    for line in read: 
        print(line)
'''
# task 17.1
import csv
import os
import re

def write_dhcp_snooping_to_csv(filenames, output):
    header = ['switch', 'mac', 'ip', 'vlan', 'interface']
    rows = []
    
    for filename in filenames:
        switch_name = os.path.basename(filename).split('_')[0]
        with open(filename) as f:
            for line in f:
                # Пропускаем заголовки и пустые строки
                if re.match(r'^[-\s]*$', line) or line.startswith('MacAddress') or 'Total number of bindings' in line:
                    continue
                
                fields = line.split()
                if len(fields) < 6:
                    continue
                
                mac = fields
                ip = fields[1]
                vlan = fields
                interface = fields
                rows.append([switch_name, mac, ip, vlan, interface])
                
    with open(output, 'w', newline='') as o:
        writer = csv.writer(o)
        writer.writerow(header)
        writer.writerows(rows)
        
    # Для проверки можно вывести, но функция возвращает None
    with open(output) as o:
        for row in csv.reader(o):
            print(row)


if __name__ == "__main__":
    filenames = [
        'configtxt/sw1_ospf.txt'
    ]
    write_dhcp_snooping_to_csv(filenames, 'configcsv/ospf.csv')



# не разобрался этот раздел для красоты вывода инфы, пока подождем 