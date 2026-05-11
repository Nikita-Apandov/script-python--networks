from flask import Flask, request, send_file
import os
import time
import socket
from waitress import serve

app = Flask(__name__)

# Конфигурация
PING_COUNT = 10
PARALLEL = 4                     # количество параллельных потоков для download/upload
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Размеры файлов: пробный 1 МБ, основные 10, 25, 50, 100МБ
FILE_SIZES = [1, 10, 25, 50]  # МБ
FILES = {}
for size in FILE_SIZES:
    FILES[size] = os.path.join(BASE_DIR, f'test_{size}MB.bin')

# ------------------- Генерация всех файлов -------------------
def generate_all_files():
    for size, path in FILES.items():
        if os.path.exists(path) and os.path.getsize(path) == size * 1024 * 1024:
            #print(f"Файл {size} МБ уже существует.")
            continue
        print(f"Генерация файла {size} МБ...")
        with open(path, 'wb') as f:
            chunk = os.urandom(1024 * 1024)
            for _ in range(size):
                f.write(chunk)
        print(f"Файл {size} МБ готов.")

# ------------------- Эндпоинты -------------------
@app.route('/')
def index():
    return f'''
<!DOCTYPE html>
<html>
<head>
    <title>Speedtest</title>
    <style>
        body {{ font-family: Arial, sans-serif; text-align: center; margin-top: 50px; }}
        button {{ padding: 12px 24px; font-size: 18px; cursor: pointer; }}
        .result {{ margin-top: 20px; font-size: 20px; }}
        .info {{ color: gray; margin-top: 20px; }}
        table {{ margin: 0 auto; text-align: left; }}
        td {{ padding: 5px 10px; }}
    </style>
</head>
<body>
    <h1>Тест скорости сети</h1>
    <button id="startBtn">Запустить тест</button>
    <div id="results" class="result"></div>
    <div id="progress" class="info"></div>

    <script>
        const PING_COUNT = {PING_COUNT};
        const PARALLEL = {PARALLEL};
        const FILE_SIZES = {FILE_SIZES};

        let log = (msg) => {{
            document.getElementById('progress').innerHTML = msg;
        }};

        // ---------- Ping ----------
        let measurePing = async () => {{
            let times = [];
            for (let i = 0; i < PING_COUNT; i++) {{
                let start = performance.now();
                await fetch('/ping?t=' + Date.now() + Math.random());
                let end = performance.now();
                times.push(end - start);
            }}
            return Math.min(...times);
        }};

        // ---------- Пробный download (1 МБ, один поток) ----------
        let probeDownload = async () => {{
            const url = `/download/1?nocache=${{Math.random()}}`;
            const start = performance.now();
            await fetch(url);
            const duration = (performance.now() - start) / 1000;
            const bytes = 1 * 1024 * 1024;
            let speedMbps = (bytes * 8) / (duration * 1e6);
            return Math.max(speedMbps, 0.5);
        }};

        // ---------- Основной download (многопоточный, выбранный файл) ----------
        let downloadFile = async (fileSizeMB) => {{
            const fileSizeBytes = fileSizeMB * 1024 * 1024;
            let totalBytes = 0;
            let startTime = performance.now();
            let promises = [];

            for (let i = 0; i < PARALLEL; i++) {{
                let promise = fetch(`/download/${{fileSizeMB}}?part=${{i}}&nocache=${{Math.random()}}`)
                    .then(response => response.arrayBuffer())
                    .then(buffer => {{
                        totalBytes += buffer.byteLength;
                    }});
                promises.push(promise);
            }}
            await Promise.all(promises);
            let durationSec = (performance.now() - startTime) / 1000;
            let speedMbps = (totalBytes * 8) / (durationSec * 1e6);
            return speedMbps;
        }};

        // ---------- Пробный upload (1 МБ) ----------
        let probeUpload = async () => {{
            // Генерируем 1 МБ случайных данных
            let data = new Uint8Array(1 * 1024 * 1024);
            for (let i = 0; i < data.length; i++) {{
                data[i] = Math.floor(Math.random() * 256);
            }}
            const start = performance.now();
            await fetch('/upload', {{ method: 'POST', body: data }});
            const duration = (performance.now() - start) / 1000;
            const bytes = 1 * 1024 * 1024;
            let speedMbps = (bytes * 8) / (duration * 1e6);
            return Math.max(speedMbps, 0.5);
        }};

        // ---------- Основной upload (многопоточный, выбранный размер данных) ----------
        let uploadData = async (dataSizeMB) => {{
            const chunkSizeBytes = dataSizeMB * 1024 * 1024;
            // Генерируем данные один раз (для всех потоков)
            let testData = new Uint8Array(chunkSizeBytes);
            for (let i = 0; i < chunkSizeBytes; i++) {{
                testData[i] = Math.floor(Math.random() * 256);
            }}
            let startTime = performance.now();
            let totalBytes = 0;
            let promises = [];

            for (let i = 0; i < PARALLEL; i++) {{
                let promise = fetch('/upload', {{
                    method: 'POST',
                    body: testData,
                    headers: {{ 'Content-Type': 'application/octet-stream' }}
                }}).then(() => {{
                    totalBytes += chunkSizeBytes;
                }});
                promises.push(promise);
            }}
            await Promise.all(promises);
            let durationSec = (performance.now() - startTime) / 1000;
            let speedMbps = (totalBytes * 8) / (durationSec * 1e6);
            return speedMbps;
        }};

        // ---------- Выбор размера файла на основе оценочной скорости ----------
        function selectFileSize(estimatedMbps) {{
            // Целевая длительность теста ~10 секунд
            // Для скорости X Мбит/с за 10 секунд передастся X*10/8 МБ.
            let targetMB = (estimatedMbps * 10) / 8;
            // Ищем ближайший предустановленный размер
            let best = FILE_SIZES[0];
            for (let sz of FILE_SIZES) {{
                if (Math.abs(sz - targetMB) < Math.abs(best - targetMB)) best = sz;
            }}
            return best;
        }}

        // ---------- Главный тест ----------
        document.getElementById('startBtn').onclick = async () => {{
            let btn = document.getElementById('startBtn');
            btn.disabled = true;
            let resultsDiv = document.getElementById('results');
            resultsDiv.innerHTML = 'Тест запущен...';
            await fetch('/start_test', {{ method: 'POST' }});
            try {{
                log('Измерение ping...');
                let ping = await measurePing();

                log('Пробный замер download...');
                let estDownload = await probeDownload();
                log(`Оценочная скорость download: ${{estDownload.toFixed(1)}} Мбит/с`);

                let dlSize = selectFileSize(estDownload);
                log(`Download...`);
                let download = await downloadFile(dlSize);

                log('Пробный замер upload...');
                let estUpload = await probeUpload();
                log(`Оценочная скорость upload: ${{estUpload.toFixed(1)}} Мбит/с`);

                let ulSize = selectFileSize(estUpload);
                log(`Upload...`);
                let upload = await uploadData(ulSize);

                resultsDiv.innerHTML = `
                    <h3>Текущую доступную пропускную способность между сервером и клиентом.</h3>
                    <table>
                        <tr><td>📡 Ping</td><td><b>${{ping.toFixed(2)}} мс</b></td><td style="color:gray;">(задержка)</td></tr>
                        <tr><td>⬇️ Download</td><td><b>${{download.toFixed(2)}} Мбит/с</b></td><td style="color:gray;">(скорость скачивания)</td></tr>
                        <tr><td>⬆️ Upload</td><td><b>${{upload.toFixed(2)}} Мбит/с</b></td><td style="color:gray;">(скорость отправки)</td></tr>
                    </table>
                    <hr>
                    <p style="font-size:12px; color:gray;">
                        ⬇️ Download — скорость, с которой ваш компьютер получает данные (например, загрузка файлов, видео).<br>
                        ⬆️ Upload — скорость, с которой ваш компьютер отправляет данные (например, публикация фото, видеозвонки).
                    </p>
                `;
                log('Тест завершён.');

                await fetch('/submit_result', {{
                    method: 'POST',
                    headers: {{ 'Content-Type': 'application/json' }},
                    body: JSON.stringify({{ ping, download, upload }})
                }});
            }} catch (err) {{
                resultsDiv.innerHTML = `<p style="color:red">Ошибка: ${{err.message}}</p>`;
                log('');
            }} finally {{
                btn.disabled = false;
            }}
        }};
    </script>
</body>
</html>
    '''

