import matplotlib.pyplot as plt

class DF_reader_table_charts:

    def DF_reader_table_charts_menu(self, df):
        print("Выберите способ визуализации:")
        print("1: Столбчатая диаграмма")
        print("2: Линейная диаграмма")
        choice = int(input())
        if choice == 1:
            self.Bar_chart(df)
        elif choice == 2:
            self.Line_chart(df)

    def Bar_chart(self, df):
        print("Доступные столбцы:")
        print(df.columns.tolist())
        x_column = input("Введите название столбца для оси X: ")
        y_column = input("Введите название столбца для оси Y: ")

        if x_column in df.columns and y_column in df.columns:
            # Вследствии ошибки избыточности данных возмём срез
            df_sample = df.sample(min(100, len(df))).sort_values(by=x_column)
            plt.figure(figsize=(15, 7))
            plt.bar(df_sample[x_column], df_sample[y_column])  # Используем plt.bar() для построения столбцов
            plt.title(f'Столбчатая диаграмма: {y_column} по {x_column}')
            plt.ylabel(y_column)
            plt.xlabel(x_column)
            plt.xticks(rotation=45)  # Поворачиваем метки на оси X для лучшей читаемости
            plt.grid(axis='y')  # Добавляем сетку для оси Y
            plt.show()
        return

    def Line_chart(self, df):
        x_column = input("Введите название столбца для оси X: ")
        y_column = input("Введите название столбца для оси Y: ")

        if x_column in df.columns and y_column in df.columns:
            # Вследствии ошибки избыточности данных возмём срез
            df_sample = df.sample(min(100, len(df))).sort_values(by=x_column)
            plt.figure(figsize=(15, 7))
            plt.plot(df_sample[x_column], df_sample[y_column])
            #df_sample.plot(kind='line', x=x_column, y=y_column)
            plt.title(f'Линейная диаграмма: {y_column} по {x_column}')
            plt.ylabel(y_column)
            plt.xlabel(x_column)
            plt.grid(True)  # Добавляем сетку для улучшения читаемости графика
            plt.show()
        return