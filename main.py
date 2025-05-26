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
import os

class MainApplication:
    def __init__(self):
        """Инициализирует главное приложение.

        Создает:
            - Пустой DataFrame для хранения данных
            - Объект локализации
            - Основные компоненты приложения
        """
        self.df = pd.DataFrame()  # Initialize empty DataFrame
        self.localizer = Localizer()
        self._offer_language_switch()
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

    def _offer_language_switch(self):
        """Предлагает пользователю сменить язык интерфейса.
        
        Использует двуязычный интерфейс для облегчения выбора
        независимо от текущего языка системы.
        """
        print(f"\n=== Language / Язык ===")
        print(f"Detected system language / Определен язык системы: {self.localizer.language}")
        choice = input("Change language? / Сменить язык? (y/д/н/n): ").lower()
        if choice in ["y", "д"]:
            self.localizer.select_language()

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
        print(f"4 - {self.localizer.get_string(201)}")

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
        print(f"\n=== {self.localizer.get_string(200)} ===")
        print(f"1. {self.localizer.get_string(202)}")
        print(f"2. {self.localizer.get_string(203)}")
        print(f"3. {self.localizer.get_string(221)}")  # Mortality risk prediction
        print(f"4. {self.localizer.get_string(204)}")
        print(f"5. {self.localizer.get_string(205)}")

        choice = input(f"{self.localizer.get_string(206)}: ")
        if choice == "1":
            self._predict_cancer_type()
        elif choice == "2":
            self._predict_mutation_type()
        elif choice == "3":
            self._predict_mortality_risk()
        elif choice == "4":
            self._predict_new_data()

    def _predict_cancer_type(self):
        """Прогнозирует тип рака."""
        if self.df.empty:
            print(f"{self.localizer.get_string(212)}")
            return
        
        try:
            print(f"\n{self.localizer.get_string(222)}")  # Creating and training cancer type model...
            
            try:
                hidden_layers = tuple(map(int, input(f"{self.localizer.get_string(207)}: ").split(',')))
            except ValueError:
                print("Invalid hidden layer format. Please enter comma-separated integers.")
                return
                
            activation = input(f"{self.localizer.get_string(208)}: ")
            activation = self._validate_activation(activation)
            if not activation:
                return
                
            learning_rate_input = input(f"{self.localizer.get_string(209)}: ")
            learning_rate = self._validate_learning_rate(learning_rate_input)
            if learning_rate is None:
                return
            
            predictor = CancerPredictor(
                hidden_layer_sizes=hidden_layers,
                activation=activation,
                learning_rate_init=learning_rate
            )
            X_train, X_test, y_train, y_test = predictor.preprocess_data(self.df, "Cancer_Type")
            predictor.train(X_train, y_train)
            accuracy = predictor.evaluate(X_test, y_test)
            print(f"\n{self.localizer.get_string(210)}: {accuracy:.2f}")
            
            model_file = "cancer_model.pkl"
            predictor.save_model(model_file)
            print(self.localizer.get_string(211).format(model_file))
        except Exception as e:
            print(f"{self.localizer.get_string(220)}: {str(e)}")
    def _predict_mutation_type(self):
        """Прогнозирует тип мутации."""
        if self.df.empty:
            print(f"{self.localizer.get_string(212)}")
            return
        
        target_column = 'Mutation_Type'
        if target_column not in self.df.columns:
            print(self.localizer.get_string(213).format(target_column))
            return
        
        try:
            print(f"\n{self.localizer.get_string(223)}")  # Creating and training mutation type model...
            
            try:
                hidden_layers = tuple(map(int, input(f"{self.localizer.get_string(207)}: ").split(',')))
            except ValueError:
                print("Invalid hidden layer format. Please enter comma-separated integers.")
                return
                
            activation = input(f"{self.localizer.get_string(208)}: ")
            activation = self._validate_activation(activation)
            if not activation:
                return
                
            learning_rate_input = input(f"{self.localizer.get_string(209)}: ")
            learning_rate = self._validate_learning_rate(learning_rate_input)
            if learning_rate is None:
                return
            
            predictor = CancerPredictor(
                hidden_layer_sizes=hidden_layers,
                activation=activation,
                learning_rate_init=learning_rate
            )
            self.df = self.df.dropna(subset=[target_column])
            X_train, X_test, y_train, y_test = predictor.preprocess_data(
                self.df, 
                target_column=target_column
            )
            predictor.train(X_train, y_train)
            accuracy = predictor.evaluate(X_test, y_test)
            print(f"\n{self.localizer.get_string(210)}: {accuracy:.2f}")
            
            model_file = "mutation_model.pkl"
            predictor.save_model(model_file)
            print(self.localizer.get_string(211).format(model_file))
        except Exception as e:
            print(f"{self.localizer.get_string(220)}: {str(e)}")


    def _validate_activation(self, activation):
        """Validate and normalize activation function choice.
        
        Args:
            activation: User input activation function
            
        Returns:
            str: Validated activation function or None if invalid
        """
        valid_activations = ['relu', 'logistic', 'tanh']
        activation = activation.lower().strip()
        if activation not in valid_activations:
            print(f"Invalid activation function. Valid options: {', '.join(valid_activations)}")
            return None
        return activation
        
    def _validate_learning_rate(self, learning_rate):
        """Validate learning rate.
        
        Args:
            learning_rate: User input learning rate
            
        Returns:
            float: Validated learning rate or None if invalid
        """
        try:
            lr = float(learning_rate)
            if lr <= 0:
                print("Learning rate must be positive")
                return None
            return lr
        except ValueError:
            print("Learning rate must be a number")
            return None
    
    def _create_risk_level(self):
        """Create simulated risk levels based on available data."""
        risk_factors = 0
        total_factors = 0
        
        # Age factor
        if 'Age' in self.df.columns:
            total_factors += 1
            risk_factors += np.where(self.df['Age'] > 65, 1, 
                                   np.where(self.df['Age'] > 50, 0.5, 0))
        
        # Stage factor
        if 'Stage' in self.df.columns:
            total_factors += 1
            risk_factors += np.where(self.df['Stage'] >= 3, 1,
                                   np.where(self.df['Stage'] >= 2, 0.5, 0))
        
        # Smoking factor
        if 'Smoking_Status' in self.df.columns:
            total_factors += 1
            risk_factors += np.where(self.df['Smoking_Status'].isin(['Current', 'Heavy']), 1,
                                   np.where(self.df['Smoking_Status'] == 'Former', 0.5, 0))
        
        # If we have any risk factors, calculate risk level based on average
        if total_factors > 0:
            risk_scores = risk_factors / total_factors
            return np.where(risk_scores >= 0.7, 'High',
                           np.where(risk_scores >= 0.3, 'Medium', 'Low'))
        else:
            # Fallback to random distribution
            return np.random.choice(['Low', 'Medium', 'High'], 
                                  size=len(self.df),
                                  p=[0.5, 0.3, 0.2])

    def _predict_mortality_risk(self):
        """Прогнозирует риск смертности."""
        if self.df.empty:
            print(f"{self.localizer.get_string(212)}")
            return
        
        target_column = 'Risk_Level'
        
        # Create or simulate a Risk_Level column if it doesn't exist
        if target_column not in self.df.columns:
            print(f"\n{self.localizer.get_string(233)}")  # Creating simulated risk levels for demonstration...
            print(f"{self.localizer.get_string(234)}")    # Note: This is simulated data for testing purposes
            
            # Check which risk factors are available
            risk_factors = []
            if 'Age' in self.df.columns:
                risk_factors.append('Age')
            if 'Stage' in self.df.columns:
                risk_factors.append('Stage')
            if 'Smoking_Status' in self.df.columns:
                risk_factors.append('Smoking_Status')
                
            if risk_factors:
                print(f"{self.localizer.get_string(235)}: {', '.join(risk_factors)}")  # Using factors for risk simulation
                self.df[target_column] = self._create_risk_level()
            else:
                print(f"{self.localizer.get_string(236)}")  # Using random distribution for risk simulation
                # Random distribution of risk levels
                self.df[target_column] = np.random.choice(
                    ['Low', 'Medium', 'High'], 
                    size=len(self.df),
                    p=[0.5, 0.3, 0.2]  # 50% low, 30% medium, 20% high risk
                )
            
            # Display risk level distribution
            print(f"\n{self.localizer.get_string(237)}")  # Risk level distribution:
            risk_dist = self.df[target_column].value_counts()
            for risk, count in risk_dist.items():
                risk_label = risk
                if risk == "Low":
                    risk_label = self.localizer.get_string(229)  # Low risk
                elif risk == "Medium":
                    risk_label = self.localizer.get_string(230)  # Medium risk
                elif risk == "High":
                    risk_label = self.localizer.get_string(231)  # High risk
                print(f"- {risk_label}: {count} ({count/len(self.df):.1%})")
        
        try:
            print(f"\n{self.localizer.get_string(224)}")  # Creating and training mortality risk model...
            
            # Get and validate neural network parameters
            try:
                hidden_layers = tuple(map(int, input(f"{self.localizer.get_string(207)}: ").split(',')))
            except ValueError:
                print("Invalid hidden layer format. Please enter comma-separated integers.")
                return
                
            activation = input(f"{self.localizer.get_string(208)}: ")
            activation = self._validate_activation(activation)
            if not activation:
                return
                
            learning_rate_input = input(f"{self.localizer.get_string(209)}: ")
            learning_rate = self._validate_learning_rate(learning_rate_input)
            if learning_rate is None:
                return
            
            predictor = CancerPredictor(
                hidden_layer_sizes=hidden_layers,
                activation=activation,
                learning_rate_init=learning_rate
            )
            
            self.df = self.df.dropna(subset=[target_column])
            X_train, X_test, y_train, y_test = predictor.preprocess_data(
                self.df, 
                target_column=target_column
            )
            predictor.train(X_train, y_train)
            accuracy = predictor.evaluate(X_test, y_test)
            print(f"\n{self.localizer.get_string(210)}: {accuracy:.2f}")
            
            model_file = "mortality_model.pkl"
            predictor.save_model(model_file)
            print(self.localizer.get_string(211).format(model_file))
        except Exception as e:
            print(f"{self.localizer.get_string(220)}: {str(e)}")

    def _predict_new_data(self):
        """Прогнозирует на новых пользовательских данных."""
        if self.df.empty:
            print(f"{self.localizer.get_string(212)}")
            return
        
        # Check if models exist and create them if needed
        models = {
            "cancer_model.pkl": self._predict_cancer_type,
            "mutation_model.pkl": self._predict_mutation_type,
            "mortality_model.pkl": self._predict_mortality_risk
        }
        
        for model_file, create_func in models.items():
            if not os.path.exists(model_file):
                print(self.localizer.get_string(225).format(model_file))  # Model needs to be created first
                choice = input(f"{self.localizer.get_string(225)} ").lower()
                if choice in ["y", "д"]:
                    print(self.localizer.get_string(227))  # Training new model...
                    create_func()
                else:
                    print(f"Skipping {model_file} predictions.")
                    continue
            else:
                print(f"\n{self.localizer.get_string(226)} {model_file}")  # Using existing model...

        try:
            new_data = {}
            valid_columns = [col for col in self.df.columns if col not in ['Cancer_Type', 'Mutation_Type', 'Risk_Level']]

            print(f"\n{self.localizer.get_string(214)}:")
            for column in valid_columns:
                dtype = self.df[column].dtype
                while True:
                    try:
                        value = input(f"{column} ({dtype}): ")
                        if np.issubdtype(dtype, np.number):
                            converted_value = float(value) if '.' in value else int(value)
                            new_data[column] = [converted_value]
                        else:
                            unique_values = list(map(str, self.df[column].unique()))
                            if value not in unique_values:
                                print(f"{self.localizer.get_string(215)}: {', '.join(unique_values)}")
                                continue
                            new_data[column] = [value]
                        break
                    except ValueError:
                        print(self.localizer.get_string(216).format(column))

            new_df = pd.DataFrame(new_data)[valid_columns]
            for col in valid_columns:
                new_df[col] = new_df[col].astype(self.df[col].dtype)
                
            predictions = {}
            
            # Cancer type prediction
            if os.path.exists("cancer_model.pkl"):
                predictor = CancerPredictor.load_model("cancer_model.pkl")
                X_processed, _ = predictor.preprocess_data(new_df)
                cancer_proba = predictor.model.predict_proba(X_processed)
                predictions["cancer"] = (predictor.label_encoder.classes_, cancer_proba[0])
            
            # Mutation type prediction
            if os.path.exists("mutation_model.pkl"):
                mutation_predictor = CancerPredictor.load_model("mutation_model.pkl")
                X_mut_processed, _ = mutation_predictor.preprocess_data(new_df)
                mutation_proba = mutation_predictor.model.predict_proba(X_mut_processed)
                predictions["mutation"] = (mutation_predictor.label_encoder.classes_, mutation_proba[0])
                
            # Mortality risk prediction
            if os.path.exists("mortality_model.pkl"):
                mortality_predictor = CancerPredictor.load_model("mortality_model.pkl")
                X_mort_processed, _ = mortality_predictor.preprocess_data(new_df)
                mortality_proba = mortality_predictor.model.predict_proba(X_mort_processed)
                predictions["mortality"] = (mortality_predictor.label_encoder.classes_, mortality_proba[0])

            self.df = pd.concat([self.df, new_df], ignore_index=True)

            print(f"\n{self.localizer.get_string(217)}:")
            
            if "cancer" in predictions:
                classes, probs = predictions["cancer"]
                print(f"\n{self.localizer.get_string(218)}:")
                for cls, prob in zip(classes, probs):
                    print(f"- {cls}: {prob:.2%}")

            if "mutation" in predictions:
                classes, probs = predictions["mutation"]
                print(f"\n{self.localizer.get_string(219)}:")
                for cls, prob in zip(classes, probs):
                    print(f"- {cls}: {prob:.2%}")
                    
            if "mortality" in predictions:
                classes, probs = predictions["mortality"]
                print(f"\n{self.localizer.get_string(232)}:")  # Mortality risk probabilities
                for cls, prob in zip(classes, probs):
                    risk_label = cls
                    if cls == "Low":
                        risk_label = self.localizer.get_string(229)  # Low risk
                    elif cls == "Medium":
                        risk_label = self.localizer.get_string(230)  # Medium risk
                    elif cls == "High":
                        risk_label = self.localizer.get_string(231)  # High risk
                    print(f"- {risk_label}: {prob:.2%}")

        except Exception as e:
            print(f"{self.localizer.get_string(220)}: {str(e)}")
            if 'new_df' in locals() and not new_df.empty:
                self.df = self.df[:-len(new_df)]


    def _exit_application(self):
        """Выводит сообщение о завершении работы."""
        print(f"\n{self.localizer.get_string(12)}")
        print(self.localizer.get_string(13))

if __name__ == "__main__":
    app = MainApplication()
