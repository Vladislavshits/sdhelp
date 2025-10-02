from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
                           QTabWidget, QLabel, QScrollArea, QCheckBox, QFrame)
from PyQt6.QtCore import Qt, QFile, QTextStream
from PyQt6.QtGui import QFont


class CustomFixScreen(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.loadStyles()

    def initUI(self):
        # Основной layout
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(20)

        # Заголовок
        title_label = QLabel("Выбор исправлений")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_font = QFont()
        title_font.setPointSize(24)
        title_font.setBold(True)
        title_label.setFont(title_font)
        title_label.setStyleSheet("color: white; margin: 20px;")

        main_layout.addWidget(title_label)

        # Создание вкладок
        self.tabs = QTabWidget()

        # Вкладка "Игры"
        games_tab = self.createGamesTab()
        self.tabs.addTab(games_tab, "🎮 Игры")

        # Вкладка "Программы"
        apps_tab = self.createAppsTab()
        self.tabs.addTab(apps_tab, "📱 Программы")

        # Вкладка "SteamOS"
        steamos_tab = self.createSteamOSTab()
        self.tabs.addTab(steamos_tab, "⚙️ SteamOS")

        # Вкладка "Сеть"
        network_tab = self.createNetworkTab()
        self.tabs.addTab(network_tab, "🌐 Сеть")

        main_layout.addWidget(self.tabs)

        # Панель с кнопкой назад
        bottom_layout = QHBoxLayout()

        # Кнопка назад
        self.back_button = QPushButton("Назад")
        self.back_button.setMinimumHeight(50)
        back_font = QFont()
        back_font.setPointSize(14)
        back_font.setBold(True)
        self.back_button.setFont(back_font)

        bottom_layout.addWidget(self.back_button)
        bottom_layout.addStretch(1)

        main_layout.addLayout(bottom_layout)

        self.setLayout(main_layout)

    def createGamesTab(self):
        """Создание вкладки с настройками игр"""
        scroll_widget = QWidget()
        layout = QVBoxLayout()

        # Заголовок вкладки
        tab_title = QLabel("Оптимизация игр")
        tab_title.setStyleSheet("color: white; font-size: 18px; font-weight: bold; margin: 10px;")
        layout.addWidget(tab_title)

        # Чекбоксы для игровых исправлений
        fixes = [
            "Оптимизация производительности в играх",
            "Исправление лагов в Proton",
            "Настройка контроллеров для не-Steam игр",
            "Оптимизация шейдерного кэша",
            "Исправление проблем с звуком в играх",
            "Настройка гироскопа",
            "Оптимизация батареи в игровом режиме"
        ]

        for fix in fixes:
            checkbox = QCheckBox(fix)
            checkbox.setStyleSheet("""
                QCheckBox {
                    color: white;
                    font-size: 14px;
                    margin: 8px;
                    padding: 5px;
                }
                QCheckBox::indicator {
                    width: 20px;
                    height: 20px;
                }
                QCheckBox::indicator:unchecked {
                    background-color: #5d4e7b;
                    border: 2px solid #7d6e9b;
                    border-radius: 4px;
                }
                QCheckBox::indicator:checked {
                    background-color: #8a7bac;
                    border: 2px solid #9d8ebf;
                    border-radius: 4px;
                }
            """)
            layout.addWidget(checkbox)

        layout.addStretch(1)
        scroll_widget.setLayout(layout)

        # Создание scroll area
        scroll_area = QScrollArea()
        scroll_area.setWidget(scroll_widget)
        scroll_area.setWidgetResizable(True)
        scroll_area.setStyleSheet("""
            QScrollArea {
                border: none;
                background-color: rgba(255, 255, 255, 0.1);
                border-radius: 10px;
            }
        """)

        return scroll_area

    def createAppsTab(self):
        """Создание вкладки с настройками программ"""
        scroll_widget = QWidget()
        layout = QVBoxLayout()

        tab_title = QLabel("Установка и настройка программ")
        tab_title.setStyleSheet("color: white; font-size: 18px; font-weight: bold; margin: 10px;")
        layout.addWidget(tab_title)

        fixes = [
            "Установка Wine и дополнительных библиотек",
            "Настройка файлового менеджера",
            "Установка медиа-кодеков",
            "Настройка браузера",
            "Установка офисных приложений",
            "Настройка эмуляторов",
            "Установка системных утилит"
        ]

        for fix in fixes:
            checkbox = QCheckBox(fix)
            checkbox.setStyleSheet("""
                QCheckBox {
                    color: white;
                    font-size: 14px;
                    margin: 8px;
                    padding: 5px;
                }
                QCheckBox::indicator {
                    width: 20px;
                    height: 20px;
                }
            """)
            layout.addWidget(checkbox)

        layout.addStretch(1)
        scroll_widget.setLayout(layout)

        scroll_area = QScrollArea()
        scroll_area.setWidget(scroll_widget)
        scroll_area.setWidgetResizable(True)
        scroll_area.setStyleSheet("QScrollArea { border: none; background-color: rgba(255, 255, 255, 0.1); border-radius: 10px; }")

        return scroll_area

    def createSteamOSTab(self):
        """Создание вкладки с настройками SteamOS"""
        scroll_widget = QWidget()
        layout = QVBoxLayout()

        tab_title = QLabel("Настройка SteamOS")
        tab_title.setStyleSheet("color: white; font-size: 18px; font-weight: bold; margin: 10px;")
        layout.addWidget(tab_title)

        fixes = [
            "Оптимизация системы",
            "Настройка интерфейса",
            "Исправление системных ошибок",
            "Обновление драйверов",
            "Настройка энергосбережения",
            "Оптимизация хранилища",
            "Резервное копирование настроек"
        ]

        for fix in fixes:
            checkbox = QCheckBox(fix)
            checkbox.setStyleSheet("""
                QCheckBox {
                    color: white;
                    font-size: 14px;
                    margin: 8px;
                    padding: 5px;
                }
                QCheckBox::indicator {
                    width: 20px;
                    height: 20px;
                }
            """)
            layout.addWidget(checkbox)

        layout.addStretch(1)
        scroll_widget.setLayout(layout)

        scroll_area = QScrollArea()
        scroll_area.setWidget(scroll_widget)
        scroll_area.setWidgetResizable(True)
        scroll_area.setStyleSheet("QScrollArea { border: none; background-color: rgba(255, 255, 255, 0.1); border-radius: 10px; }")

        return scroll_area

    def createNetworkTab(self):
        """Создание вкладки с сетевыми настройками"""
        scroll_widget = QWidget()
        layout = QVBoxLayout()

        tab_title = QLabel("Настройка сети")
        tab_title.setStyleSheet("color: white; font-size: 18px; font-weight: bold; margin: 10px;")
        layout.addWidget(tab_title)

        fixes = [
            "Оптимизация Wi-Fi соединения",
            "Настройка DNS",
            "Исправление проблем с Bluetooth",
            "Оптимизация загрузки в Steam",
            "Настройка VPN",
            "Исправление разрыва соединения",
            "Оптимизация работы в локальной сети"
        ]

        for fix in fixes:
            checkbox = QCheckBox(fix)
            checkbox.setStyleSheet("""
                QCheckBox {
                    color: white;
                    font-size: 14px;
                    margin: 8px;
                    padding: 5px;
                }
                QCheckBox::indicator {
                    width: 20px;
                    height: 20px;
                }
            """)
            layout.addWidget(checkbox)

        layout.addStretch(1)
        scroll_widget.setLayout(layout)

        scroll_area = QScrollArea()
        scroll_area.setWidget(scroll_widget)
        scroll_area.setWidgetResizable(True)
        scroll_area.setStyleSheet("QScrollArea { border: none; background-color: rgba(255, 255, 255, 0.1); border-radius: 10px; }")

        return scroll_area

    def loadStyles(self):
        """Загрузка стилей из файла"""
        try:
            style_file = QFile("app/styles.qss")
            if style_file.open(QFile.OpenModeFlag.ReadOnly | QFile.OpenModeFlag.Text):
                stream = QTextStream(style_file)
                self.setStyleSheet(stream.readAll())
                style_file.close()
        except Exception as e:
            print(f"Ошибка загрузки стилей: {e}")
