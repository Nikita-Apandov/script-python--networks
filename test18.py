import yaml
from pprint import pprint
from netmiko import ConnectHandler, NetmikoTimeoutException, NetmikoAuthenticationException
'''
def send_show_command(device, commands, log):
    result = {}
    try:
        if log:
            print(f"Подключение к устройству {device['host']}...")
        with ConnectHandler(**device) as ssh:
            ssh.enable()
            for command in commands:
                output = ssh.send_command(command)
                result[command] = output
        return result
    except (NetmikoTimeoutException, NetmikoAuthenticationException) as error:
        print('Не верный пароль')
    

if __name__ == "__main__":
    device = {
        "device_type": "cisco_ios",
        "host": "192.168.10.1",
        "username": "admin",
        "password": "cisco",
        "secret": "cisco"
    }
    commands = ["sh ip int br"
        ]
    result = send_show_command(device, commands, log=True)
    pprint(result, width=700)
    input("Нажмите Enter что бы продолжить...")

# 18.1 a-b выполняет подключение к списку устройств и выводит на экран список введенных команд на каждом устройстве
def send_show_command(device, commands, log):
    result = {}
    try:
        if log:
            print(f"Подключение к устройству {device['host']}...")
        with ConnectHandler(**device) as ssh:
            ssh.enable()
            for command in commands:
                output = ssh.send_command(command)
                result[command] = output
        return result
    except NetmikoAuthenticationException as error:
        print('Не верный пароль')
    except NetmikoTimeoutException as error:
        print(f'Устройство {device['host']} не доступно')
import yaml

if __name__ == "__main__":
    command = ["show arp"]
    with open("configyaml/devices.yaml") as f:
        devices = yaml.safe_load(f)

    for dev in devices:
        print(send_show_command(dev, command, log=True))
'''
# 18.2 a-c выводит на экран 2 списка с выполнеными командами и не выполнеными и есть возможность остановить прогу 
# в случае появления не выполненной команды
def send_show_command(device, commands, log=True):
    error_msgs = ["Invalid input detected", "Incomplete command", "Ambiguous command"]
    good_commands = []
    bad_commands = []

    if log:
        print(f"Подключение к устройству {device['host']}...")

    try:
        with ConnectHandler(**device) as ssh:
            ssh.enable()
            for command in commands:
                # Важно ставить exit_config_mode=False, чтобы остаться в режиме config
                result = ssh.send_config_set(command, exit_config_mode=False)
    
                if any(err in result for err in error_msgs):
                    bad_commands.append(command)
                    sp = (input(f'{command} не определена. Надо ли выполнять остальные команды? варианты ответа [y]/n:'))
                    if sp in ['n', 'no']:
                        break
                else:
                    good_commands.append(command)

            ssh.exit_config_mode()  # Выходим из конфигурационного режима один раз после всех команд
        print("Успешные команды:")
        print(f"{good_commands}")
        print("Команды с ошибками:")    
        print(f"{bad_commands}")

        return 

    except NetmikoAuthenticationException:
        print("Ошибка аутентификации, неверный пароль.")
    except NetmikoTimeoutException:
        print(f"Устройство {device['host']} недоступно.")
if __name__ == "__main__":
    commands = [
        "interface FastEthernet0/1",
        "ip address 10.",
        "escription Nikitos_core"
    ]

    with open("configyaml/devices.yaml") as f:
        devices = yaml.safe_load(f)

    for dev in devices:
        send_show_command(dev, commands, log=True)
# 18.3 не вижу смысла выполнять так как функции теже что и в предыдущих задания