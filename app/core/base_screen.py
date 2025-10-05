from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
                           QLabel, QScrollArea, QFrame)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
import os
import sys

current_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, current_dir)

from core.function_loader import function_loader
from config import config


class BaseScreen(QWidget):
    """Базовый класс для всех экранов с автозагрузкой функций"""
    
    def __init__(self, title, description, category):
        super().__init__()
        self.title = title
        self.description = description
        self.category = category
        self.initUI()

    def initUI(self):
        """Базовая инициализация UI"""
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(15)

        # Заголовок
        title_label = QLabel(self.title)
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_font = QFont()
        title_font.setPointSize(18)
        title_font.setBold(True)
        title_label.setFont(title_font)
        title_label.setStyleSheet("color: white; margin: 10px;")
        main_layout.addWidget(title_label)

        # Описание
        if self.description:
            desc_label = QLabel(self.description)
            desc_label.setStyleSheet("color: rgba(255,255,255,0.8); font-size: 14px; margin: 10px;")
            desc_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            desc_label.setWordWrap(True)
            main_layout.addWidget(desc_label)

        # Scroll area для функций
        scroll_area = QScrollArea()
        scroll_widget = QWidget()
        self.scroll_layout = QVBoxLayout()
        self.scroll_layout.setSpacing(10)

        # Автозагрузка функций
        self.load_functions()

        self.scroll_layout.addStretch(1)
        scroll_widget.setLayout(self.scroll_layout)
        scroll_area.setWidget(scroll_widget)
        scroll_area.setWidgetResizable(True)
        scroll_area.setStyleSheet("QScrollArea { border: none; background: transparent; }")

        main_layout.addWidget(scroll_area)
        self.setLayout(main_layout)

    def load_functions(self):
        """Автозагрузка функций из указанной категории"""
        functions = function_loader.get_functions_by_category(self.category)
        
        for function in functions:
            self.create_function_widget(function)

    def create_function_widget(self, function):
        """Создание виджета для функции"""
        widget = QFrame()
        widget.setStyleSheet("""
            QFrame {
                background-color: rgba(255, 255, 255, 0.05);
                border-radius: 10px;
                padding: 15px;
            }
            QFrame:hover {
                background-color: rgba(255, 255, 255, 0.08);
            }
        """)

        layout = QHBoxLayout()

        # Текстовая информация
        text_layout = QVBoxLayout()

        name_label = QLabel(function.name)
        name_label.setStyleSheet("color: white; font-size: 16px; font-weight: bold;")

        desc_label = QLabel(function.description)
        desc_label.setStyleSheet("color: rgba(255,255,255,0.8); font-size: 12px;")
        desc_label.setWordWrap(True)

        text_layout.addWidget(name_label)
        text_layout.addWidget(desc_label)
        text_layout.addStretch(1)

        # Кнопка действия
        action_button = QPushButton()
        action_button.setMinimumWidth(100)
        action_button.setMinimumHeight(35)

        # Обновляем состояние кнопки
        self.update_action_button(action_button, function)

        # Подключаем обработчик
        action_button.clicked.connect(
            lambda checked, func=function: self.handle_function_action(func)
        )

        layout.addLayout(text_layout)
        layout.addWidget(action_button)

        widget.setLayout(layout)
        self.scroll_layout.addWidget(widget)

    def update_action_button(self, button, function):
        """Обновление состояния кнопки (можно переопределить в дочерних классах)"""
        if function.is_applied():
            button.setText("Убрать")
            button.setStyleSheet("""
                QPushButton {
                    background-color: rgba(255, 100, 100, 0.3);
                    color: white;
                    border: none;
                    border-radius: 8px;
                    font-weight: bold;
                }
                QPushButton:hover {
                    background-color: rgba(255, 100, 100, 0.4);
                }
            """)
        else:
            button.setText("Применить")
            button.setStyleSheet("""
                QPushButton {
                    background-color: rgba(255, 255, 255, 0.1);
                    color: white;
                    border: none;
                    border-radius: 8px;
                    font-weight: bold;
                }
                QPushButton:hover {
                    background-color: rgba(255, 255, 255, 0.2);
                }
            """)

    def handle_function_action(self, function):
        """Обработчик действия функции (можно переопределить в дочерних классах)"""
        from PyQt6.QtWidgets import QMessageBox
        
        if function.is_applied():
            # Убираем функцию
            success = function.remove()
            if success:
                config.set_function_applied(function.key, False)
                QMessageBox.information(self, "Успех", f"{function.name} убрано!")
            else:
                QMessageBox.warning(self, "Ошибка", f"Не удалось убрать {function.name}")
        else:
            # Применяем функцию
            success = function.apply()
            if success:
                config.set_function_applied(function.key, True)
                QMessageBox.information(self, "Успех", f"{function.name} применено!")
            else:
                QMessageBox.warning(self, "Ошибка", f"Не удалось применить {function.name}")

        # Обновляем интерфейс
        self.initUI()
