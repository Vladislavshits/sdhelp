#!/bin/bash

# Скрипт запуска sdhelp
cd /home/deck/sdhelp

# Активация виртуального окружения
source venv/bin/activate

# Запуск основной программы
python app/sdhelp.py
