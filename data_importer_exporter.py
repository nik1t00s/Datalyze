import pandas as pd
from pathlib import Path
import requests
import zipfile
from io import BytesIO
from typing import Tuple
from kaggle.api.kaggle_api_extended import KaggleApi


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
        ppath = input(f"{self.localizer.get_string(21)} (с именем файла): ").strip()
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

    def __kaggle_import(self) -> Tuple[bool, pd.DataFrame]:
        print(f"\n{self.localizer.get_string(26)}")
        print(f"{self.localizer.get_string(27)}\n")
    
        dataset_url = input(f"{self.localizer.get_string(28)}: ").strip()
    
        try:
            api = KaggleApi()
            api.authenticate()
        
            # Извлечение информации из URL
            parts = dataset_url.split('/')
            dataset_name = parts[-1]
            user = parts[-2]
        
            # Скачивание датасета
            print(self.localizer.get_string(30))
            api.dataset_download_files(f"{user}/{dataset_name}", path="temp", unzip=True)
        
            # Поиск CSV файла
            csv_files = list(Path("temp").glob("*.csv"))
            if not csv_files:
                print(self.localizer.get_string(31))
                return False, pd.DataFrame()
        
            df = pd.read_csv(csv_files[0])
        
            if self._validate_columns(df):
                print(self.localizer.get_string(32))
                return True, df
            return False, pd.DataFrame()
        except Exception as e:
            print(f"{self.localizer.get_string(33)}: {str(e)}")
            return False, pd.DataFrame()

    def _export_data(self) -> Tuple[bool, pd.DataFrame]:
        if self.df.empty:
            print(self.localizer.get_string(10))
            return False, self.df
        
        path = input(f"{self.localizer.get_string(34)}: ").strip()
        filename = input(f"{self.localizer.get_string(35)}: ").strip()
        file_format = input(f"{self.localizer.get_string(36)}: ").lower().strip()
        
        export_path = Path(path) / f"{filename}.{file_format}"
        export_path.parent.mkdir(parents=True, exist_ok=True)
        
        try:
            if file_format == "csv":
                self.df.to_csv(export_path, index=False)
            elif file_format == "xlsx":
                self.df.to_excel(export_path, index=False, engine="openpyxl")
            else:
                print(self.localizer.get_string(37))
                return False, self.df
            
            print(self.localizer.get_string(38).format(export_path))
            return True, self.df
        except Exception as e:
            print(f"{self.localizer.get_string(39)}: {str(e)}")
            return False, self.df

    def _validate_columns(self, df: pd.DataFrame) -> bool:
        """Проверка структуры данных"""
        missing = set(self.EXPECTED_COLUMNS) - set(df.columns)
        if missing:
            print(self.localizer.get_string(40).format(", ".join(missing)))
            return False
        return True
