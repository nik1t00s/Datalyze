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
        """Инициализирует визуализатор.

        Args:
            localizer: Объект локализации для получения текстов интерфейса
        """
        self.localizer = localizer

    def show_menu(self, df: pd.DataFrame):
        """Отображает меню визуализации и обрабатывает выбор пользователя.

        Args:
            df: DataFrame с данными для визуализации

        Menu Options:
            1. Столбчатая диаграмма
            2. Линейный график
            3. Вернуться
        """
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
        """Строит график указанного типа.

        Args:
            df: DataFrame с данными
            chart_type: Тип графика ('bar' или 'line')

        Steps:
            1. Запрашивает столбцы для осей
            2. Валидирует ввод
            3. Строит график

        Raises:
            KeyError: Если указаны несуществующие столбцы
        """
        print(f"\nДоступные столбцы: {', '.join(df.columns)}")
        try:
            x_col = input(f"{self.localizer.get_string(49)}: ").strip()
            y_col = input(f"{self.localizer.get_string(50)}: ").strip()

            if x_col not in df.columns or y_col not in df.columns:
                print(self.localizer.get_string(51))
                return
            
            if chart_type == "line":
                if not pd.api.types.is_numeric_dtype(df[y_col]):
                    print("Ошибка: для линейного графика выберите числовой столбец для оси Y!")
                    return
                    
                if len(df) > 200:
                    print("Используется 200 случайных записей для предотвращения зависаний.")
                    df = df.sample(n=200)

            plt.figure(figsize=(12, 6))
            if chart_type == "bar":
                df.plot.bar(x=x_col, y=y_col, ax=plt.gca())
            else:
                df.plot.line(x=x_col, y=y_col, ax=plt.gca())

            plt.title(f"{y_col} vs {x_col}")
            plt.tight_layout()
            plt.show(block=False)
        except Exception as e:
            print(f"{self.localizer.get_string(52)}: {str(e)}")