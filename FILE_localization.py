



class Localization:
    path_for_local = ""
    RU_local = r"files_for_the_project\localization\RU.txt"

    # Функция выбора локализации
    def __init__(self):
        print("Choose the localization:")
        print("1 - RU")

        #choose_local = input()
        choose_local = 1
        if (choose_local == 1):
            self.path_for_local = self.RU_local
        else:
            print("Error loacal")
        print(self.Read_loacl_file(0))

    # Функция чтения x строки из файла локализации
    def Read_loacl_file(self, line_number):
        # Отслеживание ошибок
        try:
            # Открытие и чтение файла
            with open(self.path_for_local, 'r', encoding='utf-8') as file:
                lines = file.readlines()
                if line_number < 0 or line_number >= len(lines):
                    return "Ошибка: номер строки вне диапазона."
                return lines[line_number].rstrip()  # Удаляем символы новой строки
        except FileNotFoundError:
            return "Ошибка: файл не найден."
        except Exception as e:
            return f"Произошла ошибка: {e}"



