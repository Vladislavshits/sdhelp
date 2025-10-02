import json
import os
from typing import Dict, Any


class Config:
    def __init__(self):
        self.config_path = os.path.join(os.path.dirname(__file__), 'config.json')
        self.default_config = {
            "version": "0.1",
            "paths": {
                "home": "/home/deck",
                "sdhelp_dir": "/home/deck/sdhelp",
                "scripts_dir": "/home/deck/sdhelp/scripts"
            },
            "programs": {
                "zapret": {
                    "installed": False,
                    "version": "",
                    "path": ""
                },
                "decky_loader": {
                    "installed": False,
                    "version": "",
                    "path": ""
                }
            },
            "games": {
                "the_crew": {
                    "fixed": False,
                    "last_fix_date": ""
                },
                "forza_horizon": {
                    "fixed": False,
                    "last_fix_date": ""
                },
                "hogwarts_legacy": {
                    "fixed": False,
                    "last_fix_date": ""
                }
            },
            "steamos": {
                "optimized": False,
                "backup_created": False
            },
            "network": {
                "wifi_optimized": False,
                "dns_configured": False
            }
        }
        self.config = self.load_config()

    def load_config(self) -> Dict[str, Any]:
        """Загрузка конфигурации из файла"""
        try:
            if os.path.exists(self.config_path):
                with open(self.config_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            else:
                return self.default_config.copy()
        except Exception as e:
            print(f"Ошибка загрузки конфига: {e}")
            return self.default_config.copy()

    def save_config(self):
        """Сохранение конфигурации в файл"""
        try:
            with open(self.config_path, 'w', encoding='utf-8') as f:
                json.dump(self.config, f, indent=4, ensure_ascii=False)
        except Exception as e:
            print(f"Ошибка сохранения конфига: {e}")

    def get(self, key: str, default=None):
        """Получение значения по ключу"""
        keys = key.split('.')
        value = self.config
        for k in keys:
            if isinstance(value, dict) and k in value:
                value = value[k]
            else:
                return default
        return value

    def set(self, key: str, value: Any):
        """Установка значения по ключу"""
        keys = key.split('.')
        config_ref = self.config

        for k in keys[:-1]:
            if k not in config_ref:
                config_ref[k] = {}
            config_ref = config_ref[k]

        config_ref[keys[-1]] = value
        self.save_config()

    def is_program_installed(self, program_name: str) -> bool:
        """Проверка установлена ли программа"""
        return self.get(f"programs.{program_name}.installed", False)

    def set_program_installed(self, program_name: str, installed: bool, version: str = ""):
        """Установка статуса программы"""
        self.set(f"programs.{program_name}.installed", installed)
        if version:
            self.set(f"programs.{program_name}.version", version)

    def is_game_fixed(self, game_name: str) -> bool:
        """Проверка применено ли исправление для игры"""
        return self.get(f"games.{game_name}.fixed", False)

    def set_game_fixed(self, game_name: str, fixed: bool):
        """Установка статуса исправления игры"""
        self.set(f"games.{game_name}.fixed", fixed)


# Глобальный экземпляр конфигурации
config = Config()