@app.route('/download/<int:size_mb>')
def download_file(size_mb):
    if size_mb not in FILES:
        return 'Unsupported size', 400
    return send_file(FILES[size_mb], as_attachment=False, mimetype='application/octet-stream')

@app.route('/ping')
def ping():
    return '', 204

@app.route('/upload', methods=['POST'])
def upload():
    request.get_data()
    return '', 204

@app.route('/submit_result', methods=['POST'])
def submit_result():
    data = request.get_json()
    client_ip = request.remote_addr
    print(f"\n📊 Результаты теста от {client_ip}:")
    print(f"   Ping: {data.get('ping')} мс")
    print(f"   Download: {data.get('download')} Мбит/с")
    print(f"   Upload: {data.get('upload')} Мбит/с")
    return '', 204

@app.route('/start_test', methods=['POST'])
def start_test():
    print(f"\n🚀 Тест запущен с устройства: {request.remote_addr}")
    return '', 204

# ------------------- Меню и запуск -------------------
def main():
    while True:
        print("-----------МЕНЮ-----------")
        print("1. Запуск сервера")
        print("2. Смена IP сервера")
        print("3. Выход")
        numbe = input("Введите число от 1 до 3: ")
        if numbe == "3":
            time.sleep(0.3)
            os.system("cls")
            break
        elif numbe == "1":
            time.sleep(0.3)
            os.system("cls")
            generate_all_files()
            local_ip = "192.168.0.103"
            print(f"\n Сервер запущен. Откройте в браузере: http://{local_ip}:5000")
            print("\n ⬇️   Download — скорость, с которой пользователь получает данные от нашего сервера.")
            print("\n ⬆️   Upload — скорость, с которой пользователь отправляет данные на наш сервер.")
            print("\n Для выключения и выхода в главное меню нажмите Ctrl+C")
            try:
                serve(app, host=local_ip, port=5000, threads=32)
            except KeyboardInterrupt:
                print("\nСервер остановлен.")
            time.sleep(0.3)
            os.system("cls")
        elif numbe == "2":
            time.sleep(0.3)
            os.system("cls")
            print("IP можно сменить при следующем запуске через пункт 1.")
            time.sleep(1)
            os.system("cls")
        else:
            print("Введите число от 1 до 3")
            time.sleep(1)
            os.system("cls")

if __name__ == '__main__':
    main()