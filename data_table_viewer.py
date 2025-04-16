from tabulate import tabulate
import pandas as pd

class DataFrameViewer:
    def __init__(self, localizer):
        self.localizer = localizer
        self.page_size = 20

    def show_menu(self, df: pd.DataFrame):
        """Меню просмотра таблицы"""
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
                    self._filter_data(df)
                else:
                    return
            except ValueError:
                print(self.localizer.get_string(9))

    def _show_full_data(self, df: pd.DataFrame):
        """Постраничный вывод"""
        print(f"\n{self.localizer.get_string(42)}: {len(df)}")
        for i in range(0, len(df), self.page_size):
            print(tabulate(df.iloc[i:i+self.page_size], headers="keys", tablefmt="psql"))
            if input(f"{self.localizer.get_string(43)} (y/n): ").lower() != "y":
                break

    def _filter_data(self, df: pd.DataFrame):
        """Фильтрация данных с выбором столбцов и сортировкой"""
        print("\n=== Фильтрация данных ===")
        print("Доступные столбцы:", ', '.join(df.columns))
        
        try:
            # Выбор столбцов для отображения
            columns_to_show = input("Введите столбцы для отображения (через запятую, или оставьте пустым для всех): ").strip()
            if columns_to_show:
                columns = [col.strip() for col in columns_to_show.split(',')]
                df = df[columns]
            
            # Фильтрация
            print("\n[Шаг 1/2] Фильтрация...")
            filter_column = input("Введите столбец для фильтрации: ").strip()
            if filter_column not in df.columns:
                print("Ошибка: столбец не найден!")
                return
                
            filter_value = input(f"Введите значение для фильтрации ({filter_column}): ").strip()
            filtered_df = df[df[filter_column].astype(str).str.contains(filter_value, case=False)]
            
            # Сортировка
            print("\n[Шаг 2/2] Сортировка...")
            sort_column = input("Введите столбец для сортировки (оставьте пустым, если не нужно): ").strip()
            if sort_column and sort_column in filtered_df.columns:
                ascending = input("Сортировать по возрастанию (y/n)? ").strip().lower() == 'y'
                filtered_df = filtered_df.sort_values(by=sort_column, ascending=ascending)
            
            # Отображение
            print("\nИдет обработка данных...")
            self._show_filtered_data(filtered_df)
            
        except Exception as e:
            print(f"Ошибка: {str(e)}")

    def _apply_filters(self, df: pd.DataFrame) -> pd.DataFrame:
        """Применение фильтров"""
        # Реализация фильтров из предыдущей версии
        return df
    def _show_filtered_data(self, filtered_df: pd.DataFrame):
        """Отображение отфильтрованных данных"""
        if filtered_df.empty:
            print("Нет данных, соответствующих фильтру.")
            return

        print(f"\nРезультаты фильтрации ({len(filtered_df)} записей):")
        print(tabulate(filtered_df, headers="keys", tablefmt="psql"))