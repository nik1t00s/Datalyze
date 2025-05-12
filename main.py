"""Главный модуль приложения для анализа медицинских данных.

Содержит класс `MainApplication`, который управляет основным циклом работы:
- Инициализация компонентов
- Отображение меню
- Обработка выбора пользователя

Пример использования:
    if __name__ == "__main__":
        app = MainApplication()

Модули:
    data_importer_exporter: Импорт/экспорт данных.
    data_table_viewer: Просмотр табличных данных.
    data_visualizer: Визуализация данных.
    localization: Локализация строк.
"""

from data_importer_exporter import DataImporterExporter
from localization import Localizer
from data_table_viewer import DataFrameViewer
from data_visualizer import DataFrameVisualizer
import pandas as pd
from neural_network import CancerPredictor
import numpy as np

class MainApplication:
    def __init__(self):
        """Инициализирует главное приложение.

        Создает:
            - Пустой DataFrame для хранения данных
            - Объект локализации
            - Основные компоненты приложения
        """
        self.df = pd.DataFrame()
        self.localizer = Localizer()
        self._init_components()
        self._show_welcome()
        self.run()

    def _init_components(self):
        """Инициализирует основные компоненты приложения.

        Создает:
            - Импортер/экспортер данных
            - Просмотрщик таблиц
            - Визуализатор данных

        Raises:
            SystemExit: Если инициализация не удалась
        """
        try:
            self.importer = DataImporterExporter(self.localizer, self)
            self.table_viewer = DataFrameViewer(self.localizer)
            self.visualizer = DataFrameVisualizer(self.localizer)
        except Exception as e:
            print(f"{self.localizer.get_string(14)}: {str(e)}")
            exit(1)

    def _show_welcome(self):
        """Выводит приветственное сообщение при запуске."""
        print("=" * 50)
        print(self.localizer.get_string(0))
        print(self.localizer.get_string(1))
        print("=" * 50)
        print("\n")

    def run(self):
        """Основной цикл работы приложения.

        Обрабатывает:
            - Отображение меню
            - Ввод пользователя
            - Обработку выбора
            - Критические ошибки
        """
        while True:
            try:
                self._display_main_menu()
                choice = self._get_user_choice()

                if choice == 0:
                    self._exit_application()
                    break

                self._handle_menu_choice(choice)

            except KeyboardInterrupt:
                print(f"\n{self.localizer.get_string(15)}")
                break
            except Exception as e:
                print(f"{self.localizer.get_string(16)}: {str(e)}")

    def _display_main_menu(self):
        """Отображает главное меню с локализованными строками."""
        print(f"\n{self.localizer.get_string(2)}")
        print(f"0 - {self.localizer.get_string(5)}")
        print(f"1 - {self.localizer.get_string(6)}")
        print(f"2 - {self.localizer.get_string(7)}")
        print(f"3 - {self.localizer.get_string(8)}")
        print(f"4 - Прогнозирование с использованием нейронной сети")

    def _get_user_choice(self) -> int:
        """Получает и валидирует выбор пользователя.

        Returns:
            int: Выбранный пункт меню

        Note:
            Повторяет запрос при некорректном вводе
        """
        while True:
            try:
                return int(input(f"{self.localizer.get_string(17)}: "))
            except ValueError:
                print(self.localizer.get_string(9))

    def _handle_menu_choice(self, choice: int):
        """Обрабатывает выбор пункта меню.

        Args:
            choice: Выбранный пункт меню

        Checks:
            - Загружены ли данные для просмотра/визуализации
        """
        handlers = {
            1: self._handle_data_io,
            2: self._show_data_table,
            3: self._show_data_charts,
            4: self._handle_neural_network
        }

        if choice in handlers:
            if choice in [2, 3] and self.df.empty:
                print(self.localizer.get_string(10))
                return

            handlers[choice]()

    def _handle_data_io(self):
        """Обрабатывает операции импорта/экспорта данных.

        Обновляет:
            self.df: Если импорт прошел успешно
        """
        success, new_df = self.importer.show_menu()
        if success:
            self.df = new_df
            print(self.localizer.get_string(11).format(len(self.df)))

    def _show_data_table(self):
        """Запускает просмотр данных в табличном виде."""
        self.table_viewer.show_menu(self.df)

    def _show_data_charts(self):
        """Запускает визуализацию данных."""
        self.visualizer.show_menu(self.df)

    def _handle_neural_network(self):
        """Меню работы с нейронными сетями."""
        print("\n=== Нейронные сети ===")
        print("1. Прогнозирование типа рака")
        print("2. Прогнозирование типа мутации")
        print("3. Прогнозировать на новых данных")
        print("4. Вернуться")

        choice = input("Выберите действие: ")
        if choice == "1":
            self._predict_cancer_type()
        elif choice == "2":
            self._predict_mutation_type()
        elif choice == "3":
            self._predict_new_data()

    def _predict_cancer_type(self):
        """Прогнозирует тип рака."""
        if self.df.empty:
            print("Ошибка: данные не загружены!")
            return
        
        try:
            hidden_layers = tuple(map(int, input("Введите размеры скрытых слоёв через запятую (например, 100,50): ").split(',')))
            activation = input("Введите функцию активации (relu, logistic, tanh): ")
            learning_rate = float(input("Введите скорость обучения (например, 0.001): "))
            
            predictor = CancerPredictor(
                hidden_layer_sizes=hidden_layers,
                activation=activation,
                learning_rate_init=learning_rate
            )
            X_train, X_test, y_train, y_test = predictor.preprocess_data(self.df, "Cancer_Type")
            predictor.train(X_train, y_train)
            accuracy = predictor.evaluate(X_test, y_test)
            print(f"\nТочность модели: {accuracy:.2f}")
            
            predictor.save_model("cancer_model.pkl")
            print("Модель сохранена в cancer_model.pkl")
        except Exception as e:
            print(f"Ошибка: {str(e)}")
    def _predict_mutation_type(self):
        """Прогнозирует тип мутации."""
        if self.df.empty:
            print("Ошибка: данные не загружены!")
            return
        
        if 'Mutation_Type' not in self.df.columns:
            print("Ошибка: столбец 'Mutation_Type' отсутствует в данных!")
            return
        
        try:
            hidden_layers = tuple(map(int, input("Введите размеры скрытых слоёв через запятую (например, 100,50): ").split(',')))
            activation = input("Введите функцию активации (relu, logistic, tanh): ")
            learning_rate = float(input("Введите скорость обучения (например, 0.001): "))
            
            predictor = CancerPredictor(
                hidden_layer_sizes=hidden_layers,
                activation=activation,
                learning_rate_init=learning_rate
            )
            X_train, X_test, y_train, y_test = predictor.preprocess_data(
                self.df, 
                target_column='Mutation_Type'  # Указываем целевую переменную
            )
            predictor.train(X_train, y_train)
            accuracy = predictor.evaluate(X_test, y_test)
            print(f"\nТочность модели: {accuracy:.2f}")
            
            predictor.save_model("mutation_model.pkl")
            print("Модель сохранена в mutation_model.pkl")
        except Exception as e:
            print(f"Ошибка: {str(e)}")


    def _predict_new_data(self):
        if self.df.empty:
            print("Ошибка: данные не загружены!")
            return
        
        try:
            new_data = {}
            valid_columns = [col for col in self.df.columns 
            if col not in ['Cancer_Type', 'Mutation_Type']]  # Исключаем только целевые
            
            print("\nВведите значения признаков:")
            
            for column in valid_columns:
                dtype = self.df[column].dtype
                
                while True:
                    try:
                        value = input(f"{column} ({dtype}): ")
                        
                        # Обработка числовых признаков
                        if np.issubdtype(dtype, np.number):
                            converted_value = float(value) if '.' in value else int(value)
                            new_data[column] = [converted_value]
                        # Обработка категориальных признаков
                        else:
                            unique_values = list(map(str, self.df[column].unique()))
                            if value not in unique_values:
                                print(f"Допустимые значения: {', '.join(unique_values)}")
                                continue
                            new_data[column] = [value]
                        break
                    except ValueError:
                        print(f"Некорректный формат для {column}. Попробуйте снова.")

            # Создаем DataFrame только с необходимыми столбцами
            new_df = pd.DataFrame(new_data)[valid_columns]
            # Приводим типы данных
            for col in valid_columns:
                new_df[col] = new_df[col].astype(self.df[col].dtype)
            
            # Загрузка модели
            predictor = CancerPredictor.load_model("cancer_model.pkl")
            
            # Предобработка данных
            X_processed, _ = predictor.preprocess_data(new_df)
            
            # Прогнозирование
            cancer_proba = predictor.model.predict_proba(X_processed)
            
            # Аналогично для мутаций
            mutation_predictor = CancerPredictor.load_model("mutation_model.pkl")
            X_mut_processed, _ = mutation_predictor.preprocess_data(new_df)
            mutation_proba = mutation_predictor.model.predict_proba(X_mut_processed)
            
            # Добавление новых данных
            self.df = pd.concat([self.df, new_df], ignore_index=True)
            
            # Вывод результатов
            print("\nРезультаты прогноза:")
            print("Вероятности типов рака:")
            for cls, prob in zip(cancer_proba.label_encoder.classes_, cancer_proba[0]):
                print(f"- {cls}: {prob:.2%}")
                
            print("\nВероятности типов мутации:")
            for cls, prob in zip(mutation_proba.label_encoder.classes_, mutation_proba[0]):
                print(f"- {cls}: {prob:.2%}")

        except Exception as e:
            print(f"Ошибка прогнозирования: {str(e)}")
            if 'new_df' in locals() and not new_df.empty:
                self.df = self.df[:-len(new_df)]

    def _exit_application(self):
        """Выводит сообщение о завершении работы."""
        print(f"\n{self.localizer.get_string(12)}")
        print(self.localizer.get_string(13))


if __name__ == "__main__":
    app = MainApplication()
