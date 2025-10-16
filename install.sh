#!/bin/bash

# Установщик для sdhelp - утилиты настройки Steam Deck
set -e

# Убираем спам Gtk
zen_ns () {
    zenity 2> >(grep -v 'Gtk')>&2 "$@"
}

# Функция для показа диалогов zenity
show_dialog() {
    zen_ns --question \
        --title="Установка SD Help" \
        --text="$1" \
        --width=400 \
        --ok-label="Установить" \
        --cancel-label="Отмена"
}

# Функция для показа прогресса
show_progress() {
    zen_ns --progress \
        --title="Установка SD Help" \
        --text="$1" \
        --percentage=0 \
        --auto-close \
        --auto-kill
}

# Функция для показа информации
show_info() {
    zen_ns --info \
        --title="Установка SD Help" \
        --text="$1" \
        --width=400
}

# Функция для показа ошибки
show_error() {
    zen_ns --error \
        --title="Ошибка установки" \
        --text="$1" \
        --width=400
}

# Предупреждение, если запуск не на SteamOS
if ! command -v steamos-readonly; then
    if ! show_dialog "Похоже скрипт запускается не на SteamOS!\nУверены, что хотите продолжить?"; then
        echo "Установка отменена пользователем."
        exit 0
    fi
fi

# Показать начальный диалог
if ! show_dialog "Добро пожаловать в установщик SD Help!\n\nЭта утилита поможет настроить ваш Steam Deck.\n\nПродолжить установку?"; then
    echo "Установка отменена пользователем."
    exit 0
fi

# Переход в ~/.local/share
cd "$HOME/.local/share"

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

zen_ns () {
    zenity 2> >(grep -v 'Gtk')>&2 "$@"
}

show_dialog() {
    zen_ns --question \
        --title="Удаление SD Help" \
        --text="Вы уверены, что хотите удалить SD Help?\n\nВсе данные и настройки будут удалены." \
        --width=400 \
        --ok-label="Удалить" \
        --cancel-label="Отмена"
}

show_progress() {
    zen_ns --progress \
        --title="Удаление SD Help" \
        --text="$1" \
        --percentage=0 \
        --auto-close \
        --auto-kill
}

show_info() {
    zen_ns --info \
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
    rm -rf "$HOME"/.local/share/sdhelp
    echo "50"
    echo "# Удаление ярлыков..."
    rm -f "$HOME"/Desktop/SDHelp.desktop
    rm -f "$HOME"/Desktop/SDHelpUninstall.desktop
    echo "75"
    echo "# Удаление конфигурации..."
    rm -f "$HOME"/.config/sdhelp_config.json
    echo "100"
    echo "# Удаление завершено!"
) | show_progress "Удаление SD Help..."

show_info "SD Help успешно удален!"
EOFUNINSTALL

    # Создание ярлыков на рабочем столе
    cat > "$HOME"/Desktop/SDHelp.desktop << EOF
[Desktop Entry]
Version=1.0
Type=Application
Name=SDHelp
Comment=Steam Deck Help Utility
Exec="$HOME"/.local/share/sdhelp/run_sdhelp.sh
Icon="$HOME"/.local/share/sdhelp/icon.png
Terminal=false
StartupNotify=true
Categories=Utility;
EOF

    cat > "$HOME"/Desktop/SDHelpUninstall.desktop << EOF
[Desktop Entry]
Version=1.0
Type=Application
Name=SDHelp Uninstall
Comment=Uninstall SD Help Utility
Exec="$HOME"/.local/share/sdhelp/uninstall.sh
Icon=user-trash
Terminal=false
StartupNotify=true
Categories=Utility;
EOF

    echo "100"
    echo "# Установка завершена!"

) | show_progress "Установка SD Help"

# Проверяем успешность установки
if [ $? -ne 0 ]; then
    show_error "Установка была прервана или завершилась с ошибкой."
    exit 1
fi

# Даем права на выполнение
cd "$HOME"/.local/share/sdhelp
chmod +x run_sdhelp.sh uninstall.sh
chmod +x "$HOME"/Desktop/SDHelp.desktop
chmod +x "$HOME"/Desktop/SDHelpUninstall.desktop

# Проверяем что файлы созданы
if [ ! -f "uninstall.sh" ] || [ ! -f "$HOME/Desktop/SDHelp.desktop" ] || [ ! -f "$HOME/Desktop/SDHelpUninstall.desktop" ]; then
    show_error "Ошибка: не все файлы были созданы."
    exit 1
fi

# Этот диалог ждет нажатия OK
show_info "Установка SD Help успешно завершена!\n\n• Ярлык 'SDHelp' создан на рабочем столе\n• Ярлык 'SDHelp Uninstall' для удаления\n• Утилита удаления: $HOME/.local/share/sdhelp/uninstall.sh\n\nНажмите OK для запуска программы сейчас."

echo "Запуск программы..."
"$HOME"/.local/share/sdhelp/run_sdhelp.sh & # Установщик завершается сразу после запуска фонового процесса.
