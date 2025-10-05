#!/bin/bash

# Список программ
# "Выбор по умолчанию" "Название" "Оисание"
programm_list=(
"TRUE" "qBittorrent" "Торрент-клиент"
"TRUE" "PortProton" "Запуск сторонних игр"
"TRUE" "Protontricks" "Редактирование префиксов Steam"
"TRUE" "ProtonUP-Qt" "Установка сторонних версий Wine/Proton для Steam"
"TRUE" "Firefox" "Интернет-браузер"
"FALSE" "Bottles" "Альтератива PortProton"
"FALSE" "Anydesk" "Удалённый доступ"
"FALSE" "Heroic" "Лончер для GOG, EGS..."
"FALSE" "Warpinator" "Передача файлов по локальной сети"
)

# Добавление репозитория, если его нет
flatpak remote-add --if-not-exists flathub https://flathub.org/repo/flathub.flatpakrepo &>/dev/null

# Выбор программ
selected_string=$(zenity --list --checklist \
    --width=800 \
    --height=600 \
    --text="Выберите программы дла установки|обновления" \
    --column="Выбор" \
    --column="Название" \
    --column="Описание" \
    "${programm_list[@]}")

# Завершение скрипта если ничего не выбрано
if [ -z "$selected_string" ]; then
    zenity --error --title="autoinstall.sh" --text="Не выбраны программы для установки!"
    exit 1
fi

# Внесение вывода zenity в массив
IFS='|' read -r -a selected_list <<< "$selected_string"

format_output() {
    # Читаем данные со стандартного ввода (которые приходят от flatpak)
    # и для каждой строки добавляем префикс "# "
    while IFS= read -r line; do
        echo "# $line"
    done
}

# Функция для отображения окна прогресса
zenity_progress () {
    ("$@") | (format_output) | zenity --progress \
    --width=500 \
    --pulsate \
    --auto-close \
    --text="Установка..." \
    --title="Установка $app"
}

flatpak_install () {
    flatpak install flathub --system --or-update --assumeyes "$full_id"
}

for app in "${selected_list[@]}"; do
    # Получение полной ссылки на программу
    full_id=$(flatpak search --system --columns=application "$app" | awk 'NR==1 {print $1}')
     zenity_progress flatpak_install
done

zenity --info \
    --title="Авто-установка" \
    --text="Программы установлены!"
