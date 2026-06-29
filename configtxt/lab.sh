#!/bin/bash

# Лабораторная работа №6
# Студент: Коптелин Илья Алексеевич, группа ИСб-24-1-з

LOG_FILE="$(basename "$0").log"
> "$LOG_FILE"

log_message() {
    echo "$1"
    echo "$1" >> "$LOG_FILE"
}

log_message "=== Лабораторная работа №6 (Коптелин И.А.) ==="

# Имя результирующего файла – первый параметр или запрос
RESULT_FILE="$1"
if [ -z "$RESULT_FILE" ]; then
    log_message "Введите имя результирующего файла (например, merged.txt):"
    read -r RESULT_FILE
fi
log_message "Результирующий файл: $RESULT_FILE"

# Базовый каталог (фамилия.имя.группа)
BASE_DIR="Koptelin.Ilya.ISb-24-1-z"

# Создаём каталоги по одному (надёжно)
mkdir -p "$BASE_DIR"
mkdir -p "$BASE_DIR/I.A.K.1"
mkdir -p "$BASE_DIR/I.A.K.2"
mkdir -p "$BASE_DIR/I.A.K.3"
log_message "Создана структура: $BASE_DIR/I.A.K.{1,2,3}"

# Создаём файл в первом подкаталоге
echo "Коптелин Илья Алексеевич, группа ИСб-24-1-з" > "$BASE_DIR/I.A.K.1/Ilya.txt"
log_message "Создан файл: $BASE_DIR/I.A.K.1/Ilya.txt"

# Копируем во второй каталог
cp "$BASE_DIR/I.A.K.1/Ilya.txt" "$BASE_DIR/I.A.K.2/"
log_message "Скопировано во второй каталог"

# Переименовываем: Ilya -> aylI
cd "$BASE_DIR/I.A.K.2"
mv Ilya.txt aylI.txt
cd - > /dev/null
log_message "Переименован в aylI.txt"

# Объединяем файлы из первого и второго в третий каталог
cat "$BASE_DIR/I.A.K.1/Ilya.txt" "$BASE_DIR/I.A.K.2/aylI.txt" > "$BASE_DIR/I.A.K.3/$RESULT_FILE"
log_message "Файлы объединены в $BASE_DIR/I.A.K.3/$RESULT_FILE"

# Перемещаем результат в корневой каталог (уровнем выше)
mv "$BASE_DIR/I.A.K.3/$RESULT_FILE" "$BASE_DIR/"
log_message "Файл перемещён в $BASE_DIR/"

# Выводим содержимое результирующего файла
log_message "Содержимое результирующего файла:"
cat "$BASE_DIR/$RESULT_FILE" >> "$LOG_FILE"
cat "$BASE_DIR/$RESULT_FILE"

# Удаляем все созданные подкаталоги и файлы (по заданию)
rm -rf "$BASE_DIR/I.A.K.1" "$BASE_DIR/I.A.K.2" "$BASE_DIR/I.A.K.3"
rm -f "$BASE_DIR/$RESULT_FILE"
rmdir "$BASE_DIR" 2>/dev/null
log_message "Все временные каталоги и файлы удалены."

log_message "=== Скрипт завершён ==="