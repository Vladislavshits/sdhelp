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

# Удаление старой версии если существует
if [ -d "sdhelp" ]; then
    (
        echo "10"
        echo "# Удаление старой версии..."
        rm -rf sdhelp
        echo "20"
    ) | show_progress "Удаление старой версии..."
fi

# Скачивание архива проекта
(
    echo "30"
    echo "# Скачивание проекта..."

    # Скачивание архива с main ветки
    if curl -L -o sdhelp-main.zip https://github.com/Vladislavshits/sdhelp/archive/refs/heads/main.zip; then
        echo "60"
        echo "# Проверка архива..."

        # Проверка что архив скачался
        if [ ! -f "sdhelp-main.zip" ]; then
            show_error "Ошибка: не удалось скачать архив"
            exit 1
        fi

        echo "70"
        echo "# Распаковка архива..."

        # Распаковка архива
        if unzip -q sdhelp-main.zip; then
            echo "80"
            echo "# Установка файлов..."

            # Переименование папки и перемещение файлов
            mv sdhelp-main sdhelp

            echo "90"
            echo "# Очистка..."

            # Удаление архива
            rm -f sdhelp-main.zip

            echo "100"
            echo "# Установка завершена!"
        else
            show_error "Ошибка при распаковке архива"
            exit 1
        fi
    else
        show_error "Ошибка при скачивании архива"
        exit 1
    fi
) | show_progress "Установка SD Help..."

# Переход в директорию проекта
cd sdhelp

# Создание виртуального окружения
(
    echo "25"
    echo "# Создание виртуального окружения..."
    python3 -m venv venv

    echo "50"
    echo "# Активация окружения..."
    source venv/bin/activate

    echo "75"
    echo "# Установка зависимостей..."
    pip install --upgrade pip
    pip install pyqt6

    echo "100"
    echo "# Завершение установки..."
) | show_progress "Настройка окружения..."

# Сделать скрипты исполняемыми
chmod +x run_sdhelp.sh
chmod +x uninstall.sh

# Создание ярлыка на рабочем столе
(
    echo "# Создание ярлыка..."
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

    chmod +x /home/deck/Desktop/SDHelp.desktop
) | show_progress "Создание ярлыка..."

show_info "Установка завершена!\n\nЯрлык 'SDHelp' создан на рабочем столе.\n\nДля удаления программы запустите: ./uninstall.sh\nИли ярлык 'SDHelp Uninstall' на рабочем столе."

# Автозапуск программы
if zenity --question \
    --title="Запуск SD Help" \
    --text="Запустить программу сейчас?" \
    --width=400 \
    --ok-label="Запустить" \
    --cancel-label="Выйти"; then

    echo "Запуск программы..."
    ./run_sdhelp.sh
fi
