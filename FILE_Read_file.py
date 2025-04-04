import pandas as pd
import os
from kaggle.api.kaggle_api_extended import KaggleApi



class Import_or_export_data:


    def Import_or_export_data_menu(self, have_df, df):
        print("Меню импорта и экспорта данных, выберите следющий шаг:")
        print("1 - Импорт с диска")
        print("2 - Импорт с онлайн ресурса Kaggle API")
        print("3 - Экспорт данных на диск")
        try:
            choose_menu = int(input())
        except ValueError:
            print("Ошибка ввода")
            return

        #choose_menu = 2

        if (choose_menu == 1):
            have_df_new, df_new = self.__Read_file_from_disk()
            if (have_df_new == False):
                return have_df, df
            else:
                return have_df_new, df_new

        if (choose_menu == 2):
            if (self.__Сheck_kaggle_api_setup() == False):
                self.__Instruction_for_create_kaggle_api()
                return have_df, df
            have_df_new, df_new = self.__Read_file_from_Kaggle()
            if (have_df_new == False):
                return have_df, df
            else:
                return have_df_new, df_new


        if (choose_menu == 3):
            if (have_df == False):
                print("данные не выбраны")
                return have_df, df
            else:
                self.__Write_file_from_disk(df)
                return have_df, df
        return



    #------------------------------------------------------------------------------------------
    # Функция чтения файла, с учётом его проверки
    def __Read_file_from_disk(self):
        print("Введите путь к папке с файло с данными. Данные в формате csv или xls")
        #path = input().strip()
        path = r"C:\Users\aleks\Desktop\Системная и програмная инженерия\Проект_по_СиПИ"
        print("Введите полное имя файла с данными")
        #name_file = input().strip()
        name_file = "lung_cancer_prediction.csv"
        # Создание обсолютного пути
        file_path = os.path.join(path, name_file)

        # Проверка наличия файла
        if not os.path.isfile(file_path):
            print("Файл '{file}' не найден.")
            return False, ""

        # Определение формата файла
        file_extension = os.path.splitext(name_file)[1].lower()

        # Начало отслеживания ошибки чтения файла
        try:
            # Читаем файл с учётом формата
            if file_extension == '.csv':
                df = pd.read_csv(file_path)
            elif file_extension in ['.xls', '.xlsx']:
                df = pd.read_excel(file_path)
            else:
                print("Указанный формат файла не поддерживается системой. Пожалуйста, прдоставьте CSV или Excel файл.")
                return False, ""

            # Столбцы, которые ожидаются
            expected_columns = [
                "Country", "Age", "Gender", "Smoking_Status", "Second_Hand_Smoke",
                "Air_Pollution_Exposure", "Occupation_Exposure", "Rural_or_Urban",
                "Socioeconomic_Status", "Healthcare_Access", "Insurance_Coverage",
                "Screening_Availability", "Stage_at_Diagnosis", "Cancer_Type",
                "Mutation_Type", "Treatment_Access", "Clinical_Trial_Access",
                "Language_Barrier", "Mortality_Risk", "5_Year_Survival_Probability",
                "Delay_in_Diagnosis", "Family_History", "Indoor_Smoke_Exposure",
                "Tobacco_Marketing_Exposure", "Final_Prediction"
            ]

            # Проверка наличия столбцов
            if list(df.columns) != expected_columns:
                print("Ошибка: требуемые столбцы не найдены")
                return False, ""

            # Данные прочитаны
            print("Файл найден и прочитан")
            return True, df

        except Exception as e:
            print("Ошибка чтения файла")
            return False, ""

# ------------------------------------------------------------------------------------------
    # Инструкция создания Kaggle API
    def __Instruction_for_create_kaggle_api(self):
        print("Ниже приведена инструкция, по получению Kaggle.api")
        print("1) Заригистрируйтесь на сайте")
        print("2) Зайдите в настройки аккаунта")
        print("3) Прокрутите настройки до пункат API и выберите 'Create new token'")
        print("4) Перенисите скачанный файл json в следующую папку:")
        print(r"C:\Users\users_name\.kaggle")

    # Функция проверки Kaggle API
    def __Сheck_kaggle_api_setup(self):
        # Путь к файлу Kaggle API на Windows
        kaggle_config_path = os.path.join(os.environ['USERPROFILE'], '.kaggle', 'kaggle.json')
        # Проверка сущиствования файла
        if not os.path.isfile(kaggle_config_path):
            print(f"Файл {kaggle_config_path} не найден. Убедитесь, что Kaggle API установлен и настроен.")
            return False

        try:
            # Проверка аутентифицироваться с помощью Kaggle API
            api = KaggleApi()
            api.authenticate()
            print("Kaggle API настроен правильно. Аутентификация прошла успешно.")
            return True
        except Exception as e:
            print(f"Ошибка при аутентификации с Kaggle API: {e}")
            return False

    # Функция чтения файла с электронного ресурса Kaggle
    def __Read_file_from_Kaggle(self):
        # Ссылка на набор данных
        # dataset_url = input().strip()
        dataset_url = "https://www.kaggle.com/datasets/ankushpanday1/lung-cancer-risk-and-prediction-dataset"

        # Извлекаем имя пользователя и название датасета из URL
        dataset_parts = dataset_url.split('/')
        if len(dataset_parts) != 6:
            print("Некорректный URL")
            return False, ""
        username = dataset_parts[len(dataset_parts) - 2]
        dataset_name = dataset_parts[len(dataset_parts) - 1]

        # Аутентификация с Kaggle API
        api = KaggleApi()
        api.authenticate()

        # Проверка доступности датасета
        try:
            api.dataset_download_files(f"{username}/{dataset_name}", path=".", unzip=True)
        except Exception as e:
            print("Ошибка в нименовании датасета или пользователя его выложевшего")
            return False, ""

        # Загрузка датасета
        try:
            # Поиск загруженного CSV файла
            csv_file = [f for f in os.listdir('.') if f.endswith('.csv')][0]
            # Чтение данных в DataFrame
            df = pd.read_csv(csv_file)
            return True, df
        except Exception as e:
            print("Ошибка при загрузке датасета")
            return False, ""

