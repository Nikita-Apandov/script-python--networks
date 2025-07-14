

#import pexpect # первая библеотека подключения, говорят на винде не работает, но мы не верим, а пробуем

#r1 = pexpect.spawn("ssh admin@192.168.0.154") 
#r1.expect("Password")#метод говорит какой строки надо дождаться 
#r1.sendline("admin") #отправляет указанную строку и добовляет автоматический перевод строки
#r1.expect(">")#читает пока не увидим ">"
#r1.sendline("ip address print") 
#r1.expect(">R1[>#]")# читать до R1> или R1#
#r1.before #вывод информации пользователю которая находится до expect(сколько команд столько expext нужно прописать)
#r1.close()# закрыви сеанс 

from pprint import pprint
import pexpect

def send_show_command(ip, user, password, command):
    print(f"Подключаюсь к {ip}")
    cmd_out_dict =  {}
    try:
        with pexpect.spawn(f"ssh {user}@{ip}", timeout=10 encoding="utf-8") as ssh: #сам закрываетс shh сессию, если не закрывать могут закончится порты для подключения к ssh 
            ssh.expect("Password")

            ssh.sendline(password)
            ssh.expect(">")

            ssh.sendline("ip address print")
            ssh.expect(">")

            if type(commands) == str:      
                commands = [commands]
            for cmd in commands: 
            ssh.sendline(cmd)
            ssh.expect(">")
            output = ssh.before
            uotput = output.replace("\r\n", "\n")
            cmd_out_dict[cmd] = output 
        return cmd_out_dict
    except.pexpect.exceptions.TIMEOUT as error: 
        print(f"Ошибка при подключении к {ip}")


if __name__ == "__main__":
    ip_list = ["192.168.0.154", "192.168.0.130"]
    commands = ["export", "ip address print"]
    for ip in ip_list:
        out = send_show_command(ip, "admin", "admin", commands)
        pprint(out, width=120)   
   

  