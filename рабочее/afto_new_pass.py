import paramiko
import logging
import time
import socket
import yaml
from pprint import pprint
from concurrent.futures import ThreadPoolExecutor, as_completed

logging.getLogger("paramiko").setLevel(logging.WARNING)
logging.basicConfig(
    format = '%(asctime)s %(threadName)s %(levelname)s: %(message)s',
    level=logging.DEBUG)

def session(dev, max_bytes=1000, short_pause=1, long_pause=5): # функция подключения и выполнения команд
    host = dev["host"]
    username = dev["username"]
    password = dev["password"]
    secret = dev["secret"]
    device_type = dev["device_type"]
    commands = dev["commands"]
    output = ''
    try:
        logging.info(f'===>  Попытка подключения к: {device_type}')
        client = paramiko.SSHClient() # создание ssh клиента
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy()) # настройка политики, которая автоматически принимает и добавляет ключ хоста, если ранее его не было
        client.connect(hostname=host, 
                    username=username, 
                    password=password, 
                    timeout=5, # ожидание отклика от сервера
                    look_for_keys=False, 
                    allow_agent=False
                    )
    
        with client.invoke_shell() as ssh: 
            logging.info(f'===>  Сессия с: {device_type} активна')
            ssh.send("enable\n")
            time.sleep(short_pause)
            ssh.send(f"{secret}\n")
            time.sleep(short_pause)
            for command in commands:
                ssh.send(f"{command}\n")
                time.sleep(short_pause)
                part = ssh.recv(max_bytes).decode("utf-8").replace("\r\n", "\n")
                output += part
            client.close()
            logging.info(f'<===  Сессия с {device_type} завершина')
    except TimeoutError:
        print(f"Узел: {device_type} в сети не найден")
        return    
    except paramiko.ssh_exception.AuthenticationException:
        print(f"Не верный логин или пароль от: {device_type}")
        return    
    except paramiko.ssh_exception.SSHException:
        print(f"Не удалось подключится к: {device_type} проверьте качество канала связи")
        return 
    except Exception: 
        print("Другая ошибка")
        return
    return output

def new_pass(devices, max_threads=10): # функция много поточнисти подключений
    error = []
    save = []
    with ThreadPoolExecutor(max_workers=max_threads) as ex: 
        future_list = [ex.submit(session, dev) for dev in devices]
        for dev, future in zip(devices, future_list):
            output = future.result()
            if output == None:
                error.append(dev['device_type'])
            else:
                save.append(dev['device_type'])
    return error, save

if __name__ == "__main__":
    with open("configyaml/dev_afto_new_pass.yaml") as f:
        devices = yaml.safe_load(f) # преобразуем yaml в python
        error, save = new_pass(devices) 
        pprint("Список узлов на которых не удалось сменить пароль:")
        pprint(error)
        print() # пустая строка для разделения вывода
        pprint("Список узлов на которых смена пароля была успешна:")
        pprint(save)
        print() # пустая строка для разделения вывода
        input('Нажмите Enter для завершения.')