# ------------------------------------------------------------------------------------------
    # Инструкция создания Kaggle API
    def __Instruction_for_create_kaggle_api(self):
        print("Ниже приведена инструкция, по получению Kaggle.api")
        print("1) Заригистрируйтесь на сайте")
        print("2) Зайдите в настройки аккаунта")
        print("3) Прокрутите настройки до пункат API и выберите 'Create new token'")
        print("4) Перенисите скачанный файл json в следующую папку:")
        print(r"C:\Users\users_name\.kaggle")

    # Функция проверки Kaggle API
    def __Сheck_kaggle_api_setup(self):
        # Путь к файлу Kaggle API на Windows
        kaggle_config_path = os.path.join(os.environ['USERPROFILE'], '.kaggle', 'kaggle.json')
        # Проверка сущиствования файла
        if not os.path.isfile(kaggle_config_path):
            print(f"Файл {kaggle_config_path} не найден. Убедитесь, что Kaggle API установлен и настроен.")
            return False

        try:
            # Проверка аутентифицироваться с помощью Kaggle API
            api = KaggleApi()
            api.authenticate()
            print("Kaggle API настроен правильно. Аутентификация прошла успешно.")
            return True
        except Exception as e:
            print(f"Ошибка при аутентификации с Kaggle API: {e}")
            return False

    def __Read_file_from_Kaggle(self):
        # Ссылка на набор данных
        # dataset_url = input().strip()
        dataset_url = "https://www.kaggle.com/datasets/ankushpanday1/lung-cancer-risk-and-prediction-dataset"

        # Извлекаем имя пользователя и название датасета из URL
        dataset_parts = dataset_url.split('/')
        if len(dataset_parts) != 6:
            print("Некорректный URL")
            return False, ""
        username = dataset_parts[len(dataset_parts) - 2]
        dataset_name = dataset_parts[len(dataset_parts) - 1]

        # Аутентификация с Kaggle API
        api = KaggleApi()
        api.authenticate()

        # Проверка доступности датасета
        try:
            api.dataset_download_files(f"{username}/{dataset_name}", path=".", unzip=True)
        except Exception as e:
            print("Ошибка в нименовании датасета или пользователя его выложевшего")
            return False, ""

        # Загрузка датасета
        try:
            # Поиск загруженного CSV файла
            csv_file = [f for f in os.listdir('.') if f.endswith('.csv')][0]
            # Чтение данных в DataFrame
            df = pd.read_csv(csv_file)
            return True, df
        except Exception as e:
            print("Ошибка при загрузке датасета")
            return False, ""

# ------------------------------------------------------------------------------------------
    # Функция чтения файла, с учётом его проверки
    def __Write_file_from_disk(self, df):
        print("Введите путь к папке куда сохранить данные")
        # path = input().strip()
        path = r"C:\Users\aleks\Desktop\Системная и програмная инженерия\Проект_по_СиПИ"
        print("Введите имя файла")
        # name_file = input().strip()
        name_file = "test_save_df"
        print("Введите формат файла для сохранения")
        #format_file = .strip().lower()
        format_file = "csv"

        # Проверяем формата
        if format_file not in ['csv', 'xls']:
            print("Ошибка формат не поддерживается")
            return ""

        # Создание обсолютного пути
        file_path = os.path.join(path, f"{name_file}.{format_file}")
        # Отслеживание ошибок
        try:
            # Сохраняем DataFrame в нужном формате
            if format_file == 'csv':
                df.to_csv(file_path, index=False, encoding='utf-8')
            elif format_file == 'xls':
                df.to_excel(file_path, index=False, engine='openpyxl')

            print(f"Файл успешно сохранён как: {file_path}")
            return 0
        except Exception as e:
            print(f"Произошла ошибка при сохранении файла: {e}")
            return ""



