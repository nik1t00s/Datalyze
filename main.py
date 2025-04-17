"""Главный модуль приложения для анализа медицинских данных.

Содержит класс `MainApplication`, который управляет основным циклом работы:
- Инициализация компонентов
- Отображение меню
- Обработка выбора пользователя

Пример использования:
    if __name__ == "__main__":
        app = MainApplication()

Модули:
    data_importer_exporter: Импорт/экспорт данных.
    data_table_viewer: Просмотр табличных данных.
    data_visualizer: Визуализация данных.
    localization: Локализация строк.
"""

from data_importer_exporter import DataImporterExporter
from localization import Localizer
from data_table_viewer import DataFrameViewer
from data_visualizer import DataFrameVisualizer
import pandas as pd
from pathlib import Path
import openpyxl

class MainApplication:
    def __init__(self):
        self.df = pd.DataFrame()
        self.localizer = Localizer()
        self._init_components()
        self._show_welcome()
        self.run()

    def _init_components(self):
        """Инициализация компонентов приложения"""
        try:
            self.importer = DataImporterExporter(self.localizer, self)
            self.table_viewer = DataFrameViewer(self.localizer)
            self.visualizer = DataFrameVisualizer(self.localizer)
        except Exception as e:
            print(f"{self.localizer.get_string(14)}: {str(e)}")
            exit(1)

    def _show_welcome(self):
        """Отображение приветственного сообщения"""
        print("=" * 50)
        print(self.localizer.get_string(0))
        print(self.localizer.get_string(1))
        print("=" * 50)
        print("\n")

    def run(self):
        """Основной цикл работы приложения"""
        while True:
            try:
                self._display_main_menu()
                choice = self._get_user_choice()

                if choice == 0:
                    self._exit_application()
                    break

                self._handle_menu_choice(choice)

            except KeyboardInterrupt:
                print(f"\n{self.localizer.get_string(15)}")
                break
            except Exception as e:
                print(f"{self.localizer.get_string(16)}: {str(e)}")

    def _display_main_menu(self):
        """Отображение главного меню"""
        print(f"\n{self.localizer.get_string(2)}")
        print(f"0 - {self.localizer.get_string(5)}")
        print(f"1 - {self.localizer.get_string(6)}")
        print(f"2 - {self.localizer.get_string(7)}")
        print(f"3 - {self.localizer.get_string(8)}")

    def _get_user_choice(self) -> int:
        """Получение выбора пользователя"""
        while True:
            try:
                return int(input(f"{self.localizer.get_string(17)}: "))
            except ValueError:
                print(self.localizer.get_string(9))

    def _handle_menu_choice(self, choice: int):
        """Обработка выбора пункта меню"""
        handlers = {
            1: self._handle_data_io,
            2: self._show_data_table,
            3: self._show_data_charts
        }

        if choice in handlers:
            if choice in [2, 3] and self.df.empty:
                print(self.localizer.get_string(10))
                return

            handlers[choice]()

    def _handle_data_io(self):
        """Работа с импортом/экспортом данных"""
        success, new_df = self.importer.show_menu()
        if success:
            self.df = new_df  # Сохранение данных
            print(self.localizer.get_string(11).format(len(self.df)))

    def _show_data_table(self):
        """Отображение данных в табличном виде"""
        self.table_viewer.show_menu(self.df)

    def _show_data_charts(self):
        """Визуализация данных в виде графиков"""
        self.visualizer.show_menu(self.df)

    def _exit_application(self):
        """Завершение работы приложения"""
        print(f"\n{self.localizer.get_string(12)}")
        print(self.localizer.get_string(13))

if __name__ == "__main__":
    app = MainApplication()
