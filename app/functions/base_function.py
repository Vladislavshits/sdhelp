import os
import subprocess
import logging
from abc import ABC, abstractmethod

class BaseFunction(ABC):
    """Базовый класс для всех функций в программе"""
    
    def __init__(self):
        self.logger = logging.getLogger(self.__class__.__name__)
        self.scripts_dir = os.path.join(os.path.dirname(__file__), "..", "scripts")
    
    @property
    @abstractmethod
    def name(self):
        """Название функции (обязательно к реализации)"""
        pass
    
    @property
    @abstractmethod
    def description(self):
        """Описание функции (обязательно к реализации)"""
        pass
    
    @property
    def key(self):
        """Уникальный ключ функции (по умолчанию имя класса в lower)"""
        return self.__class__.__name__.lower()
    
    @property
    def category(self):
        """Категория функции (games/programs/steamos/network)"""
        return self.__class__.__module__.split('.')[-2]
    
    def run_script(self, script_name, *args):
        """Запуск bash/python скрипта из папки scripts"""
        script_path = os.path.join(self.scripts_dir, self.category, script_name)
        
        if not os.path.exists(script_path):
            self.logger.error(f"Скрипт не найден: {script_path}")
            return False
        
        try:
            if script_name.endswith('.sh'):
                # Запуск bash скрипта
                result = subprocess.run(
                    ['bash', script_path] + list(args),
                    capture_output=True, text=True, check=True
                )
            elif script_name.endswith('.py'):
                # Запуск python скрипта
                result = subprocess.run(
                    ['python3', script_path] + list(args),
                    capture_output=True, text=True, check=True
                )
            else:
                self.logger.error(f"Неизвестный тип скрипта: {script_name}")
                return False
            
            self.logger.info(f"Скрипт выполнен: {script_name}")
            self.logger.debug(f"Вывод: {result.stdout}")
            return True
            
        except subprocess.CalledProcessError as e:
            self.logger.error(f"Ошибка выполнения скрипта {script_name}: {e}")
            self.logger.error(f"Stderr: {e.stderr}")
            return False
    
    def execute_command(self, command, shell=False):
        """Выполнение системной команды"""
        try:
            result = subprocess.run(
                command if not shell else command,
                shell=shell,
                capture_output=True, 
                text=True, 
                check=True
            )
            self.logger.info(f"Команда выполнена: {command}")
            return True
        except subprocess.CalledProcessError as e:
            self.logger.error(f"Ошибка выполнения команды: {e}")
            return False
    
    @abstractmethod
    def apply(self):
        """Применить функцию (обязательно к реализации)"""
        pass
    
    def remove(self):
        """Убрать функцию (опционально, по умолчанию просто True)"""
        return True
    
    def is_applied(self):
        """Проверить применена ли функция (опционально)"""
        # Базовая реализация через конфиг
        from config import config
        return config.is_function_applied(self.key)
    
    def to_dict(self):
        """Представление функции в виде словаря для UI"""
        return {
            "name": self.name,
            "description": self.description,
            "key": self.key,
            "category": self.category,
            "class": self.__class__
        }
