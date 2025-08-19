import pexpect
#import getpass # в ввод пароля что бы он не отсвечивался
#password = getpass.getpass()
#print(password)
########################

ssh = pexpect.spawn('ssh admin@192.168.0.99')

ssh.expect('>')
ssh.sendline('interface print')

ssh.expect('>')

show_output = ssh.before.decode('utf-8')
print(show_output)