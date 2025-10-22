#!/bin/bash

source "$HOME/.local/share/sdhelp/app/core/ZenityFunctions"

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
if ! selected_string=$(zen_ns --list --checklist \
    --width=800 \
    --height=600 \
    --text="Выберите программы дла установки|обновления" \
    --column="Выбор" \
    --column="Название" \
    --column="Описание" \
    "${programm_list[@]}")
then exit 0
fi

# Завершение скрипта если ничего не выбрано
if [ -z "$selected_string" ]; then
    zen_err "autoinstall.sh" "Не выбраны программы для установки!"
    exit 1
fi

# Внесение вывода zenity в массив
IFS='|' read -r -a selected_list <<< "$selected_string"

# Функция для отображения окна прогресса
zenity_progress_flatpak () {
    ("$@" | format_output) | zen_ns --progress \
    --width=500 \
    --pulsate \
    --auto-close \
    --text="Установка..." \
    --title="Установка $app"
}

flatpak_install () {
    flatpak install flathub --or-update --assumeyes "$full_id"
}

for app in "${selected_list[@]}"; do
    # Получение полной ссылки на программу
    full_id=$(flatpak search --system --columns=application "$app" | awk 'NR==1 {print $1}')
    zenity_progress_flatpak flatpak_install
done
xdg-user-dirs-update
zen_info "Авто-установка" "Программы установлены!"
