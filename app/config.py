import json
import os
from typing import Any, Dict

class Config:
    def __init__(self):
        self.config_path = os.path.join(os.path.dirname(__file__), "config.json")
        self.data = self.load_config()
    
    def load_config(self) -> Dict[str, Any]:
        """Загрузка конфигурации"""
        default_config = {
            "version": "0.1.0",
            "functions": {},
            "games": {},
            "programs": {}
        }
        
        try:
            if os.path.exists(self.config_path):
                with open(self.config_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
        except Exception:
            pass
            
        return default_config
    
    def save_config(self):
        """Сохранение конфигурации"""
        try:
            with open(self.config_path, 'w', encoding='utf-8') as f:
                json.dump(self.data, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"Ошибка сохранения конфига: {e}")
    
    def set_function_applied(self, function_key: str, applied: bool):
        """Установить статус применения функции"""
        self.data.setdefault("functions", {})[function_key] = applied
        self.save_config()
    
    def is_function_applied(self, function_key: str) -> bool:
        """Проверить применена ли функция"""
        return self.data.get("functions", {}).get(function_key, False)
    
    # Совместимость со старым кодом
    def is_game_fixed(self, game_key: str) -> bool:
        return self.is_function_applied(f"game_{game_key}")
    
    def set_game_fixed(self, game_key: str, fixed: bool):
        self.set_function_applied(f"game_{game_key}", fixed)
    
    def is_program_installed(self, program_key: str) -> bool:
        return self.is_function_applied(f"program_{program_key}")
    
    def set_program_installed(self, program_key: str, installed: bool, version: str = ""):
        self.set_function_applied(f"program_{program_key}", installed)

# Глобальный инстанс конфига
config = Config()
