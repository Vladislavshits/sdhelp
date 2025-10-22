#!/bin/bash

source "$HOME/.local/share/sdhelp/app/core/ScriptFunctions"

if ! flatpak remotes | grep "launcher.moe" &>/dev/null
then
    if zen_q "Аниме лаунчеры" "Установить flatpak репозиторий лаунчеров?"
    then pkexec flatpak remote-add --if-not-exists launcher.moe https://gol.launcher.moe/gol.launcher.moe.flatpakrepo
    else err_trap "Без репозитория нельзя установить лаунчеры!"
    fi
fi

launchers_list=(
"Общий лаунчер (test)" "moe.launcher.anime-games-launcher"
"PGR (неподдерживается)" "moe.celica.BabyloniaTerminal"
"Genshin Impact" "moe.launcher.an-anime-game-launcher"
"Honkai Impact 3rd" "moe.launcher.honkers-launcher"
"Zenless Zone Zero" "moe.launcher.sleepy-launcher"
"Honkai: Star Rail" "moe.launcher.the-honkers-railway-launcher")

if ! launcher=$(zen_ns --list \
    --title="Установки аниме лаунчера" \
    --text="Выберите лаунчер для нужной игры" \
    --column="Игра" \
    --column="Полное название лаунчера" \
    --width=600 \
    --height=400 \
    --print-column=2 \
    "${launchers_list[@]}")
then exit 0
fi

anime_launcher_install () {
    flatpak install --assumeyes $launcher
}

if zen_progress anime_launcher_install "Установка аниме лаунчера"
then zen_info "Установка аниме лаунчера" "$launcher установлен!"
else zen_err "Установка не удалась!"
fi
xdg-user-dirs-update
