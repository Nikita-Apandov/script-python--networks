
'''
a, d = [1, 2]
#######

inter = ['fast0/1' , 'vlan', '12', '10.3.5.2']
interface, vlan, nomer, ip = inter
print(f'первый вариант {vlan}')
inter, *others, ip = inter 
print(f"второй вариант {others}")
#inter, ip _, _ = inter
new = ['привет', '*inter', 'распоковали в новом списке', ]
###########
'''
from pprint import pprint
result = {}
with open('ospf.txt') as f: 
    for line in f: 
        line_list = line.split()
        if line_list:
            inent, inter, ip, *other = line_list 
            result[inter] = ip
            

pprint(result)

##################################
# полезные функции
