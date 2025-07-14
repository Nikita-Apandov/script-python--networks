


from pprint import pprint
import yaml
from netmiko import (
    ConnectHandler,
    NetmikoTimeoutException,
    NetmikoAuthenticationException,
)


def send_show_command(device, commands):
    result = {}
    try:
        with ConnectHandler(**device) as ssh:
            ssh.enable()
            for command in commands:
                output = ssh.send_command(command)
                result[command] = output
        return result
    except (NetmikoTimeoutException, NetmikoAuthenticationException) as error:
        print(error)


if __name__ == "__main__":
    device = {
        "device_type": "mikrotik_routeros",
        "host": "192.168.0.154",
        "username": "admin",
        "password": "admin"
    }
    commands = ["ip address add address=192.168.0.34/24 interface=ether1", "ip address add address=192.168.0.33/24 interface=ether1", "export"]
    result = send_show_command(device, commands)
    pprint(result, width=120)
    input("Нажмите Enter что бы продолжить...")