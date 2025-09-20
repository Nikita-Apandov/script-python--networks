


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
            ssh.enable() # если есть пароль на enable 
            for command in commands:
                output = ssh.send_command(command) #  отправлят 1 команду 
                result[command] = output
        return result
    except (NetmikoTimeoutException, NetmikoAuthenticationException) as error:
        print(error)


if __name__ == "__main__":
    device = {
        "device_type": "cisco_ios",
        "host": "192.168.10.1",
        "username": "admin",
        "password": "cisco",
        "secret": "cisco"
    }
    commands = ["show running-config"]
    result = send_show_command(device, commands)
    pprint(result, width=1200)
    input("Нажмите Enter что бы продолжить...")