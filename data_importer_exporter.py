import pandas as pd
from pathlib import Path
import requests
import zipfile
from io import BytesIO
from typing import Tuple

class DataImporterExporter:
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

    def __init__(self, localizer):
        self.localizer = localizer

    def show_menu(self) -> Tuple[bool, pd.DataFrame]:
        """Меню импорта/экспорта"""
        print(f"\n{self.localizer.get_string(20)}")
        print("1. Импорт с локального диска")
        print("2. Импорт с Kaggle")
        print("3. Экспорт данных")
        print("4. Вернуться")

        try:
            choice = int(input("Выберите действие: "))
            if choice == 1:
                return self._local_import()
            elif choice == 2:
                return self._kaggle_import()
            elif choice == 3:
                return self._export_data()
            else:
                return False, pd.DataFrame()
        except ValueError:
            print(self.localizer.get_string(9))
            return False, pd.DataFrame()

    def _local_import(self) -> Tuple[bool, pd.DataFrame]:
        """Локальный импорт данных"""
        path = input(f"{self.localizer.get_string(21)}: ").strip()
        file_path = Path(path)

        if not file_path.exists():
            print(self.localizer.get_string(22).format(file_path))
            return False, pd.DataFrame()

        try:
            if file_path.suffix == '.csv':
                df = pd.read_csv(file_path)
            elif file_path.suffix in ('.xlsx', '.xls'):
                df = pd.read_excel(file_path)
            else:
                print(self.localizer.get_string(23))
                return False, pd.DataFrame()

            if self._validate_columns(df):
                print(self.localizer.get_string(24))
                return True, df
            return False, pd.DataFrame()

        except Exception as e:
            print(f"{self.localizer.get_string(25)}: {str(e)}")
            return False, pd.DataFrame()

    def _kaggle_import(self) -> Tuple[bool, pd.DataFrame]:
        """Импорт данных с Kaggle"""
        print(f"\n{self.localizer.get_string(26)}")
        print(f"{self.localizer.get_string(27)}\n")

        dataset_url = input(f"{self.localizer.get_string(28)}: ").strip()

        try:
            # Извлечение информации из URL
            parts = [p for p in dataset_url.strip("/").split("/") if p]
            if len(parts) < 5 or parts[2] != "datasets":
                raise ValueError(self.localizer.get_string(29))

            username = parts[3]
            dataset_name = parts[4]
            download_url = f"https://www.kaggle.com/{username}/{dataset_name}/download"

            # Загрузка данных
            print(self.localizer.get_string(30))
            response = requests.get(download_url, stream=True, timeout=15)
            response.raise_for_status()

            # Обработка архива
            with zipfile.ZipFile(BytesIO(response.content)) as zip_file:
                csv_files = [f for f in zip_file.namelist() if f.endswith(".csv")]
                if not csv_files:
                    print(self.localizer.get_string(31))
                    return False, pd.DataFrame()

                with zip_file.open(csv_files[0]) as csv_file:
                    df = pd.read_csv(csv_file)

            if self._validate_columns(df):
                print(self.localizer.get_string(32))
                return True, df
            return False, pd.DataFrame()

        except Exception as e:
            print(f"{self.localizer.get_string(33)}: {str(e)}")
            return False, pd.DataFrame()

    def _export_data(self) -> Tuple[bool, pd.DataFrame]:
        """Экспорт данных"""
        path = input(f"{self.localizer.get_string(34)}: ").strip()
        filename = input(f"{self.localizer.get_string(35)}: ").strip()
        file_format = input(f"{self.localizer.get_string(36)}: ").lower().strip()

        if file_format not in ("csv", "xlsx"):
            print(self.localizer.get_string(37))
            return False, pd.DataFrame()

        export_path = Path(path) / f"{filename}.{file_format}"
        export_path.parent.mkdir(parents=True, exist_ok=True)

        try:
            if file_format == "csv":
                pd.DataFrame.to_csv(export_path, index=False)
            else:
                pd.DataFrame.to_excel(export_path, index=False, engine="openpyxl")

            print(self.localizer.get_string(38).format(export_path))
            return True, pd.DataFrame()
        except Exception as e:
            print(f"{self.localizer.get_string(39)}: {str(e)}")
            return False, pd.DataFrame()

    def _validate_columns(self, df: pd.DataFrame) -> bool:
        """Проверка структуры данных"""
        missing = set(self.EXPECTED_COLUMNS) - set(df.columns)
        if missing:
            print(self.localizer.get_string(40).format(", ".join(missing)))
            return False
        return True
