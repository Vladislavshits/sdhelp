#!/bin/bash
# Скрипт установки Zapret DPI Manager https://github.com/mashakulina/Zapret-DPI-for-Steam-Deck
# Copyright (c) 2025 mashakulina (Скрипт установки)
# Copyright (c) 2025 Kaktus-Kidala (Адаптация под zenity)

# Убираем спам Gtk
zen_ns () {
    zenity 2> >(grep -v 'Gtk') >&2 "$@"
}

# Окно при ошибках
err_trap () {
    zen_ns --error \
        --title="Ошибка установки" \
        --text="Попробуйте запустить установку повторно"
}
trap 'err_trap' ERR
set -e

# Приветсвтенное окно
zen_ns --question \
    --title="Установка Zapret DPI Manager" \
    --text="Установить Zapret DPI Manager?\nКаталог установки: $HOME/zapret" \
    --ok-label="Установить" \
    --cancel-label="Отмена" || exit 0

# Проверка каталога установки
if [ -d "$HOME/zapret" ]; then
    zen_ns --question \
        --title="Переустановка Zapret" \
        --text="Обнаружен установленный каталог!\nПереустановить?" \
        --ok-label="Переустановить" \
        --cancel-label="Отмена" || exit 0
    rm -rf "$HOME/zapret"
fi

PASS=$(zen_ns --entry \
            --hide-text \
            --title="Установка Zapret DPI Manager" \
            --text="Требуется пароль sudo")

# Проверка введённого пароля
if ! ( echo "$PASS" | sudo --stdin -k true ); then
    zen_ns --error --title="Установка Zapret Manager" --text="Неправильный пароль!\nПерезапустите скрипт."
    exit 1
fi

# Создание каталога программы
mkdir -p "$HOME/zapret"
cd "$HOME/zapret"

# Скачивание и распаковка
wget https://github.com/mashakulina/Zapret-DPI-for-Steam-Deck/releases/latest/download/zapret_dpi_manager.zip
unzip zapret_dpi_manager.zip
rm zapret_dpi_manager.zip

# Добавление прав на запуск от sudo
echo "$PASS" | sudo --stdin chmod +x zapret.py

# Добавление ярлыка
echo "[Desktop Entry]
Type=Application
Name=Zapret DPI Manager
Exec=/usr/bin/python3 /home/deck/zapret/zapret.py
Icon=/home/deck/zapret/zapret.png
Terminal=false
Categories=Utility;" > ~/Desktop/Zapret-DPI.desktop

# Добавление прав на запуск ярлыку
chmod +x ~/Desktop/Zapret-DPI.desktop

zen_ns --info \
    --title="Установка Zapret DPI Manager" \
    --text="Установка завершена!\nМожете запустить Zapret с помощью ярлыка на рабочем столе."
