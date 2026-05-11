import socket
import threading
from datetime import datetime
import sys
import time

def scan_port(ip, port, timeout=1):
    """Проверяет, открыт ли порт на указанном IP"""
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(timeout)
        result = sock.connect_ex((ip, port))
        sock.close()
        if result == 0:
            return True
    except:
        pass
    return False

def scan_ports(ip, start_port, end_port, max_threads=100):
    """Сканирует диапазон портов в многопоточном режиме"""
    open_ports = []
    threads = []
    lock = threading.Lock()
    
    def worker(port):
        if scan_port(ip, port):
            with lock:
                open_ports.append(port)
                print(f"  [+] Порт {port} открыт")
    
    print(f"\n🔍 Сканирование {ip} (порты {start_port}-{end_port})...")
    start_time = time.time()
    
    # Запускаем потоки
    for port in range(start_port, end_port + 1):
        t = threading.Thread(target=worker, args=(port,))
        threads.append(t)
        t.start()
        
        # Ограничиваем количество одновременно работающих потоков
        if len(threads) >= max_threads:
            for t in threads:
                t.join()
            threads = []
    
    # Дожидаемся оставшихся потоков
    for t in threads:
        t.join()
    
    elapsed = time.time() - start_time
    print(f"\n✅ Сканирование завершено за {elapsed:.2f} сек")
    print(f"📊 Найдено открытых портов: {len(open_ports)}")
    return open_ports

def get_service_name(port):
    """Пытается определить службу по номеру порта (часто используемые)"""
    common_ports = {
        21: "FTP",
        22: "SSH",
        23: "Telnet",
        25: "SMTP",
        53: "DNS",
        80: "HTTP",
        110: "POP3",
        143: "IMAP",
        443: "HTTPS",
        445: "SMB",
        993: "IMAPS",
        995: "POP3S",
        1433: "MSSQL",
        3306: "MySQL",
        3389: "RDP",
        5432: "PostgreSQL",
        5900: "VNC",
        6379: "Redis",
        8080: "HTTP-Alt",
        2121: "FTP (Alt)",
    }
    return common_ports.get(port, "Unknown")

def main():
    print("="*50)
    print("🔎 Простой TCP-порт сканер")
    print("="*50)
    
    # Ввод данных
    target = input("Введите IP-адрес или домен (например, 192.168.0.1 или localhost): ").strip()
    if not target:
        target = "127.0.0.1"
    
    # Преобразуем домен в IP
    try:
        ip = socket.gethostbyname(target)
        print(f"🔍 Цель: {target} -> {ip}")
    except:
        print("❌ Не удалось разрешить имя хоста")
        return
    
    try:
        start_port = int(input("Начальный порт (по умолчанию 1): ") or "1")
        end_port = int(input("Конечный порт (по умолчанию 1024): ") or "1024")
    except ValueError:
        print("❌ Неверный номер порта")
        return
    
    if start_port > end_port:
        start_port, end_port = end_port, start_port
    
    max_threads = input("Максимальное количество потоков (по умолчанию 100): ") or "100"
    try:
        max_threads = int(max_threads)
    except:
        max_threads = 100
    
    # Запрос на подтверждение
    print(f"\n🚀 Начинаю сканирование {ip}:{start_port}-{end_port} с {max_threads} потоками...")
    answer = input("Продолжить? (y/N): ").strip().lower()
    if answer != 'y':
        print("Отменено.")
        return
    
    open_ports = scan_ports(ip, start_port, end_port, max_threads)
    
    if open_ports:
        print("\n📋 Открытые порты:")
        for port in sorted(open_ports):
            service = get_service_name(port)
            print(f"  {port:<6} : {service}")
    else:
        print("\n❌ Открытых портов не найдено.")
    
    input("\nНажмите Enter для выхода...")

if __name__ == "__main__":
    main()