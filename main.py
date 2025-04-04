from data_importer_exporter import DataImporterExporter
from localization import Localizer
from data_table_viewer import DataFrameViewer
from data_visualizer import DataFrameVisualizer
import pandas as pd

class MainApplication:
    MENU_OPTIONS = {
        0: "Exit",
        1: "Import/Export data",
        2: "Show data table",
        3: "Show data charts"
    }

    def __init__(self):
        self._initialize_components()
        self._show_welcome_message()
        self._setup_localization()
        self.run()

    def _initialize_components(self):
        """Инициализация компонентов приложения"""
        self.df = pd.DataFrame()
        self.localizer = Localizer()
        self.importer = DataImporterExporter()
        self.table_viewer = DataFrameViewer()
        self.visualizer = DataFrameVisualizer()

    def _show_welcome_message(self):
        """Отображение приветственного сообщения"""
        print("=" * 50)
        print("Добро пожаловать в систему анализа медицинских данных!")
        print("Программа разработана в рамках проектной работы по СиПИ")
        print("Разработчики:")
        print("Соколов А.В., Кожемякин А.А., Шиханова Е.В., Чайка Н.В.")
        print("=" * 50)
        print("\n")

    def _setup_localization(self):
        """Настройка локализации"""
        self.localizer = Localizer()
        print("Локализация успешно загружена\n")

    def run(self):
        """Основной цикл работы приложения"""
        while True:
            self._display_main_menu()
            choice = self._get_user_choice()

            if choice == 0:
                self._exit_application()
                break

            self._handle_menu_choice(choice)

    def _display_main_menu(self):
        """Отображение главного меню"""
        print("\nГлавное меню:")
        for key, value in self.MENU_OPTIONS.items():
            print(f"{key} - {value}")

    def _get_user_choice(self) -> int:
        """Получение выбора пользователя"""
        while True:
            try:
                return int(input("Выберите пункт меню: "))
            except ValueError:
                print("Ошибка: введите число от 0 до 3")

    def _handle_menu_choice(self, choice: int):
        """Обработка выбора пункта меню"""
        handlers = {
            1: self._handle_data_io,
            2: self._show_data_table,
            3: self._show_data_charts
        }

        if choice in handlers:
            if choice in [2, 3] and self.df.empty:
                print("Ошибка: данные не загружены!")
                return

            handlers[choice]()

    def _handle_data_io(self):
        """Работа с импортом/экспортом данных"""
        success, new_df = self.importer.import_export_menu(not self.df.empty, self.df)
        if success:
            self.df = new_df
            print(f"\nУспешно загружено {len(self.df)} записей")

    def _show_data_table(self):
        """Отображение данных в табличном виде"""
        self.table_viewer.show_menu(self.df)

    def _show_data_charts(self):
        """Визуализация данных в виде графиков"""
        self.visualizer.show_visualization_menu(self.df)

    def _exit_application(self):
        """Завершение работы приложения"""
        print("\nРабота программы завершена")
        print("Спасибо за использование нашего ПО!")

if __name__ == "__main__":
    app = MainApplication()
