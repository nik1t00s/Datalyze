# neural_network.py (полная версия с исправлениями)
from sklearn.neural_network import MLPClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.metrics import accuracy_score
from sklearn.preprocessing import OneHotEncoder
import numpy as np
import joblib

class CancerPredictor:
    def __init__(self, hidden_layer_sizes=(100,), activation='relu', learning_rate_init=0.001):
        self.model = MLPClassifier(
            hidden_layer_sizes=hidden_layer_sizes,
            activation=activation,
            learning_rate_init=learning_rate_init,
            max_iter=200,
            random_state=42
        )
        self.encoder = OneHotEncoder(handle_unknown='ignore')
        self.scaler = StandardScaler()
        self.label_encoder = LabelEncoder()
        self.feature_names = None  # Добавлено для хранения имен признаков

    def preprocess_data(self, df, target_column=None):
        """Обрабатывает категориальные и числовые признаки."""
        # Изменения в обработке категориальных признаков
        categorical_cols = df.select_dtypes(include=['object']).columns
        numeric_cols = df.select_dtypes(include=['number']).columns
        
        # Сохраняем имена признаков
        self.feature_names = list(categorical_cols) + list(numeric_cols)
        
        # Удаляем целевую переменную только если она указана
        if target_column:
            categorical_cols = categorical_cols.drop(target_column, errors='ignore')
            numeric_cols = numeric_cols.drop(target_column, errors='ignore')

        # Обработка категориальных признаков
        if not categorical_cols.empty:
            self.encoder.fit(df[categorical_cols])
            X_cat = self.encoder.transform(df[categorical_cols]).toarray()
        else:
            X_cat = np.array([])

        # Обработка числовых признаков
        if not numeric_cols.empty:
            self.scaler.fit(df[numeric_cols])
            X_num = self.scaler.transform(df[numeric_cols])
        else:
            X_num = np.array([])

        # Объединение признаков
        X = np.hstack([X_num, X_cat]) if X_cat.size else X_num

        if not target_column:
            return X, None

        y = self.label_encoder.fit_transform(df[target_column])
        return train_test_split(X, y, test_size=0.2, random_state=42)

    def train(self, X_train, y_train):
        self.model.fit(X_train, y_train)

    def evaluate(self, X_test, y_test):
        y_pred = self.model.predict(X_test)
        return accuracy_score(y_test, y_pred)

    def save_model(self, path):
        to_dump = {
            'model': self.model,
            'encoder': self.encoder,
            'scaler': self.scaler,
            'label_encoder': self.label_encoder,
            'feature_names': self.feature_names  # Сохраняем имена признаков
        }
        joblib.dump(to_dump, path)

    @staticmethod
    def load_model(path):
        loaded = joblib.load(path)
        predictor = CancerPredictor(
            hidden_layer_sizes=loaded['model'].hidden_layer_sizes,
            activation=loaded['model'].activation,
            learning_rate_init=loaded['model'].learning_rate_init
        )
        # Прямая подстановка загруженных компонентов
        predictor.model = loaded['model']
        predictor.encoder = loaded['encoder']
        predictor.scaler = loaded['scaler']
        predictor.label_encoder = loaded['label_encoder']
        predictor.feature_names = loaded['feature_names']  # Загружаем имена
        
        return predictor