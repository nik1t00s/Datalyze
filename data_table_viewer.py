"""Модуль для просмотра и фильтрации табличных данных.

Особенности:
- Постраничный вывод с навигацией
- Интерактивная фильтрация по столбцам
- Сортировка результатов

Классы:
    DataFrameViewer: Обеспечивает функциональность просмотра таблиц.
"""

from tabulate import tabulate
import pandas as pd


def _show_filtered_data(filtered_df: pd.DataFrame):
    """Отображает отфильтрованные данные в табличном формате.

    Args:
        filtered_df: DataFrame после применения фильтров

    Handles:
        - Случай пустого DataFrame
        - Красивое форматирование через tabulate
    """
    if filtered_df.empty:
        print("Нет данных, соответствующих фильтру.")
        return

    print(f"\nРезультаты фильтрации ({len(filtered_df)} записей):")
    print(tabulate(filtered_df, headers="keys", tablefmt="psql"))


def _filter_data(df: pd.DataFrame):
    """Фильтрует данные по интерактивному сценарию.

    Workflow:
        1. Выбор столбцов для отображения
        2. Фильтрация по значению в столбце
        3. Сортировка результатов

    Args:
        df: Исходный DataFrame для фильтрации

    Output:
        Выводит отфильтрованную таблицу через tabulate
    """
    print("\n=== Фильтрация данных ===")
    print("Доступные столбцы:", ', '.join(df.columns))

    try:
        # Этап 1: Выбор столбцов
        columns_to_show = input(
            "Введите столбцы для отображения (через запятую, или оставьте пустым для всех): ").strip()
        if columns_to_show:
            columns = [col.strip() for col in columns_to_show.split(',')]
            df = df[columns]

        # Этап 2: Фильтрация
        print("\n[Шаг 1/2] Фильтрация...")
        filter_column = input("Введите столбец для фильтрации: ").strip()
        if filter_column not in df.columns:
            print("Ошибка: столбец не найден!")
            return

        filter_value = input(f"Введите значение для фильтрации ({filter_column}): ").strip()
        filtered_df = df[df[filter_column].astype(str).str.contains(filter_value, case=False)]

        # Этап 3: Сортировка
        print("\n[Шаг 2/2] Сортировка...")
        sort_column = input("Введите столбец для сортировки (оставьте пустым, если не нужно): ").strip()
        if sort_column and sort_column in filtered_df.columns:
            ascending = input("Сортировать по возрастанию (y/n)? ").strip().lower() == 'y'
            filtered_df = filtered_df.sort_values(by=sort_column, ascending=ascending)

        # Отображение результатов
        print("\nИдет обработка данных...")
        _show_filtered_data(filtered_df)
    except Exception as e:
        print(f"Ошибка: {str(e)}")


class DataFrameViewer:
    """Реализует интерфейс для работы с табличными данными.

    Attributes:
        localizer: Объект локализации для текстов интерфейса
        page_size: Количество строк на странице при постраничном выводе
    """

    def __init__(self, localizer):
        """Инициализирует просмотрщик таблиц.

        Args:
            localizer: Объект для получения локализованных строк
        """
        self.localizer = localizer
        self.page_size = 20

    def show_menu(self, df: pd.DataFrame):
        """Отображает главное меню просмотра таблицы.

        Args:
            df: DataFrame для просмотра

        Menu Options:
            1. Полный просмотр (постраничный)
            2. Фильтрация данных
            3. Вернуться
        """
        while True:
            print(f"\n{self.localizer.get_string(41)}")
            print("1. Полный просмотр")
            print("2. Фильтрация данных")
            print("3. Вернуться")

            try:
                choice = int(input("Выберите действие: "))
                if choice == 1:
                    self._show_full_data(df)
                elif choice == 2:
                    _filter_data(df)
                else:
                    return
            except ValueError:
                print(self.localizer.get_string(9))

    def _show_full_data(self, df: pd.DataFrame):
        """Выводит данные постранично с возможностью навигации.

        Args:
            df: DataFrame для отображения

        Features:
            - Показывает общее количество строк
            - По 20 строк на страницу
            - Запрос подтверждения для продолжения
        """
        print(f"\n{self.localizer.get_string(42)}: {len(df)}")
        for i in range(0, len(df), self.page_size):
            print(tabulate(df.iloc[i:i + self.page_size], headers="keys", tablefmt="psql"))
            if input(f"{self.localizer.get_string(43)} (y/n): ").lower() != "y":
                break
