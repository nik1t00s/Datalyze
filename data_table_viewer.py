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
        """Фильтрация данных"""
        try:
            filtered_df = df.copy()
            filtered_df = self._apply_filters(filtered_df)

            if not filtered_df.empty:
                print(f"\n{self.localizer.get_string(44)}:")
                print(tabulate(filtered_df, headers="keys", tablefmt="psql"))
                print(f"{self.localizer.get_string(45)}: {len(filtered_df)}")
            else:
                print(self.localizer.get_string(46))
        except Exception as e:
            print(f"{self.localizer.get_string(47)}: {str(e)}")

    def _apply_filters(self, df: pd.DataFrame) -> pd.DataFrame:
        """Применение фильтров"""
        # Реализация фильтров из предыдущей версии
        return df
