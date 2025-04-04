import pandas as pd

import pandas as pd


class DF_reader_table:

    def DF_reader_table_menu(self, df):
        print("Меню табличной визуализации, выберите следющий шаг:")
        print("1 - Вывод всех данных")
        print("2 - Вывод данных с условием")
        try:
            choose_menu = int(input())
        except ValueError:
            print("Ошибка ввода")
            return
        if (choose_menu == 1):
            self.__OUT_dataframe(df)
        if (choose_menu == 2):
            self.__OUT_with_filter_dataframe(df)

    def __OUT_dataframe(self, df):
        print("Вывод всех данных")
        print(df)

    def __OUT_with_filter_dataframe(self, df):
        print("Вывод данных с условием")
        print("В программе представленны 4 условия:")
        print("Вывод запись от i до j")
        print("Вывод определённых столбцов")
        print("Вывод отстортированные по столбцу")
        print("Вывод данных с фильтром на столбце, на равенство")

        try:
            # Получение диапазона индексов
            start_index = int(input("Введите начальный индекс (i): "))
            end_index = int(input("Введите конечный индекс (j): "))
            filtered_df = df.iloc[start_index:end_index]

            print("Доступные столбцы:")
            print(df.columns.tolist())
            # Получение имен столбцов для вывода
            columns_input = input("Введите названия столбцов через запятую (или оставьте пустым, чтобы вывести все): ")
            if columns_input:
                columns = [col.strip() for col in columns_input.split(',')]
                filtered_df = filtered_df[columns]

            # Сортировка по столбцу
            sort_column = input("Введите название столбца для сортировки (или оставьте пустым, чтобы не сортировать): ")
            if sort_column and sort_column in filtered_df.columns:
                filtered_df = filtered_df.sort_values(by=sort_column)
            elif sort_column:
                print(f"Столбец '{sort_column}' не найден.")

            # Фильтрация по значению в столбце
            filter_column = input("Введите название столбца для фильтрации (или оставьте пустым, чтобы не фильтровать): ")
            if filter_column and filter_column in filtered_df.columns:
                filter_value = input(f"Введите значение для фильтрации в столбце '{filter_column}': ")
                filtered_df = filtered_df[filtered_df[filter_column] == filter_value]
            elif filter_column:
                print(f"Столбец '{filter_column}' не найден.")

            print("Результат фильтрации:")
            print(filtered_df)
        except Exception as e:
            print("Ошибка настройки фильтров")
            return
