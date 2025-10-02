#!/bin/bash

# Установщик для sdhelp - утилиты настройки Steam Deck
set -e

# Функция для показа диалогов zenity
show_dialog() {
    zenity --question \
        --title="Установка SD Help" \
        --text="Добро пожаловать в установщик SD Help!\n\nЭта утилита поможет настроить ваш Steam Deck.\n\nПродолжить установку?" \
        --width=400 \
        --ok-label="Установить" \
        --cancel-label="Отмена"
}

# Функция для показа прогресса
show_progress() {
    zenity --progress \
        --title="Установка SD Help" \
        --text="$1" \
        --percentage=0 \
        --auto-close \
        --auto-kill
}

# Функция для показа информации
show_info() {
    zenity --info \
        --title="Установка SD Help" \
        --text="$1" \
        --width=400
}

# Функция для показа ошибки
show_error() {
    zenity --error \
        --title="Ошибка установки" \
        --text="$1" \
        --width=400
}

# Проверка наличия zenity
if ! command -v zenity &> /dev/null; then
    echo "Ошибка: zenity не установлен. Установите zenity для работы установщика."
    exit 1
fi

# Показать начальный диалог
if ! show_dialog; then
    echo "Установка отменена пользователем."
    exit 0
fi

# Переход в домашнюю директорию
cd /home/deck

# Проверка наличия Python
if ! command -v python3 &> /dev/null; then
    show_error "Python3 не найден. Установите Python3 перед продолжением."
    exit 1
fi

# Основной процесс установки в одном прогресс-баре
(
    echo "10"
    echo "# Удаление старой версии..."
    if [ -d "sdhelp" ]; then
        rm -rf sdhelp
    fi

    echo "30"
    echo "# Скачивание проекта..."

    # Скачивание архива с main ветки
    curl -L -o sdhelp-main.zip https://github.com/Vladislavshits/sdhelp/archive/refs/heads/main.zip

    echo "50"
    echo "# Распаковка архива..."
    unzip -q sdhelp-main.zip
    mv sdhelp-main sdhelp
    rm -f sdhelp-main.zip

    echo "70"
    echo "# Настройка окружения..."
    cd sdhelp
    python3 -m venv venv
    source venv/bin/activate
    pip install --upgrade pip --quiet
    pip install pyqt6 --quiet

    echo "90"
    echo "# Создание ярлыков..."

    # Создание утилиты удаления
    cat > uninstall.sh << 'EOFUNINSTALL'
#!/bin/bash
set -e

show_dialog() {
    zenity --question \
        --title="Удаление SD Help" \
        --text="Вы уверены, что хотите удалить SD Help?\n\nВсе данные и настройки будут удалены." \
        --width=400 \
        --ok-label="Удалить" \
        --cancel-label="Отмена"
}

show_progress() {
    zenity --progress \
        --title="Удаление SD Help" \
        --text="$1" \
        --percentage=0 \
        --auto-close \
        --auto-kill
}

show_info() {
    zenity --info \
        --title="Удаление SD Help" \
        --text="$1" \
        --width=400
}

if ! command -v zenity &> /dev/null; then
    echo "Ошибка: zenity не установлен."
    exit 1
fi

if ! show_dialog; then
    echo "Удаление отменено."
    exit 0
fi

(
    echo "25"
    echo "# Удаление файлов программы..."
    rm -rf /home/deck/sdhelp
    echo "50"
    echo "# Удаление ярлыков..."
    rm -f /home/deck/Desktop/SDHelp.desktop
    rm -f /home/deck/Desktop/SDHelpUninstall.desktop
    echo "75"
    echo "# Удаление конфигурации..."
    rm -f /home/deck/.config/sdhelp_config.json
    echo "100"
    echo "# Удаление завершено!"
) | show_progress "Удаление SD Help..."

show_info "SD Help успешно удален!"
EOFUNINSTALL

    # Создание ярлыков на рабочем столе
    cat > /home/deck/Desktop/SDHelp.desktop << EOF
[Desktop Entry]
Version=1.0
Type=Application
Name=SDHelp
Comment=Steam Deck Help Utility
Exec=/home/deck/sdhelp/run_sdhelp.sh
Icon=/home/deck/sdhelp/icon.png
Terminal=false
StartupNotify=true
Categories=Utility;
EOF

    cat > /home/deck/Desktop/SDHelpUninstall.desktop << EOF
[Desktop Entry]
Version=1.0
Type=Application
Name=SDHelp Uninstall
Comment=Uninstall SD Help Utility
Exec=/home/deck/sdhelp/uninstall.sh
Icon=user-trash
Terminal=false
StartupNotify=true
Categories=Utility;
EOF

    echo "100"
    echo "# Установка завершена!"

) | show_progress "Установка SD Help"

# После завершения прогресс-бара даем права и показываем финальное сообщение
if [ $? -eq 0 ]; then
    # Даем права на выполнение ВНЕ прогресс-бара
    cd /home/deck/sdhelp
    chmod +x run_sdhelp.sh uninstall.sh
    chmod +x /home/deck/Desktop/SDHelp.desktop
    chmod +x /home/deck/Desktop/SDHelpUninstall.desktop

    # Проверяем что файлы созданы и имеют права
    if [ -f "uninstall.sh" ] && [ -x "uninstall.sh" ] && \
       [ -f "/home/deck/Desktop/SDHelp.desktop" ] && \
       [ -f "/home/deck/Desktop/SDHelpUninstall.desktop" ]; then

        # Запрос на запуск программы
        if zenity --question \
            --title="Установка завершена" \
            --text="Установка SD Help успешно завершена!\n\n• Ярлык 'SDHelp' создан на рабочем столе\n• Ярлык 'SDHelp Uninstall' для удаления\n• Утилита удаления: /home/deck/sdhelp/uninstall.sh\n\nЗапустить программу сейчас?" \
            --width=500 \
            --ok-label="Запустить" \
            --cancel-label="Закрыть"; then

            echo "Запуск программы..."
            ./run_sdhelp.sh
        else
            show_info "Установка завершена!\n\nДля запуска программы:\n• Ярлык 'SDHelp' на рабочем столе\n• Или файл: /home/deck/sdhelp/run_sdhelp.sh\n\nДля удаления:\n• Ярлык 'SDHelp Uninstall' на рабочем столе\n• Или файл: /home/deck/sdhelp/uninstall.sh"
        fi
    else
        show_error "Ошибка: не все файлы были созданы или нет прав доступа."
        # Показываем какие файлы есть
        echo "Проверка файлов:"
        ls -la /home/deck/sdhelp/
        ls -la /home/deck/Desktop/SDHelp*.desktop
        exit 1
    fi
else
    show_error "Установка была прервана или завершилась с ошибкой."
    exit 1
fi
