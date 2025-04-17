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


class MainApplication:
    def __init__(self):
        """Инициализирует главное приложение.

        Создает:
            - Пустой DataFrame для хранения данных
            - Объект локализации
            - Основные компоненты приложения
        """
        self.df = pd.DataFrame()
        self.localizer = Localizer()
        self._init_components()
        self._show_welcome()
        self.run()

    def _init_components(self):
        """Инициализирует основные компоненты приложения.

        Создает:
            - Импортер/экспортер данных
            - Просмотрщик таблиц
            - Визуализатор данных

        Raises:
            SystemExit: Если инициализация не удалась
        """
        try:
            self.importer = DataImporterExporter(self.localizer, self)
            self.table_viewer = DataFrameViewer(self.localizer)
            self.visualizer = DataFrameVisualizer(self.localizer)
        except Exception as e:
            print(f"{self.localizer.get_string(14)}: {str(e)}")
            exit(1)

    def _show_welcome(self):
        """Выводит приветственное сообщение при запуске."""
        print("=" * 50)
        print(self.localizer.get_string(0))
        print(self.localizer.get_string(1))
        print("=" * 50)
        print("\n")

    def run(self):
        """Основной цикл работы приложения.

        Обрабатывает:
            - Отображение меню
            - Ввод пользователя
            - Обработку выбора
            - Критические ошибки
        """
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
        """Отображает главное меню с локализованными строками."""
        print(f"\n{self.localizer.get_string(2)}")
        print(f"0 - {self.localizer.get_string(5)}")
        print(f"1 - {self.localizer.get_string(6)}")
        print(f"2 - {self.localizer.get_string(7)}")
        print(f"3 - {self.localizer.get_string(8)}")

    def _get_user_choice(self) -> int:
        """Получает и валидирует выбор пользователя.

        Returns:
            int: Выбранный пункт меню

        Note:
            Повторяет запрос при некорректном вводе
        """
        while True:
            try:
                return int(input(f"{self.localizer.get_string(17)}: "))
            except ValueError:
                print(self.localizer.get_string(9))

    def _handle_menu_choice(self, choice: int):
        """Обрабатывает выбор пункта меню.

        Args:
            choice: Выбранный пункт меню

        Checks:
            - Загружены ли данные для просмотра/визуализации
        """
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
        """Обрабатывает операции импорта/экспорта данных.

        Обновляет:
            self.df: Если импорт прошел успешно
        """
        success, new_df = self.importer.show_menu()
        if success:
            self.df = new_df
            print(self.localizer.get_string(11).format(len(self.df)))

    def _show_data_table(self):
        """Запускает просмотр данных в табличном виде."""
        self.table_viewer.show_menu(self.df)

    def _show_data_charts(self):
        """Запускает визуализацию данных."""
        self.visualizer.show_menu(self.df)

    def _exit_application(self):
        """Выводит сообщение о завершении работы."""
        print(f"\n{self.localizer.get_string(12)}")
        print(self.localizer.get_string(13))


if __name__ == "__main__":
    app = MainApplication()
