import paramiko
import logging
import time
import socket
import yaml
from pprint import pprint
from concurrent.futures import ThreadPoolExecutor, as_completed

# автоматический сбор логов маршрутизаторов 
# эта строка указывает, что лог-сообщения paramiko будут выводиться
# только если они уровня WARNING и выше
logging.getLogger("paramiko").setLevel(logging.WARNING)
logging.basicConfig(
    format = '%(asctime)s %(threadName)s %(levelname)s: %(message)s',
    level=logging.DEBUG)

def send_show(device, max_bytes=1000, short_pause=1, long_pause=5):
    host = device["host"]
    username = device["username"]
    password = device["password"]
    secret = device["secret"]
    device_type = device["device_type"]
    commands = device["commands"]
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
        with client.invoke_shell() as ssh: # поддержание ссесии ssh
            logging.info(f'===>  Сессия с: {device_type} активна')
            ssh.send("enable\n") # вход в режим enable
            time.sleep(short_pause)
            ssh.send(f"{secret}\n") # ввод пароля режима enable
            time.sleep(short_pause) # сон менжду командами
            for command in commands:
                ssh.send(f"{command}\n")
                time.sleep(long_pause)
                try:
                    while True:
                        part = ssh.recv(max_bytes).decode("utf-8").replace("\r\n", "\n") # метод чтения и записи вывода команды
                        # Удалить BS символы (backspace)
                        while '\b' in part:
                            bs_index = part.find('\b') # поиск символа пробела
                            if bs_index > 0:
                                part = part[:bs_index-1] + part[bs_index+1:]  # удаляем символ перед BS и сам BS
                            else:
                                part = part.replace('\b', '', 1)  # удаляем BS, если он в начале
                        output += part
                        if '--More--' in part: 
                            ssh.send(' ') # пробел что бы прогнать конфиг
                        elif part.endswith(('#', '>')):
                            break
                        time.sleep(short_pause)
                except socket.timeout:
                    pass
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
    
def collect_data(devices, output_file, max_threads=10):
    error = []
    save = []
    with ThreadPoolExecutor(max_workers=max_threads) as ex: # указываем кол-во потоков
        
        future_list = [ex.submit(send_show, dev) for dev in devices] # выполнение функции в одном из потоков, передает данные в порядке пергвого выполненного в отличии от map()
         
        for dev, future in zip(devices, future_list): # cвязали два списка по индексам с помощью zip
            output = future.result() # записали результат объекта future
            if output == None:
                error.append(dev['device_type'])
            elif output is not None: 
                save.append(dev['device_type'])
                with open(output_file.format(dev['device_type']), 'w') as f: 
                    if isinstance(output, list): # если данные строка, то мы записываем их в фаил 
                        f.write('\n'.join(output) + '\n')
                    else: # вдругих случаях преобразуем данные в строку и записываем 
                        f.write(str(output) + '\n')
                
    return error, save
if __name__ == "__main__":
    
    with open('configyaml/dev_afto_conf.yaml') as f:
        devices = yaml.safe_load(f) # считываем и преобразуем yaml в тип данных который понимает python (словари, списки)
        error, save = collect_data(devices, 'config_{}.txt')
        pprint("Список узлов запись конфигурации которых не удалась:")
        pprint(error)
        print() # пустая строка для разделения вывода
        pprint("Список успешно сохранённых узлов:")
        pprint(save)
        print() # пустая строка для разделения вывода
        input('Нажмите Enter для завершения.')