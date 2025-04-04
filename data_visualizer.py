import matplotlib.pyplot as plt
import pandas as pd
from typing import Optional

class DataFrameVisualizer:
    """Класс для визуализации данных из DataFrame"""

    def show_visualization_menu(self, df: pd.DataFrame) -> None:
        """Меню выбора типа визуализации"""
        menu = """
        Меню визуализации данных:
        1 - Столбчатая диаграмма
        2 - Линейный график
        3 - Вернуться в предыдущее меню
        """

        while True:
            print(menu)
            try:
                choice = int(input("Выберите тип визуализации: "))
                if choice == 1:
                    self._plot_bar_chart(df)
                elif choice == 2:
                    self._plot_line_chart(df)
                elif choice == 3:
                    return
                else:
                    print("Неверный ввод, выберите 1-3")
            except ValueError:
                print("Ошибка: введите число от 1 до 3")

    def _get_valid_columns(self, df: pd.DataFrame) -> Optional[tuple[str, str]]:
        """Получение и валидация названий столбцов"""
        print("Доступные столбцы:")
        print(", ".join(df.columns))

        while True:
            x_col = input("Введите столбец для оси X (или 'exit' для отмены): ").strip()
            if x_col.lower() == 'exit':
                return None

            y_col = input("Введите столбец для оси Y: ").strip()

            missing = [col for col in [x_col, y_col] if col not in df.columns]
            if missing:
                print(f"Столбцы не найдены: {', '.join(missing)}")
                continue

            return x_col, y_col

    def _plot_bar_chart(self, df: pd.DataFrame) -> None:
        """Построение столбчатой диаграммы"""
        columns = self._get_valid_columns(df)
        if not columns:
            return

        x_col, y_col = columns

        try:
            with plt.style.context('seaborn'):
                fig, ax = plt.subplots(figsize=(15, 7))

                # Сэмплирование и сортировка данных
                plot_df = self._prepare_data(df, x_col, y_col)

                # Построение графика
                ax.bar(plot_df[x_col], plot_df[y_col], color='skyblue')

                self._configure_plot(ax, x_col, y_col, 'Столбчатая диаграмма')
                plt.tight_layout()
                plt.show()
        finally:
            plt.close(fig)

    def _plot_line_chart(self, df: pd.DataFrame) -> None:
        """Построение линейного графика"""
        columns = self._get_valid_columns(df)
        if not columns:
            return

        x_col, y_col = columns

        try:
            with plt.style.context('seaborn'):
                fig, ax = plt.subplots(figsize=(15, 7))

                # Подготовка данных
                plot_df = self._prepare_data(df, x_col, y_col)

                # Проверка типа данных для оси X
                if not pd.api.types.is_numeric_dtype(plot_df[x_col]):
                    print(f"Предупреждение: столбец '{x_col}' содержит нечисловые данные")

                # Построение графика
                ax.plot(plot_df[x_col], plot_df[y_col],
                       marker='o', linestyle='-', color='green', markersize=5)

                self._configure_plot(ax, x_col, y_col, 'Линейный график')
                plt.tight_layout()
                plt.show()
        finally:
            plt.close(fig)

    def _prepare_data(self, df: pd.DataFrame, x_col: str, y_col: str) -> pd.DataFrame:
        """Подготовка данных для визуализации"""
        # Ограничение количества данных
        sample_size = min(1000, len(df))
        plot_df = df.sample(sample_size) if len(df) > 1000 else df.copy()

        # Сортировка по оси X
        return plot_df.sort_values(by=x_col).reset_index(drop=True)

    def _configure_plot(self, ax: plt.Axes, x_label: str, y_label: str, title: str) -> None:
        """Настройка параметров графика"""
        ax.set_title(f"{title}: {y_label} по {x_label}", fontsize=14)
        ax.set_xlabel(x_label, fontsize=12)
        ax.set_ylabel(y_label, fontsize=12)
        ax.grid(True, linestyle='--', alpha=0.7)
        ax.tick_params(axis='x', rotation=45)
        ax.tick_params(axis='both', labelsize=10)

# Пример использования
if __name__ == "__main__":
    df = pd.DataFrame({
        'Year': [2010, 2011, 2012, 2013, 2014],
        'Sales': [100, 150, 200, 180, 220]
    })

    visualizer = DataFrameVisualizer()
    visualizer.show_visualization_menu(df)
