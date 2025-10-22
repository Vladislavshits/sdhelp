#!/bin/bash

source "$HOME/.local/share/sdhelp/app/core/ScriptFunctions"
source "$HOME/.local/share/sdhelp/app/core/ZenityFunctions"

# Запуск от прав root
if [[ "$EUID" -ne 0 ]]; then
  sudo_p "$0" "$@"
  exit 0
fi

edit_error () {
  zen_err "Редактирование /etc/locale.gen" \
  "Не удалось отредактировать конфиг\nИзменения не были внесены"
  steamos-readonly enable
  exit 1
}

# Разрешение записи в систему
steamos-readonly disable || true

# Проверка и редактирования конфига локалей
if grep -q "#ru_RU.UTF-8 UTF-8" /etc/locale.gen
then
  sed -i "s/#ru_RU.UTF-8 UTF-8/ru_RU.UTF-8 UTF-8/g" /etc/locale.gen &>/dev/null
fi

if grep -q "#en_US.UTF-8 UTF-8" /etc/locale.gen
then
  sed -i "s/#en_US.UTF-8 UTF-8/en_US.UTF-8 UTF-8/g" /etc/locale.gen &>/dev/null
fi

# Проверка конфига
if ! grep -q "^ru_RU.UTF-8 UTF-8" /etc/locale.gen
then
  edit_error
  else
  if ! grep -q "^en_US.UTF-8 UTF-8" /etc/locale.gen
  then
    edit_error
  fi
fi

# Генерация локалей
locale-gen

# Возвращение запрета на запись в систему
steamos-readonly enable

zen_info "Генерация локалей выполнена" \
  "Сгенерированы локали en_US и ru_RU\nДля применения изменений требуется перезагрузить устройство"

exit 0
