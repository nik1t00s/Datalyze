from sklearn.neural_network import MLPClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import RobustScaler, LabelEncoder
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
        self.scaler = RobustScaler()
        self.label_encoder = LabelEncoder()
        self.feature_names = None

    def preprocess_data(self, df, target_column=None):
        df = df.copy()
        df = df.replace([np.inf, -np.inf], np.nan).dropna()

        categorical_cols = df.select_dtypes(include=['object']).columns.tolist()
        numeric_cols = df.select_dtypes(include=['number']).columns.tolist()

        if target_column:
            if target_column in categorical_cols:
                categorical_cols.remove(target_column)
            if target_column in numeric_cols:
                numeric_cols.remove(target_column)

        for col in ['Cancer_Type', 'Mutation_Type']:
            if col != target_column:
                if col in categorical_cols:
                    categorical_cols.remove(col)
                if col in numeric_cols:
                    numeric_cols.remove(col)

        X_cat = np.array([])
        if categorical_cols:
            if not hasattr(self.encoder, 'categories_'):
                self.encoder.fit(df[categorical_cols])
            X_cat = self.encoder.transform(df[categorical_cols]).toarray()

        X_num = np.array([])
        if numeric_cols:
            if not hasattr(self.scaler, 'scale_'):
                self.scaler.fit(df[numeric_cols])
            X_num = self.scaler.transform(df[numeric_cols])

        if X_cat.size and X_num.size:
            X = np.hstack([X_num, X_cat])
        elif X_num.size:
            X = X_num
        elif X_cat.size:
            X = X_cat
        else:
            raise ValueError("Нет признаков для обработки.")

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
            'feature_names': self.feature_names
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
        predictor.model = loaded['model']
        predictor.encoder = loaded['encoder']
        predictor.scaler = loaded['scaler']
        predictor.label_encoder = loaded['label_encoder']
        predictor.feature_names = loaded['feature_names']
        
        return predictor