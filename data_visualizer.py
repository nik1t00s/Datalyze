import matplotlib.pyplot as plt
import pandas as pd
import matplotlib as mpl

mpl.rcParams['agg.path.chunksize'] = 10000

class DataFrameVisualizer:
    def __init__(self, localizer):
        self.localizer = localizer

    def show_menu(self, df: pd.DataFrame):
        while True:
            print(f"\n{self.localizer.get_string(48)}")
            print("1. Bar chart")  # Можно заменить на локализованное
            print("2. Line chart")
            print("3. " + self.localizer.get_string(5))
            try:
                choice = int(input(f"{self.localizer.get_string(17)}: "))
                if choice == 1:
                    self._plot_chart(df, "bar")
                elif choice == 2:
                    self._plot_chart(df, "line")
                else:
                    return
            except ValueError:
                print(self.localizer.get_string(9))

    def _plot_chart(self, df: pd.DataFrame, chart_type: str):
        print(f"\n{self.localizer.get_string(69)}: {', '.join(df.columns)}")
        try:
            x_col = input(f"{self.localizer.get_string(49)}: ").strip()
            y_col = input(f"{self.localizer.get_string(50)}: ").strip()
            if x_col not in df.columns or y_col not in df.columns:
                print(self.localizer.get_string(51))
                return

            if chart_type == "line":
                if not pd.api.types.is_numeric_dtype(df[y_col]):
                    print(self.localizer.get_string(53))
                    return
                if len(df) > 200:
                    print(self.localizer.get_string(70))
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