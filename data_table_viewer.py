import pandas as pd
from tabulate import tabulate

class DataFrameViewer:
    """Класс для интерактивного просмотра DataFrame с различными фильтрами"""

    def show_menu(self, df: pd.DataFrame) -> None:
        """Основное меню визуализации данных"""
        menu_text = """
        Меню табличной визуализации:
        1 - Вывод всех данных
        2 - Вывод данных с фильтрами
        3 - Вернуться в предыдущее меню
        """

        while True:
            print(menu_text)
            try:
                choice = int(input("Выберите действие: "))
                if choice == 1:
                    self._display_full_data(df)
                elif choice == 2:
                    self._display_with_filters(df)
                elif choice == 3:
                    return
                else:
                    print("Неверный ввод, попробуйте снова")
            except ValueError:
                print("Ошибка: введите число от 1 до 3")

    def _display_full_data(self, df: pd.DataFrame, max_rows: int = 20) -> None:
        """Вывод полного набора данных с пагинацией"""
        print("\nПолный набор данных:")
        print(f"Всего записей: {len(df)}")

        start = 0
        while start < len(df):
            print(tabulate(df.iloc[start:start+max_rows], headers="keys", tablefmt="psql"))
            start += max_rows

            if start < len(df):
                cont = input("Показать следующие записи? (y/n): ").lower()
                if cont != 'y':
                    break

    def _display_with_filters(self, df: pd.DataFrame) -> None:
        """Интерактивная фильтрация данных"""
        try:
            filtered_df = self._apply_filters(df)
            if not filtered_df.empty:
                print("\nРезультаты фильтрации:")
                print(tabulate(filtered_df, headers="keys", tablefmt="psql"))
                print(f"Найдено записей: {len(filtered_df)}")
            else:
                print("Нет данных, соответствующих условиям")
        except Exception as e:
            print(f"Ошибка фильтрации: {str(e)}")

    def _apply_filters(self, df: pd.DataFrame) -> pd.DataFrame:
        """Применение цепочки фильтров к DataFrame"""
        filtered_df = df.copy()

        # Фильтр по диапазону индексов
        filtered_df = self._index_filter(filtered_df)

        # Выбор столбцов
        filtered_df = self._column_filter(filtered_df)

        # Сортировка
        filtered_df = self._sort_filter(filtered_df)

        # Фильтрация по значению
        filtered_df = self._value_filter(filtered_df)

        return filtered_df

    def _index_filter(self, df: pd.DataFrame) -> pd.DataFrame:
        """Фильтрация по диапазону индексов"""
        while True:
            try:
                print(f"Доступный диапазон индексов: 0-{len(df)-1}")
                start = int(input("Начальный индекс (Enter для пропуска): ") or 0)
                end = int(input("Конечный индекс (Enter для конца): ") or len(df))

                if 0 <= start < end <= len(df):
                    return df.iloc[start:end]
                print("Некорректный диапазон индексов")
            except ValueError:
                print("Ошибка: введите целые числа")

    def _column_filter(self, df: pd.DataFrame) -> pd.DataFrame:
        """Выбор отображаемых столбцов"""
        print("Доступные столбцы:")
        print(", ".join(df.columns))

        while True:
            columns = input("Введите нужные столбцы через запятую (или Enter для всех): ")
            if not columns:
                return df

            selected = [col.strip() for col in columns.split(",")]
            missing = [col for col in selected if col not in df.columns]

            if not missing:
                return df[selected]

            print(f"Столбцы не найдены: {', '.join(missing)}")

    def _sort_filter(self, df: pd.DataFrame) -> pd.DataFrame:
        """Сортировка данных"""
        while True:
            column = input("Столбец для сортировки (Enter для пропуска): ").strip()
            if not column:
                return df

            if column in df.columns:
                asc = input("Сортировать по возрастанию? (y/n): ").lower() == 'y'
                return df.sort_values(column, ascending=asc)

            print(f"Столбец '{column}' не существует")

    def _value_filter(self, df: pd.DataFrame) -> pd.DataFrame:
        """Фильтрация по значению в столбце"""
        while True:
            column = input("Столбец для фильтрации (Enter для пропуска): ").strip()
            if not column:
                return df

            if column not in df.columns:
                print(f"Столбец '{column}' не существует")
                continue

            try:
                value = input(f"Значение для фильтрации в '{column}': ").strip()
                if not value:
                    return df

                # Автоматическое преобразование типа данных
                dtype = df[column].dtype
                converted_value = pd.to_numeric(value, errors="ignore") if dtype != 'object' else value

                return df[df[column] == converted_value]
            except Exception as e:
                print(f"Ошибка фильтрации: {str(e)}")
