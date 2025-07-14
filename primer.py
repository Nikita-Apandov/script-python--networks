import paramiko
import time
import socket
from pprint import pprint



def send_show_command(
    ip,
    username,
    password,
    command,
    max_bytes=60000,
    short_pause=1,
    long_pause=5,
):
    cl = paramiko.SSHClient()
    cl.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    cl.connect(
        hostname=ip,
        username=username,
        password=password,
        look_for_keys=False,
        allow_agent=False,
    )
    with cl.invoke_shell() as ssh:
        for command in commands:       
            ssh.send(f"{command}\n")
            time.sleep(short_pause)
        output = ssh.recv(max_bytes).decode("utf-8").replace("\r\n", "\n")
        return output
       




if __name__ == "__main__":
    ip_list = ["192.168.0.154"]
    commands = ["export"]

    result = send_show_command("192.168.0.154", "admin", "admin", commands)
    pprint(result, width=120)
    input("Нажмите Enter что бы продолжить...")


