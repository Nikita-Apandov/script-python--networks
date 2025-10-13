'''
# tack 6.1 
mac = ["aabb:cc80:7000", "aabb:dd80:7340", "aabb:ee80:7000", "aabb:ff80:7000"]
mac_new = []
for m in mac: 
    mac_new.append(m.replace(':', '.'))
print(mac_new)

# tack 6.2 (ab)

while True:
    ip = input("Введите IP адресс: ")
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

new = int(octets[3])
if  1 <= new <= 223:
    print('unicast')
elif 224 <= new <= 239:
    print('multicast')
elif ip == '255.255.255.255':
    print('local broadcast')
elif ip == '0.0.0.0':
    print('unassigned')
else: 
    print('unused')
'''
# tack 6.3

trunk_template = [
    "switchport trunk encapsulation dot1q",
    "switchport mode trunk",
    "switchport trunk allowed vlan",
]

trunk = {
        "0/1": ["add", "10", "20"], 
        "0/2": ["only", "11", "30"], 
        "0/4": ["del", "17"]
         }
for inter, vlan in trunk.items():
    print(f'interface FastEthernet {inter}')
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