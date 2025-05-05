from sklearn.neural_network import MLPClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.metrics import accuracy_score
from sklearn.preprocessing import OneHotEncoder
import pandas as pd
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
        self.encoder = OneHotEncoder(handle_unknown='ignore')
        self.scaler = StandardScaler()
        self.label_encoder = LabelEncoder()
        
    def preprocess_data(self, df, target_column):
        """Обрабатывает категориальные и числовые признаки."""
        categorical_cols = df.select_dtypes(include=['object']).columns.drop(target_column)
        numeric_cols = df.select_dtypes(include=['number']).columns
        
        if not categorical_cols.empty:
            X_cat = self.encoder.fit_transform(df[categorical_cols]).toarray()
        else:
            X_cat = np.array([])
        
        X_num = self.scaler.fit_transform(df[numeric_cols]) if not numeric_cols.empty else np.array([])
        
        X = np.hstack([X_num, X_cat]) if X_cat.size else X_num
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
        """Сохраняет модель."""
        joblib.dump(self.model, path)
    
    @staticmethod
    def load_model(path):
        """Загружает модель."""
        return joblib.load(path)