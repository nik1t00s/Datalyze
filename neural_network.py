from sklearn.neural_network import MLPClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.metrics import accuracy_score
from sklearn.preprocessing import OneHotEncoder
import numpy as np
import joblib

class CancerPredictor:
    """Класс для прогнозирования рака с использованием нейронной сети из scikit-learn."""
    
    def __init__(self, hidden_layer_sizes=(100,), activation='relu', learning_rate_init=0.001):
        self.model = MLPClassifier(
            hidden_layer_sizes=hidden_layer_sizes,
            activation=activation,
            learning_rate_init=learning_rate_init,
            max_iter=200,
            random_state=42
        )
        # Инициализируйте препроцессоры явно
        self.encoder = OneHotEncoder(handle_unknown='ignore')
        self.scaler = StandardScaler()
        self.label_encoder = LabelEncoder()
        
    def preprocess_data(self, df, target_column=None):
        """Обрабатывает категориальные и числовые признаки."""
        categorical_cols = df.select_dtypes(include=['object']).columns
        if target_column:
            categorical_cols = categorical_cols.drop(target_column)
        categorical_cols = categorical_cols.drop('Mutation_Type', errors='ignore')  # Исключите столбец
        
        numeric_cols = df.select_dtypes(include=['number']).columns
        numeric_cols = numeric_cols.drop(['Cancer_Type', 'Mutation_Type'], errors='ignore')
        # Определение категориальных и числовых столбцов
        categorical_cols = df.select_dtypes(include=['object']).columns
        if target_column and target_column in categorical_cols:
            categorical_cols = categorical_cols.drop(target_column)
        
        numeric_cols = df.select_dtypes(include=['number']).columns

        # Обучение encoder и scaler только если есть данные
        if not categorical_cols.empty:
            if not hasattr(self.encoder, 'categories_'):
                # Если encoder не обучен, обучите его
                self.encoder.fit(df[categorical_cols])
            X_cat = self.encoder.transform(df[categorical_cols]).toarray()
        else:
            X_cat = np.array([])

        if not numeric_cols.empty:
            if not hasattr(self.scaler, 'scale_'):
                # Если scaler не обучен, обучите его
                self.scaler.fit(df[numeric_cols])
            X_num = self.scaler.transform(df[numeric_cols])
        else:
            X_num = np.array([])

        X = np.hstack([X_num, X_cat]) if X_cat.size else X_num

        # Для прогнозирования возвращаем только X
        if not target_column:
            return X, None

        # Обучение label_encoder для целевой переменной
        y = self.label_encoder.fit_transform(df[target_column])
        return train_test_split(X, y, test_size=0.2, random_state=42)
    
    def train(self, X_train, y_train):
        """Обучает модель."""
        self.model.fit(X_train, y_train)
    
    def evaluate(self, X_test, y_test):
        """Оценивает точность модели."""
        y_pred = self.model.predict(X_test)
        return accuracy_score(y_test, y_pred)
    
    def save_model(self, path):
        """Сохраняет модель с параметрами признаков."""
        to_dump = {
            'model': self.model,
            'encoder': self.encoder,
            'scaler': self.scaler,
            'label_encoder': self.label_encoder,
            'feature_names': list(self.encoder.feature_names_in_) + list(self.scaler.feature_names_in_)
        }
        joblib.dump(to_dump, path)
    
    @staticmethod
    def load_model(path):
        """Загружает модель и препроцессоры."""
        loaded = joblib.load(path)
        predictor = CancerPredictor(
            hidden_layer_sizes=loaded['model'].hidden_layer_sizes,
            activation=loaded['model'].activation,
            learning_rate_init=loaded['model'].learning_rate_init
        )
        predictor.feature_names = loaded['feature_names']
        return predictor