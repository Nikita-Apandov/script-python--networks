# задание 4.1 
#nat = "ip nat inside source list ACL interface FastEthernet0/1 overload"
#nat.replace('Fast', 'Gigabit')работает в cmd ipython

# задание 4.2
#mac = "AAAA:BBBB:CCCC"
#mac.replace(':', '.')
#".".join(mac)работает в cmd ipython

# задание 4.3 
#config = "switchport trunk allowed vlan 1,3,10,20,30,100"
#words = config.split()
#vlans_str = words[-1]
#vlans = vlans_str.split(",")
#print(vlans)

# задание 4.4 
#vlans = [10, 20, 30, 1, 2, 100, 10, 30, 3, 4, 10]
#sorted(vlans) сортировали по возрастанию 
#result = sorted(vlans)
#set(result) преобразовали во множесто для удаления повторяющихся элементов 
#print(result) работает в cmd ipython

#задание 4.5 
#command1 = "switchport trunk allowed vlan 1,2,3,5,8"
#command2 = "switchport trunk allowed vlan 1,3,8,9"
#wor1 = command1.split()
#wor2 = command2.split()
#vlans_1 = wor1[-1]
#vlans_2 = wor2[-1]
#vl1 = vlans_1.split(",")
#vl2 = vlans_2.split(",")
#set(vl1)
#set(vl2)
#v1 = set(vl1)
#v2 = set(vl2)
#v1 & v2
#result =  v1 & v2
#print(result)
'''
#задание 4.6
ospf_route = "    10.0.24.0/24 [110/41] via 10.0.13.3, 3d18h, FastEthernet0/0"

# Очищаем строку от лишних пробелов и разбиваем на части
net = ospf_route.strip().split()

# Извлекаем нужные данные
prefix = net[0]
metric = net[1].strip('[]')
hop = net[3].strip(',')
last = net[4].strip(',')
interface = net[5].strip()
# Формируем и выводим результат
out = f"""
Prefix {prefix}
AD/Metric {metric}
Next-Hop {hop}
Last update {last}
Outbound Interface {interface}"""
'''

#задание 4.8
#ip = "192.168.3.1"
#ip_templ = '''
#IP address: 
#{:<10}{:<10}{:<10}{:<10}
#{:08b}  {:08b}  {:08b}  {:08b}
#'''
#print(ip_templ.format(192, 168, 3, 1, 192, 168, 3, 1))

#задание 4.7 не работает !!!
"""
mac = "AAAA:BBBB:CCCC"

# Удаляем двоеточия
mac = mac.replace(":", "")

# Переводим каждую hex-цифру в 4-битную двоичную строку и объединяем
binary_str = ''.join(f"{int(c, 16):04b}" for c in mac) 

print(binary_str)
"""

######################################################

# 4.1
nat = "in nat inside source list ACL interface FastEthernet0/1 overload"
result = nat.replace("Fast","Gigabit")
print(result)
# 4.2 
mac = "AAAA:BBBB:CCCC"
mac2 = mac.replace(":",".")
print(mac2)
# 4.3
config = "switchport trunk allowed vlan 1,3,10,20,30,100"
command = config.split()
result = command[-1].split(",")
print(result)
# 4.4
vlans = [10, 20, 30, 1, 2, 100, 10, 30, 3, 4, 10]
vlans.sort()
result = set(vlans)
print(result)
# 4.5
command1 = "switchport trunk allowed vlan 1,2,3,5,8"
command2 = "switchport trunk allowed vlan 1,3,8,9"
and1 = command1.split()
and2 = command2.split()
vlan1 = and1[-1]
vlan2 = and2[-1]
vl1 = vlan1.split(",")
vl2 = vlan2.split(",")
l1 = set(vl1)
l2 = set(vl2)
res = l1.intersection(l2)
re = list(res)
re.sort()
result = re
print(result)
# 4.6
ospf_route = "       10.0.24.0/24 [110/41] via 10.0.13.3, 3d18h, FastEthernet0/0"
conf = ospf_route.split()
print(f"""
Prefix                {conf[0]}
AD/Metric             {conf[1].strip("[]")}
Next-Hop              {conf[2].rstrip(",")}
Last update           {conf[3].rstrip(",")}
Outbound Interface    {conf[4]}
""")
# 4.7
mac = "AAAA:BBBB:CCCC"
mac = mac.replace(":", "")
mac2 = bin(int(mac, 16))
print(mac2)
# 4.8
ip = "192.168.3.1"
vlan = ip.split(".")
octet = list(map(int, vlan))
print(f""" 
{octet[0]:>10}{octet[1]:>10}{octet[2]:>10}{octet[3]:>10}
{octet[0]:08b}  {octet[1]:08b}  {octet[2]:08b}  {octet[3]:08b}
""")