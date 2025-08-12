
#tack 1
nat = "ip nat inside source list ACL interface FastEthernet0/1 overload"
print(nat.replace('Fast', 'Gigabit'))

#tack 2 
mac = "AAAA:BBBB:CCCC"
print(mac.replace(':', '.'))

#tack 3
config = "switchport trunk allowed vlan 1,3,10,20,30,100"
command = config.split(' ')
result = command[-1].split(',')
print(result)

# tack 4
vlans = [10, 20, 30, 1, 2, 100, 10, 30, 3, 4, 10]
vlans.sort()
result = set(vlans)
print(result)# (set(vlans))

# tack 5
command1 = "switchport trunk allowed vlan 1,2,3,5,8"
command2 = "switchport trunk allowed vlan 1,3,8,9"
com1 = command1.split()
com2 = command2.split() 
result = list(set(com1[-1].split(',')) & set(com2[-1].split(',')))
result.sort()
print(result) 

# tack 6 
ospf_route = "       10.0.24.0/24 [110/41] via 10.0.13.3, 3d18h, FastEthernet0/0"
result = ospf_route.split()
print(f'''
#Prefix                {result[0]}
#AD/Metric             {result[1].strip('[]')}
#Next-Hop              {result[3].rstrip(',')}
#Last update           {result[4].rstrip(',')}
#Outbound Interface    {result[5]}
''')

# tack 7
mac = "AAAA:BBBB:CCCC"
mac_int = str(bin(int(mac.replace(':', ''), 16))[2:]) 
print(mac_int)

# tack 8
ip = "192.168.3.1"
octet = ip.split('.')
print(f""" 
{octet[0]:<10}{octet[1]:<10}{octet[2]:<10}{octet[3]:<10}
{int(octet[0]):08b}  {int(octet[1]):08b}  {int(octet[2]):08b}  {int(octet[3]):08b}
""")