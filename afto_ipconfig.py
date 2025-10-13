import subprocess
import re

import ctypes
import sys


def get_current_ip(interface_name):
    result = subprocess.run("ipconfig", shell=True, capture_output=True, text=True)
    output = result.stdout

    # Поиск IP в блоке интерфейса
    pattern = re.compile(rf"{re.escape(interface_name)}.*?IPv4[^:]*: ([\d\.]+)", re.DOTALL | re.IGNORECASE)
    match = pattern.search(output)
    if match:
        return match.group(1)
    return None

def set_static_ip(interface_name, ip_address):
    if ip_address == "192.168.12.3":
        ip = "10.10.10.2"
        mask = "255.255.255.240"
        gw = "10.10.10.1"
        command = f'netsh interface ip set address name="{interface_name}" static {ip} {mask} {gw}'
        subprocess.run(command, shell=True)
    elif ip_address == "10.10.10.2":
        ip = "192.168.12.3"
        mask = "255.255.255.0"
        gw = "192.168.12.1"
        command = f'netsh interface ip set address name="{interface_name}" static {ip} {mask} {gw}'
        subprocess.run(command, shell=True)
        set_dns_servers(interface_name)
    return
def set_dns_servers(interface_name):
    # Установить основной DNS
    primary_dns = '1.1.1.1'
    secondary_dns = '8.8.8.8'
    command_primary = f'netsh interface ip set dns name="{interface_name}" static {primary_dns}'
    subprocess.run(command_primary, shell=True)
    # Добавить дополнительный DNS, если указан
    command_secondary = f'netsh interface ip add dns name="{interface_name}" {secondary_dns} index=2'
    subprocess.run(command_secondary, shell=True)

if __name__ == "__main__":
    iface =  'Ethernet 7'
    print("netsh interface ip show address команда в терминале что бы узнать существующие сетевые интерфейсы")
    info = input("Нажмите Enter что бы продолжить")
    ip = get_current_ip(iface)
    result = set_static_ip(iface, ip)
    
    
    