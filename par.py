
import paramiko
import time
import socket
from pprint import pprint

def send_show_command(
    ip,
    user,
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
    username=user,
    password=password,
    look_for_keys=False,
    allow_agent=False,
    )
    with cl.invoke_shell() as ssh:
     
        for command in commands:
            ssh.send(f"{command}\n")
            ssh.settimeout(5)

            output = ""
            while True:
                try:
                    part = ssh.recv(max_bytes).decode("utf-8")
                    output += part
                    time.sleep(0.5)
                except socket.timeout:
                    break
            command = output

        return result


if __name__ == "__main__":
    devices = ["192.168.0.154"]
    commands = ["ip address add address=192.168.0.33/24 interface=ether1", "ip address print"]
    result = send_show_command(devices, "admin", "admin", commands)
    pprint(result, width=120)
    input("Нажмите Enter что бы продолжить...")