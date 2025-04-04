import pandas as pd
from pathlib import Path
from kaggle.api.kaggle_api_extended import KaggleApi

class ImportOrExportData:
    EXPECTED_COLUMNS = [
        "Country", "Age", "Gender", "Smoking_Status", "Second_Hand_Smoke",
        "Air_Pollution_Exposure", "Occupation_Exposure", "Rural_or_Urban",
        "Socioeconomic_Status", "Healthcare_Access", "Insurance_Coverage",
        "Screening_Availability", "Stage_at_Diagnosis", "Cancer_Type",
        "Mutation_Type", "Treatment_Access", "Clinical_Trial_Access",
        "Language_Barrier", "Mortality_Risk", "5_Year_Survival_Probability",
        "Delay_in_Diagnosis", "Family_History", "Indoor_Smoke_Exposure",
        "Tobacco_Marketing_Exposure", "Final_Prediction"
    ]

    def import_export_menu(self, has_df: bool, df: pd.DataFrame) -> tuple[bool, pd.DataFrame]:
        print("\nМеню импорта/экспорта данных:")
        print("1 - Импорт с локального диска")
        print("2 - Импорт с Kaggle")
        print("3 - Экспорт данных")

        try:
            choice = int(input("Выберите действие: "))
        except ValueError:
            print("Ошибка: введите число от 1 до 3")
            return has_df, df

        if choice == 1:
            return self._read_local_file()
        elif choice == 2:
            return self._handle_kaggle_import()
        elif choice == 3:
            return self._export_data(has_df, df)
        else:
            print("Неверный выбор")
            return has_df, df

    def _read_local_file(self) -> tuple[bool, pd.DataFrame]:
        path = input("Путь к файлу (csv/xlsx): ").strip()
        file_path = Path(path)

        if not file_path.exists():
            print(f"Ошибка: файл {file_path} не найден")
            return False, None

        try:
            if file_path.suffix == '.csv':
                df = pd.read_csv(file_path)
            elif file_path.suffix in ('.xlsx', '.xls'):
                df = pd.read_excel(file_path)
            else:
                print("Формат не поддерживается")
                return False, None
        except Exception as e:
            print(f"Ошибка чтения файла: {e}")
            return False, None

        if not set(self.EXPECTED_COLUMNS).issubset(df.columns):
            print("Ошибка: отсутствуют необходимые столбцы")
            return False, None

        print("Данные успешно загружены!")
        return True, df

    def _handle_kaggle_import(self) -> tuple[bool, pd.DataFrame]:
        if not self._check_kaggle_setup():
            self._show_kaggle_instructions()
            return False, None

        dataset_url = input("Введите URL датасета Kaggle: ").strip()
        try:
            dataset_slug = dataset_url.split("/datasets/")[-1]
            username, dataset_name = dataset_slug.split("/")[:2]
        except Exception:
            print("Неверный формат URL")
            return False, None

        try:
            api = KaggleApi()
            api.authenticate()
            api.dataset_download_files(f"{username}/{dataset_name}", path=".", unzip=True)

            # Поиск первого CSV файла в текущей директории
            for file in Path('.').iterdir():
                if file.suffix == '.csv':
                    df = pd.read_csv(file)

                    if not set(self.EXPECTED_COLUMNS).issubset(df.columns):
                        print("Ошибка: в данных отсутствуют необходимые столбцы")
                        return False, None

                    print("Данные успешно загружены с Kaggle!")
                    return True, df

            print("CSV файл не найден в датасете")
            return False, None

        except Exception as e:
            print(f"Ошибка загрузки с Kaggle: {e}")
            return False, None

    def _export_data(self, has_df: bool, df: pd.DataFrame) -> tuple[bool, pd.DataFrame]:
        if not has_df:
            print("Нет данных для экспорта")
            return False, None

        path = input("Путь для сохранения: ").strip()
        filename = input("Имя файла (без расширения): ").strip()
        file_format = input("Формат (csv/xlsx): ").lower().strip()

        if file_format not in ('csv', 'xlsx'):
            print("Неверный формат")
            return has_df, df

        export_path = Path(path) / f"{filename}.{file_format}"
        export_path.parent.mkdir(parents=True, exist_ok=True)

        try:
            if file_format == 'csv':
                df.to_csv(export_path, index=False)
            else:
                df.to_excel(export_path, index=False, engine='openpyxl')

            print(f"Файл сохранен: {export_path}")
            return has_df, df

        except Exception as e:
            print(f"Ошибка сохранения: {e}")
            return has_df, df

    def _check_kaggle_setup(self) -> bool:
        kaggle_dir = Path.home() / ".kaggle"
        config_file = kaggle_dir / "kaggle.json"

        if not config_file.exists():
            print("Kaggle API не настроен!")
            return False

        try:
            KaggleApi().authenticate()
            return True
        except Exception as e:
            print(f"Ошибка аутентификации: {e}")
            return False

    def _show_kaggle_instructions(self) -> None:
        print("\nИнструкция по настройке Kaggle API:")
        print("1. Зарегистрируйтесь на kaggle.com")
        print("2. В настройках аккаунта создайте API токен")
        print("3. Поместите файл kaggle.json в папку:")
        print(f"   {Path.home() / '.kaggle'}")
