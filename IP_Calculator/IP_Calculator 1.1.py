import colorama
colorama.init()

#проверка правильности ввода данных
while True:
    def is_valid_ip(ip_address):
        parts = ip_address.split('.')
        if len(parts) != 4:
            return False
        for part in parts:
            if not part.isdigit():
                return False
            num = int(part)
            if num < 0 or num > 255:
                return False
        return True


    def is_valid_mask(mask):
        if not mask.isdigit():
            return False
        num = int(mask)
        return 0 <= num <= 32


    network = input("Введите IP-адрес (10.10.10.0/24) или префикс (24): ")

    #  блок для проверки, была ли отдельно ввкдка только маска (только цифры)
    if network.isdigit():  # Пользователь ввёл только маску
        mask_length = int(network)
        if not is_valid_mask(str(mask_length)):  # Проверка на валидность маски
            print("\033[91mНеверная маска\033[0m")
            print()
            continue
        else:
            # Только маска была указана, переходим сразу к выводу
            mask_binary = "1" * mask_length + "0" * (32 - mask_length)
            mask = [
                int(mask_binary[0:8], 2),
                int(mask_binary[8:16], 2),
                int(mask_binary[16:24], 2),
                int(mask_binary[24:32], 2)
            ]
            
            # Цветовые коды
            Y = "\033[33m"  # Жёлтый цвет
            Z = "\033[32m"  # Зелёный цвет
            R = "\033[0m"   # Сброс цвета
            
            # Отображаем только маску
            print(f'{Y}Маска:{R} {mask[0]}.{mask[1]}.{mask[2]}.{mask[3]}')
            continue
    
    #далее идет стандартная обработка ip адреса
    # Разбиваем на IP и маску
    if '/' not in network:
        print("\033[91mНеверный формат. Используйте IP/маска\033[0m")
        print()
    else:
        ip_str, mask_str = network.split('/')
        if not is_valid_ip(ip_str):
            print("\033[91mНеверный IP-адрес\033[0m")
            print()
        elif not is_valid_mask(mask_str):
            print("\033[91mНеверная маска\033[0m")
            print()
        else:
            # Проверка закончена, далее основная обработка

            # Заменяем "." и "/" на ","
            network = network.replace('.', ',').replace('/', ',')
            network_parts = network.split(",")

            # Получаем IP-адрес и маску
            ip_address = list(map(int, network_parts[:4]))  # Преобразуем первые четыре части в int
            mask_length = int(network_parts[4])  # Пятая часть - это длина маски

            # Создаем двоичную маску
            mask_binary = "1" * mask_length + "0" * (32 - mask_length)

            ip_address_binary = (
                    f"{ip_address[0]:08b}" +
                    f"{ip_address[1]:08b}" +
                    f"{ip_address[2]:08b}" +
                    f"{ip_address[3]:08b}"
            )

            network_bin = ip_address_binary[:mask_length].ljust(32, '0')
            broadcast_bin = ip_address_binary[:mask_length].ljust(32, '1')

            # Преобразуем двоичную сеть в десятичный формат
            network = [
                int(network_bin[0:8], 2),
                int(network_bin[8:16], 2),
                int(network_bin[16:24], 2),
                int(network_bin[24:32], 2)
            ]

            # Преобразуем двоичную маску в десятичный формат
            mask = [
                int(mask_binary[0:8], 2),
                int(mask_binary[8:16], 2),
                int(mask_binary[16:24], 2),
                int(mask_binary[24:32], 2)
            ]

            broadcast = [
                int(broadcast_bin[0:8], 2),
                int(broadcast_bin[8:16], 2),
                int(broadcast_bin[16:24], 2),
                int(broadcast_bin[24:32], 2)
            ]

            Y = "\033[33m"  # желтый цвет
            Z = "\033[32m"
            R = "\033[0m"  # сброс цвета

            ip_template = f'''
-------------------------
{Z}Сеть:{R} {{0}}.{{1}}.{{2}}.{{3}}/{{4}}
{Z}Минимальный IP:{R} {{13}}.{{14}}.{{15}}.{{16}}
{Z}Маска:{R} {{9}}.{{10}}.{{11}}.{{12}}
{Z}Broadcast:{R} {{17}}.{{18}}.{{19}}.{{20}}
{Y}Количество хостов:{R} {{21}}
-----------------------
'''

            if mask_length == 31:
                host_count = 2
            elif mask_length == 32:
                host_count = 1
            else:
                host_count = (2 ** (32 - mask_length)) - 2

            # Правильный расчет минимального IP
            if mask_length in (31, 32):
                min_ip = network  # минимальный IP равен адресу сети
            else:
                # Добавляем +1 к последнему октету сети
                min_ip = network.copy()
                min_ip[3] += 1
                if min_ip[3] > 255:
                    min_ip[3] = 0
                    min_ip[2] += 1
                    if min_ip[2] > 255:
                        min_ip[2] = 0
                        min_ip[1] += 1
                        if min_ip[1] > 255:
                            min_ip[1] = 0
                            min_ip[0] += 1

            print(ip_template.format(
                network[0], network[1], network[2], network[3],
                mask_length,
                mask_binary[0:8], mask_binary[8:16], mask_binary[16:24], mask_binary[24:32],
                mask[0], mask[1], mask[2], mask[3],
                min_ip[0], min_ip[1], min_ip[2], min_ip[3],
                broadcast[0], broadcast[1], broadcast[2], broadcast[3],
                host_count
            ))

