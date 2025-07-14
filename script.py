import paramiko 
import time
import socket
from pprint import pprint
import re

def send_show_command(ip, user, password, command, 
                      short_sleep=0.2,# спать 0,2 секунды 
                      max_read=10000,# считать указанное кол-во байт
                      long_sleep=2# спать 2 секунды
                      ):
    try:# поместили код в котором могут возникнуть исключения при возникновении которых переходим в блок except
        cl = paramiko.SSHClient() #создаем клиента
        cl.set_missing_host_key_policy(paramiko.AutoAddPolicy())#если подключаемся впервые, автоматически добовляет ключ SSH
        cl.connect(
            hostname=ip,
            username=user,
            password=password,
            look_for_keys=False,# отключение аудентификации по ключам
            allow_agent=False,#отключаем  считывание SSH agent
            timeout=5 # ждать подключение 5 секунд
        )
    except socket.timeout:# выводит икслючение в следующем формате при не удачном подключении
        print(f"Не получилось подключиться к {ip}")
        return
    except paramiko.SSHException as error: # выводит любое сключение в следующей формате 
        print(f"Возникла ошибка на {error} на {ip}")
        return
    
    with cl.invoke_shell() as ssh: #with открывает и закрывает автоматически, открываем сессию, результат используется как переменная ssh
        ssh.send("ip address print\n")
        output = ssh.recv(max_read).decode("utf-8")
        prompt = re.search(r"\S+#", output).group() #читать пока не увидем указанный фрагмент
        ssh.send(f"{command}\n")
      
        output = ""
        ssh.settimeout(5)
        while True: #бесконечный цикл
            time.sleep(short_sleep)
            part = ssh.recv(100).decode("utf-8")#получение данных, декодирование данных, замена последовательности \r\n на \n
            print("="*50)
            print(part)
            output += part 
            if prompt in output:# если увидили указанный фрагмент, то заканчиваем безконечный цикл
                break
        output = output.replace("\r\n", "\n")
        return output
    
if __name__ == "__main__":
    ip_list = ["192.168.0.154"]
    for ip in ip_list:
        out = send_show_command(ip, "admin", "admin", "export")
    pprint(out, width=120)# максимальное кол-во символов на 1 строке
    input("Нажмите Enter что бы продолжить...")