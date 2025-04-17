"""Модуль для импорта и экспорта данных.

Поддерживает:
- Локальный импорт из CSV/XLSX
- Импорт с Kaggle API
- Экспорт в CSV/XLSX

Классы:
    DataImporterExporter: Основной класс для работы с импортом/экспортом данных.
"""

import pandas as pd
from pathlib import Path
from typing import Tuple
from kaggle.api.kaggle_api_extended import KaggleApi
import shutil

shutil.rmtree("temp", ignore_errors=True)  # Удаление временной папки при инициализации


class DataImporterExporter:
    """Обрабатывает операции импорта/экспорта данных.

    Attributes:
        localizer: Объект для локализации текстов
        main_app: Ссылка на главное приложение для доступа к данным
    """

    def __init__(self, localizer, main_app):
        """Инициализирует импортер/экспортер.

        Args:
            localizer: Объект локализации для получения текстов интерфейса
            main_app: Ссылка на главное приложение
        """
        self.localizer = localizer
        self.main_app = main_app

    def show_menu(self) -> Tuple[bool, pd.DataFrame]:
        """Отображает меню импорта/экспорта и обрабатывает выбор пользователя.

        Returns:
            Tuple[bool, pd.DataFrame]:
                - bool: Успешность операции
                - pd.DataFrame: Загруженные данные (пустой DataFrame при ошибке)

        Menu Options:
            1. Импорт с локального диска
            2. Импорт с Kaggle
            3. Экспорт данных
            4. Вернуться
        """
        print(f"\n{self.localizer.get_string(20)}")
        print("1. Импорт с локального диска")
        print("2. Импорт с Kaggle")
        print("3. Экспорт данных")
        print("4. Вернуться")

        try:
            choice = int(input("Выберите действие: "))
            if choice == 1:
                return self._local_import()
            elif choice == 2:
                return self._kaggle_import()
            elif choice == 3:
                return self._export_data()
            return False, pd.DataFrame()
        except ValueError:
            print(self.localizer.get_string(9))
            return False, pd.DataFrame()

    def _local_import(self) -> Tuple[bool, pd.DataFrame]:
        """Загружает данные из локального файла.

        Supported Formats:
            - CSV (.csv)
            - Excel (.xlsx, .xls)

        Returns:
            Tuple[bool, pd.DataFrame]:
                - bool: Успешность операции
                - pd.DataFrame: Загруженные данные

        Raises:
            KeyboardInterrupt: При отмене операции пользователем
        """
        try:
            path = input(f"{self.localizer.get_string(21)} (с именем файла): ").strip()
            file_path = Path(path)

            if not file_path.exists():
                print(self.localizer.get_string(22).format(file_path))
                return False, pd.DataFrame()

            try:
                if file_path.suffix == '.csv':
                    df = pd.read_csv(file_path)
                elif file_path.suffix in ('.xlsx', '.xls'):
                    df = pd.read_excel(file_path)
                else:
                    print(self.localizer.get_string(23))
                    return False, pd.DataFrame()

                return True, df
            except Exception as e:
                print(f"{self.localizer.get_string(25)}: {str(e)}")
                return False, pd.DataFrame()
        except KeyboardInterrupt:
            print("\nОперация отменена.")
            return False, pd.DataFrame()

    def _kaggle_import(self) -> Tuple[bool, pd.DataFrame]:
        """Загружает датасет с Kaggle через API.

        Workflow:
            1. Запрашивает URL датасета
            2. Аутентифицируется в Kaggle API
            3. Скачивает и распаковывает архив
            4. Загружает первый найденный CSV-файл

        Returns:
            Tuple[bool, pd.DataFrame]:
                - bool: Успешность операции
                - pd.DataFrame: Загруженные данные

        Raises:
            Exception: При ошибках API или загрузки файлов
        """
        print(f"\n{self.localizer.get_string(26)}")
        print(f"{self.localizer.get_string(27)}\n")

        dataset_url = input(f"{self.localizer.get_string(28)}: ").strip()

        try:
            api = KaggleApi()
            api.authenticate()

            parts = dataset_url.split('/')
            dataset_name = parts[-1]
            user = parts[-2]

            print(self.localizer.get_string(30))
            api.dataset_download_files(f"{user}/{dataset_name}", path="temp", unzip=True)

            csv_files = list(Path("temp").glob("*.csv"))

            if csv_files:
                df = pd.read_csv(csv_files[0])
                shutil.rmtree("temp")
                return True, df
            return False, pd.DataFrame()
        except Exception as e:
            print(f"{self.localizer.get_string(33)}: {str(e)}")
            return False, pd.DataFrame()

    def _export_data(self) -> Tuple[bool, pd.DataFrame]:
        """Экспортирует данные в файл с проверкой пути.

        Supported Formats:
            - CSV (.csv)
            - Excel (.xlsx)

        Returns:
            Tuple[bool, pd.DataFrame]:
                - bool: Успешность операции
                - pd.DataFrame: Текущие данные (не изменяются)

        Raises:
            Exception: При ошибках сохранения файла
        """
        if self.main_app.df.empty:
            print(self.localizer.get_string(10))
            return False, self.main_app.df

        try:
            path = input(f"{self.localizer.get_string(34)}: ").strip()
            filename = input(f"{self.localizer.get_string(35)}: ").strip()
            file_format = input(f"{self.localizer.get_string(36)}: ").lower().strip()

            export_path = Path(path) / f"{filename}.{file_format}"
            if not export_path.parent.exists():
                print(f"Ошибка: путь '{export_path.parent}' не существует!")
                return False, self.main_app.df

            export_path.parent.mkdir(parents=True, exist_ok=True)
            if file_format == "csv":
                self.main_app.df.to_csv(export_path, index=False)
            elif file_format == "xlsx":
                self.main_app.df.to_excel(export_path, index=False, engine="openpyxl")
            else:
                print(self.localizer.get_string(37))
                return False, self.main_app.df

            if export_path.exists():
                print(self.localizer.get_string(38).format(export_path))
                return True, self.main_app.df

            print("Ошибка: файл не был сохранен!")
            return False, self.main_app.df
        except Exception as e:
            print(f"{self.localizer.get_string(39)}: {str(e)}")
            return False, self.main_app.df
        
