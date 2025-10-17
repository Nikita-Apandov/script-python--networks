import paramiko
import logging
import time
import socket
import yaml
import re
from pprint import pprint
from concurrent.futures import ThreadPoolExecutor, as_completed

# автоматический сбор логов маршрутизаторов 
# эта строка указывает, что лог-сообщения paramiko будут выводиться
# только если они уровня WARNING и выше
logging.getLogger("paramiko").setLevel(logging.WARNING)
logging.basicConfig(
    format = '%(asctime)s %(threadName)s %(levelname)s: %(message)s',
    level=logging.DEBUG)

def send_arp(device, max_bytes=1000, short_pause=1, long_pause=5):
    host = device["host"]
    username = device["username"]
    password = device["password"]
    commands = device["commands"]
    output = ''
    while True:
        try:
            logging.info(f'===>  Попытка подключения к: {host}')
            client = paramiko.SSHClient() # создание ssh клиента
            client.set_missing_host_key_policy(paramiko.AutoAddPolicy()) # настройка политики, которая автоматически принимает и добавляет ключ хоста, если ранее его не было
            client.connect(hostname=host, 
                        username=username, 
                        password=password, 
                        timeout=5, # ожидание отклика от сервера
                        look_for_keys=False, 
                        allow_agent=False
                        )
            with client.invoke_shell() as ssh: # поддержание ссесии ssh
                logging.info(f'===>  Сессия с: {host} активна')
                ssh.send("enable\n") # вход в режим enable
                time.sleep(short_pause)
                ssh.send(f"cisco\n") # ввод пароля режима enable
                time.sleep(short_pause) # сон менжду командами
                
                for command in commands:
                    ssh.send(f"{command}\n")
                    time.sleep(long_pause)
                    while True: # бесконечный цикл без принуждения не закончится
                        if ssh.recv_ready():
                            part = ssh.recv(max_bytes).decode("utf-8").replace("\r\n", "\n") # метод чтения и записи вывода команды
                        # Удалить BS символы (backspace)
                            while '\b' in part:
                                bs_index = part.find('\b') # поиск символа пробела
                                if bs_index > 0:
                                    part = part[:bs_index-1] + part[bs_index+1:]  # удаляем символ перед BS и сам BS
                                else:
                                    part = part.replace('\b', '', 1)  # удаляем BS, если он в начале
                            output += part
                            ####################################### более компактный вариант
                            '''
                            if any(x in part for x in ['--More--', ':', 'lines', '---(more)']):
                                ssh.send(' ')
                            elif '(END)' in part:
                                ssh.send('q')
                            elif part.endswith(('#', '>', '$')):
                                break
                            else:
                                break
                            '''
                            #######################################
                            if '--More--' in part: 
                                ssh.send(' ') # пробел что бы прогнать конфиг
                            elif ':' in part: 
                                ssh.send(' ')
                            elif '(END)' in part: 
                                ssh.send('q')    
                            elif 'lines' in part: 
                                ssh.send(' ')
                            elif part.endswith(('#', '>', '$')):
                                break
                            elif '---(more' in part: 
                                ssh.send(' ')
                            time.sleep(short_pause) 
                        else:
                            break
                
                client.close()
                logging.info(f'<===  Сессия с {host} завершина')
        except TimeoutError:
            print(f"Узел: {host} в сети не найден")
            return    
        except paramiko.ssh_exception.AuthenticationException:
            print(f"Не верный логин или пароль от: {host}")
            username = input('Введите логин еще раз: ')
            password = input('Введите пароль еще раз:  ')
            continue    
        except paramiko.ssh_exception.SSHException:
            print(f"Не удалось подключится к: {host} проверьте качество канала связи")
            return 
        except Exception: 
            print("Другая ошибка")
            return
        return output
def config(result, device):   
    poisk = device["poisk"]       
    print('Данные котороые содержит устройство о указанном адресе:') 
    for line in result: 
        if poisk in line:
            print(line)
        if f"Internet {poisk}" in line:
            print(line)
    while True:
        exit_program = input("Выйти? (y/n): ")
        if exit_program == 'y':
            break
    return
    
if __name__ == "__main__":
    while True:
        host_ip = input("Введите IP устройства: ")
        octets = host_ip.split(".")
        # Проверяем, что 4 октета
        if len(octets) != 4:
            print(f"{host_ip} Не корректен: должно быть 4 октета")
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
            print(f"{host_ip} Не корректен: октеты должны быть числами от 0 до 255")
    user = input("Введите логин: ")
    password = input("Введите пароль: ")
    while True:
        poisk_ip = input("Введите адрес который хотите найти: ")
        octets = poisk_ip.split(".")
        # Проверяем, что 4 октета
        if len(octets) != 4:
            print(f"{poisk_ip} Не корректен: должно быть 4 октета")
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
            print(f"{poisk_ip} Не корректен: октеты должны быть числами от 0 до 255")

    device = {
        "host": host_ip,
        "username": user,
        "password": password,
        "poisk" : poisk_ip,
        "commands": ["show arp", "show ip arp"]
    }
    
    result = send_arp(device)
    result_new = config(result, device)
    input('Нажмите Enter для завершения.')
