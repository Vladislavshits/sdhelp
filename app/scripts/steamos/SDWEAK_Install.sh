#!/bin/bash

# Установка SDWEAK
# https://github.com/Taskerer/SDWEAK

# Удаление старого скрипта, если таковой имеется
rm -rf /tmp/desktop-install.sh || true

# Команда скачивания и запуска установщика из https://github.com/Taskerer/SDWEAK/blob/main/SDWEAK-installer.desktop
wget -O /tmp/desktop-install.sh https://raw.githubusercontent.com/Taskerer/SDWEAK/main/desktop-install.sh && bash /tmp/desktop-install.sh
