# Импорт файлов с классами для работы

from FILE_Read_file import Import_or_export_data
from FILE_localization import Localization
from FILE_df_reader_table import DF_reader_table
from File_df_reader_charts import DF_reader_table_charts

class main():
    have_df = False
    df = ""
    localisation_file = ""



    def __init__(self):
        print("START")
        print("Приветствум вас в нашей программе по работе с данными по раковым заболиваниям.")
        print("Программа создана в качестве проектной работы по СиПИ.")
        print("Авторы программы:")
        print("Соколов А.В.")
        print("Кожемякин А.А.")
        print("Шиханова Е.В.")
        print("Чайка Н.В.")
        print("\n\n")

        # Выбор локализации
        self.localisation_file = Localization()

        # Переход в меню
        self.Program_menu()

    def Program_menu(self):
        if (self.have_df == False):
            print("Обноруженна ошибка, данные не выбраны!")
        while(True):
            print("Вы находитесь в меню, выберите следующий шаг:")
            print("0 - Выход")
            print("1 - Импор или экспорт данных")
            print("2 - Вывод данных ввиде таблицы")
            print("3 - Вывод данных ввиде графиков")
            try:
                choose_menu = int(input())
            except ValueError:
                choose_menu
                print("Ошибка ввода")
            #choose_menu = 1
            if (choose_menu == 1):
                reder_files = Import_or_export_data()
                self.have_df, self.df = reder_files.Import_or_export_data_menu(self.have_df, self.df)
                #print(self.df)
            if (choose_menu == 2) and (self.have_df):
                DF_reader_table().DF_reader_table_menu(self.df)
            if (choose_menu == 3) and (self.have_df):
                DF_reader_table_charts().DF_reader_table_charts_menu(self.df)
            if (choose_menu == 0):
                break
        return 0












START_PROGRAM = main()






print("\n\nFINISH")
print("")