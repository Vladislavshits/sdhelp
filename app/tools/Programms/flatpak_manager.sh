#!/bin/bash

export app

# Добавление репозитория, если его нет
flatpak remote-add --if-not-exists flathub https://flathub.org/repo/flathub.flatpakrepo &>/dev/null

# Форматирование всего вывода для zen_progress
format_output() {
    while IFS= read -r line; do
        echo "# $line"
    done
}

# Окно ошибки и выход
zen_err () {
    zenity --error \
        --title="$1" \
        --text="$2"
    zenity --info \
        --title="flatpak manager" \
        --text="Завершение скрипта"
    exit 0
}

# Функция для отображения окна прогресса
zen_progress () {
    ("$1") | (format_output) | zenity --progress \
    --width=500 \
    --pulsate \
    --auto-close \
    --text="$2" \
    --title="$3"
}

# Функция для вычисления полного названия программы
flatpak_id () {
    full_id=$(flatpak search --system --columns=application "$@" | awk 'NR==1 {print $1}')
}

flatpak_update () {
    zen_progress "flatpak update --assumeyes"
    zenity --info
}

# Вынесение команды в функцию для вызова zen_progress
flatpak_install_c () {
    flatpak install flathub --system --or-update --assumeyes "$full_id"
}

flatpak_install () {
    app=$(zenity --entry \
        --title="Установка программы" \
        --text="Введите название программы")

    if [ -z "$app" ]; then
        zen_err "Установка программы" "Не введено название"
    fi

    flatpak_id "$app"

    zen_progress flatpak_install_c "Установка $full_id" "Установка $app"

    zenity --question \
        --title="Установка $app" \
        --text="Программа $full_id установлена!\nНаверное..." \
        --ok-label="Запустить" \
        --cancel-label="Отмена"
    if [ "$?" -eq 0 ]; then
        ($full_id)
        exit 0
    fi
}

flatpak_remove_c () {
    flatpak uninstall --assumeyes "$full_id"
}

flatpak_remove () {
    # Обнуляем переменную во избежание дубликатов
    unset flatpak_installed_raw

    # Создаём массив с форматированием под zenity --list
    flatpak_installed_raw=$(flatpak list --columns=name | grep -v "Mesa*" | tail -n +1)

    while IFS= read -r line; do
        # Удаляем возможные ведущие/завершающие пробелы, которые могут сбить Zenity
        trimmed_line=$(echo "$line" | xargs)

        # Добавляем в массив только непустые строки
        if [[ -n "$trimmed_line" ]]; then
            flatpak_installed+=("$trimmed_line")
        fi
    done <<< "$flatpak_installed_raw"

    selected_delete=$(zenity --list \
    --title="Удаление программы" \
    --text="Выберите программу для удаления" \
    --column="Название программы" \
    "${flatpak_installed[@]}")

    # Проверка на выбор программы
    if [ -z "$selected_delete" ]; then
        zen_err "Удаление программы" "Программа для удаления не выбрана"
    fi

    flatpak_id "$selected_delete"

    zen_progress flatpak_remove_c "Удаление $full_id" "Удаление $selected_delete"

    sleep 4

    delete_confirm=$(flatpak list --columns=name | grep "$full_id")

    # Проверка на удаление программы
    if [ -z "$delete_confirm" ]; then
        zenity --info \
            --title="Удаление $selected_delete" \
            --text="Удаление завершено\nЯрлык может ещё присутствовать (это враки до ребута)"
    else
        zenity --error \
            --title="Удаление $selected_delete" \
            --text="Не удалось удалить программу!\nУбедитесь что она закрыта и не работает в фоне"
    fi
}

while true; do
    menu=$(zenity --list \
        --title="flatpak manager" \
        --text="Простой и топорный аналог Discover" \
        --column="Действие" \
        --cancel-label="Выход" \
        "Обновить всё" \
        "Установить программу" \
        "Удалить программу")
    case "$menu" in
        "Обновить всё") flatpak_update ;;
        "Установить программу") flatpak_install ;;
        "Удалить программу") flatpak_remove ;;
        *) break;;
    esac
done
