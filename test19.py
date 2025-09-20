from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed
import logging

import netmiko
import yaml
import paramiko
'''
# автоматический сбор логов маршрутизаторов с метадом map
# эта строка указывает, что лог-сообщения paramiko будут выводиться
# только если они уровня WARNING и выше
logging.getLogger("paramiko").setLevel(logging.WARNING)
logging.basicConfig(
    format = '%(asctime)s %(threadName)s %(levelname)s: %(message)s',
    level=logging.DEBUG)

def send_show(device, show):
    
    host = device["host"]
    logging.info(f'===>  Connection: {host}')
    try:
        with netmiko.ConnectHandler(**device) as ssh:
            ssh.enable()
            result =  ssh.send_command(show)
            logging.info(f'<===  Received:   {host}')
        return result
    except netmiko.NetMikoTimeoutException as error:
        print(f'Не удалось подключиться к {device['host']}')
    except paramiko.ssh_exception.AuthenticationException:
        print(f'Ошибка аутентификации с {device['host']}')


def collect_data(devices, command, output_file, max_threads=2):
    with ThreadPoolExecutor(max_workers=max_threads) as ex:
        results = ex.map(
            send_show, devices, [command]*len(devices) 
            )
        for dev, output in zip(devices, results):
            with open(output_file.format(dev['host']), 'w') as f: 
                f.write(output + '\n')
if __name__ == "__main__":
    with open('devices.yaml') as f:
        devices = yaml.safe_load(f)
    print(collect_data(devices, 'sh clock', 'results_{}.txt'))
#    for dev in devices:
#        print(send_show(dev, 'sh clock'))    
'''

logging.getLogger("paramiko").setLevel(logging.WARNING)
logging.basicConfig(
    format = '%(asctime)s %(threadName)s %(levelname)s: %(message)s',
    level=logging.DEBUG)

def send_show(device, show):
    
    host = device["host"]
    logging.info(f'===>  Connection: {host}')
    try:
        with netmiko.ConnectHandler(**device) as ssh:
            ssh.enable()
            result =  ssh.send_command(show)
            logging.info(f'<===  Received:   {host}')
        return result
    except netmiko.NetMikoTimeoutException as error:
        print(f'Не удалось подключиться к {device['host']}')
    except paramiko.ssh_exception.AuthenticationException:
        print(f'Ошибка аутентификации с {device['host']}')


def collect_data(devices, command, max_threads=2):
    ip_output = {}
    with ThreadPoolExecutor(max_workers=max_threads) as ex:
        future_list = [ex.submit(send_show, dev, command) 
                       for dev in devices]
            
            
        for future in as_completed(future_list):
            print(future.result())
            
    return ip_output         
                
if __name__ == "__main__":
    with open('devices.yaml') as f:
        devices = yaml.safe_load(f)
    print(collect_data(devices, 'sh clock'))