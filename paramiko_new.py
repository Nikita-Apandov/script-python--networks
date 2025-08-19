
import paramiko
import time
import re
import socket
from pprint import pprint

def send_show_command(ip, user, password, command, short_sleep=0.2, max_read=10000, long_sleep=2):
    try:   
        cl = paramiko.SSHClient() # говорим что мы клиент SSH
        cl.set_missing_host_key_policy(paramiko.AutoAddPolicy()) # что делать если подключился к устройству впервые
        cl.connect(
        hostname=ip,
        username=user,
        password=password,
        look_for_keys=False, # отключение аудентификации по ключу
        allow_agent=False, # отключение аудентификации по ключу
            )
    except socket.timeout: # не смог подключиться
        print(f'Не удалось подключиться к {ip}')
        return
    except paramiko.ssh_exception.AuthenticationException:
        print(f'Не верный логин или пароль для: {ip}')
        return
    with cl.invoke_shell() as ssh: # вызываем инетарктивную ссессию в которой будем работать
        ssh.recv(max_read)
        time.sleep(short_sleep)
        ssh.recv(max_read)
        time.sleep(short_sleep)
        output = ssh.recv(max_read).decode('utf-8')
        match = re.search(r'([\w.@-]+[>#])\s*$', output)
        if match:
            prompt = match.group(1)
        else:
            prompt = '>'

        ssh.send(command + '\n')
        output = read_until(ssh, prompt)
        return output
        
def read_until(ssh_conn, prompt, short_sleep=1):
    output = ''
    ssh_conn.settimeout(5)
    while True: 
            time.sleep(short_sleep)
            try:
                part = ssh_conn.recv(100).decode('utf-8')
            except socket.timeout:
                break
            print('='*50)
            print(part)
            output += part
            if prompt in output:
                break
    output = output.replace('\r\n', '\n')
    return output        

if __name__ == '__main__':
    ip_list = ["192.168.0.99"]
    commands = "ping 192.168.0.1"
        #user = input('Username: ') 
        #password = getpass.getpass('Password: ')
    for ip in ip_list:
        out = send_show_command(ip, "admin", "12345678", commands)
        pprint(out, width=120)   