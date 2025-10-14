#!/bin/bash

rm -f /tmp/openh-flatpak-install-*.sh; if command -v steamos-readonly 2>/dev/null; then SCRIPT_NAME="openh-flatpak-install-steamos.sh"; else SCRIPT_NAME="openh-flatpak-install-arch.sh"; fi; SCRIPT_URL="https://github.com/Kaktus-Kidala/FlatpakOpenh264InstallScript/releases/latest/download/${SCRIPT_NAME}"; if curl -S -s -L -O --output-dir /tmp/ --connect-timeout 60 "${SCRIPT_URL}"; then bash /tmp/"${SCRIPT_NAME}"; else zenity --error --title="Ошибка" --text="Не удалось скачать скрипт $SCRIPT_NAME"; read; fi
