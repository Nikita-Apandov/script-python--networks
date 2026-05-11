import os
from pyftpdlib.authorizers import DummyAuthorizer
from pyftpdlib.handlers import FTPHandler
from pyftpdlib.servers import ThreadedFTPServer
import time
# Настройки
HOST = '0.0.0.0'        # слушаем все интерфейсы
PORT = 2121
USER = 'user'
PASSWORD = '123'
HOME_DIR =  'D:\Git_programming\script-python--networks' # папка, к которой даём доступ

# Создаём менеджер пользователей
authorizer = DummyAuthorizer()

# Добавляем пользователя с полными правами
authorizer.add_user(USER, PASSWORD, HOME_DIR, perm='elradfmwMT')

# Добавляем анонимный доступ (чтобы клиенты, которые подключаются без логина/пароля, не отваливались)
#authorizer.add_anonymous(HOME_DIR)

# Настраиваем обработчик
class MyHandler(FTPHandler):
    print('sdfdsfdfs')
    def on_connect(self):
        pass
        #print(f"✅ Подключился клиент: {self.remote_ip}:{self.remote_port}")


MyHandler.authorizer = authorizer

# Запускаем сервер
server = ThreadedFTPServer((HOST, PORT), MyHandler)

print(f"🚀 FTP-сервер запущен на порту {PORT}")
print(f"🔐 Логин: {USER}, Пароль: {PASSWORD} (если требуется)")
#print("🔓 Также доступен анонимный вход (без логина/пароля)")
print(f"📁 Директория для доступа: ftp://{HOST}:{PORT}")
print("Ожидание подключений... (нажмите Ctrl+C для остановки)\n")

# Обработка остановки

server.serve_forever()
