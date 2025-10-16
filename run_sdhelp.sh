#!/bin/bash

# Скрипт запуска sdhelp с логированием
cd "$HOME/.local/share/sdhelp"

# Диалоговое окно
zen_q () {
    zenity 2> >(grep -v 'Gtk') >&2 --question \
        --title="Отсутствует окружение!" \
        --text="Выолнить переустановку программы для установки окружения?" \
        --ok-label="Переустановить" \
        --cancel-label="Отмена" \
        --width=400
}

# Проверка существования директории
if [ ! -d "venv" ]; then
    echo "Отсутствует окружение venv!\nЗапрос на переустановку..."
    if zen_q; then
        echo "Запуск установщика и выход"
        exec "$HOME/.local/share/sdhelp/install.sh"
    else
        echo "Отсутствует окружение venv!\nПользователь отказался от переустановки."
        exit 1
    fi
fi

# Создание папки для логов если не существует
mkdir -p logs

# Создание файла лога с временной меткой
LOG_FILE="logs/sdhelp_$(date +%Y%m%d_%H%M%S).log"

echo "=== Запуск SD Help $(date) ===" >> "$LOG_FILE"

# Активация виртуального окружения
echo "Активация виртуального окружения..." >> "$LOG_FILE"
source venv/bin/activate

# Запуск основной программы из папки app с логированием
echo "Запуск основной программы..." >> "$LOG_FILE"
cd app

# Запуск с перенаправлением вывода в лог и на консоль
python sdhelp.py 2>&1 | tee -a "../$LOG_FILE"

# Запись времени завершения
echo "=== Завершение SD Help $(date) ===" >> "../$LOG_FILE"
