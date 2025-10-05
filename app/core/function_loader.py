import os
import importlib
import pkgutil
import logging
from typing import Dict, List, Type
from functions.base_function import BaseFunction

class FunctionLoader:
    """Автозагрузчик функций из папок"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.functions: Dict[str, Type[BaseFunction]] = {}
        self.load_all_functions()
    
    def load_all_functions(self):
        """Загрузить все функции из папки functions"""
        functions_package = "functions"
        
        # Ищем все подпакеты в functions (games, programs, etc)
        package_path = os.path.join(os.path.dirname(__file__), "..", functions_package)
        
        for category in os.listdir(package_path):
            category_path = os.path.join(package_path, category)
            
            if os.path.isdir(category_path) and not category.startswith('__'):
                self.load_functions_from_category(functions_package, category)
    
    def load_functions_from_category(self, base_package: str, category: str):
        """Загрузить функции из конкретной категории"""
        category_package = f"{base_package}.{category}"
        
        try:
            category_module = importlib.import_module(category_package)
            
            # Ищем все модули в категории
            for _, module_name, is_pkg in pkgutil.iter_modules(category_module.__path__):
                if not is_pkg and not module_name.startswith('__'):
                    self.load_function_from_module(category_package, module_name)
                    
        except ImportError as e:
            self.logger.warning(f"Не удалось загрузить категорию {category}: {e}")
    
    def load_function_from_module(self, category_package: str, module_name: str):
        """Загрузить функцию из конкретного модуля"""
        try:
            full_module_name = f"{category_package}.{module_name}"
            module = importlib.import_module(full_module_name)
            
            # Ищем классы наследованные от BaseFunction
            for attr_name in dir(module):
                attr = getattr(module, attr_name)
                
                if (isinstance(attr, type) and 
                    issubclass(attr, BaseFunction) and 
                    attr != BaseFunction):
                    
                    # Создаем экземпляр и регистрируем
                    function_instance = attr()
                    self.functions[function_instance.key] = function_instance
                    
                    self.logger.info(f"Загружена функция: {function_instance.name}")
                    
        except Exception as e:
            self.logger.error(f"Ошибка загрузки функции {module_name}: {e}")
    
    def get_functions_by_category(self, category: str) -> List[BaseFunction]:
        """Получить все функции определенной категории"""
        return [
            func for func in self.functions.values() 
            if func.category == category
        ]
    
    def get_function(self, key: str) -> BaseFunction:
        """Получить функцию по ключу"""
        return self.functions.get(key)
    
    def get_all_functions(self) -> List[BaseFunction]:
        """Получить все функции"""
        return list(self.functions.values())

# Глобальный инстанс загрузчика
function_loader = FunctionLoader()
