
#username = input('Введите имя пользователя: ')
#password = input('Введите пароль: ')
'''
def check_passwd(username, password):
    if type(username) != str or type(password) != str:
        raise ValueError('Надо передавать строки')
    if len(password) < 8:
        print('Пароль слишком короткий')
        return False
    elif username.lower() in password.lower():
        print('Пароль содержит имя пользователя')
        return False
    else:
        print(f'Пароль для пользователя {username} установлен')
        return True
data = [
    ['user1', '324325wewer345'],
    [34, 23],
    [34, 23],
    ['user2', 'sdfsdgsd'],
    ['user3', 'user3dsfjsdgs'],
]
correct_user = []
wrong_user = []
for user, passwd in data: 
    print(user, passwd)
    try:
        check = check_passwd(user, passwd)
    except ValueError as error:
        print(error)
    else:
        if check: 
            correct_user.append(user)
        else:
            wrong_user.append(user)
print(correct_user)
print(wrong_user)



from pprint import pprint
def get_intf(filename):
    result = {}
    with open(filename) as file:
        for line in file: 
            if 'line protocol' in line:
                interface = line.split()[0]
            elif 'MTU is' in line:
                mtu = line.split()[-2]
                result[interface] = mtu
                
    return result

#r1 = get_intf('octet.txt')
#pprint(r1) 
config_list = ("octet.txt", "result.txt", "sh_ip.txt")
for cfg in config_list:
    result = get_intf(cfg)
    pprint(result)
'''

def check_passwd(username, password, min_len=8, check_numbers=False):
    print(f'{username} {password} {min_len=}')
    if len(password) < min_len:
        print('Пароль слишком короткий')
        return False
    elif username.lower() in password.lower():
        print('Пароль содержит имя пользователя')
        return False
    elif check_numbers and len(set('1234567890') & set(password)) < 3:
        print('пароль должен содержать не менее 3 чисел')
        return False
    else:
        print(f'Пароль для пользователя {username} установлен')
        return True
    
check_passwd('admin', 'adsfsdgsdfgsdf234234234')