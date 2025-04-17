"""Модуль для визуализации данных через matplotlib.

Поддерживаемые графики:
- Столбчатые диаграммы
- Линейные графики

Классы:
    DataFrameVisualizer: Управляет построением графиков.

Пример:
    visualizer = DataFrameVisualizer(localizer)
    visualizer.show_menu(df)

Требования:
    - matplotlib>=3.0
"""

import matplotlib.pyplot as plt
import pandas as pd
import matplotlib as mpl

mpl.rcParams['agg.path.chunksize'] = 10000

class DataFrameVisualizer:
    def __init__(self, localizer):
        self.localizer = localizer

    def show_menu(self, df: pd.DataFrame):
        """Меню визуализации"""
        while True:
            print(f"\n{self.localizer.get_string(48)}")
            print("1. Столбчатая диаграмма")
            print("2. Линейный график")
            print("3. Вернуться")

            try:
                choice = int(input("Выберите действие: "))
                if choice == 1:
                    self._plot_chart(df, "bar")
                elif choice == 2:
                    self._plot_chart(df, "line")
                else:
                    return
            except ValueError:
                print(self.localizer.get_string(9))

    def _plot_chart(self, df: pd.DataFrame, chart_type: str):
        """Построение графика указанного типа.
    
        Args:
            df: DataFrame с данными.
            chart_type: Тип графика ('bar' или 'line').
        
        Raises:
            KeyError: Если указаны неверные столбцы.
        """
        print(f"\nДоступные столбцы: {', '.join(df.columns)}")
        try:
            x_col = input(f"{self.localizer.get_string(49)}: ").strip()
            y_col = input(f"{self.localizer.get_string(50)}: ").strip()

            if x_col not in df.columns or y_col not in df.columns:
                print(self.localizer.get_string(51))
                return

            plt.figure(figsize=(12, 6))
            if chart_type == "bar":
                df.plot.bar(x=x_col, y=y_col, ax=plt.gca())
            else:
               df.plot.line(x=x_col, y=y_col, ax=plt.gca())

            plt.title(f"{y_col} vs {x_col}")
            plt.tight_layout()
            plt.show(block = False)
        except Exception as e:
            print(f"{self.localizer.get_string(52)}: {str(e)}")
