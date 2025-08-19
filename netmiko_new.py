


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
        "host": "192.168.0.99",
        "username": "admin",
        "password": "12345678"
    }
    commands = ["ip address print"]
    result = send_show_command(device, commands)
    pprint(result, width=1200)
    input("Нажмите Enter что бы продолжить...")