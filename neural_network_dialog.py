# neural_network_dialog.py (новый файл)
from PyQt6.QtWidgets import QDialog, QVBoxLayout, QFormLayout, QLineEdit, QPushButton, QMessageBox

from neural_network import CancerPredictor


class NeuralNetworkDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.setup_ui()

    def setup_ui(self):
        self.setWindowTitle(self.tr("Neural Network Settings"))
        layout = QVBoxLayout()

        form = QFormLayout()
        self.hidden_layers = QLineEdit("50,25")
        self.activation = QLineEdit("relu")
        self.learning_rate = QLineEdit("0.001")

        form.addRow(self.tr("Hidden Layers (comma-separated):"), self.hidden_layers)
        form.addRow(self.tr("Activation Function:"), self.activation)
        form.addRow(self.tr("Learning Rate:"), self.learning_rate)

        self.train_button = QPushButton(self.tr("Train Model"))
        self.train_button.clicked.connect(self.train_model)

        layout.addLayout(form)
        layout.addWidget(self.train_button)
        self.setLayout(layout)

    def train_model(self):
        try:
            hidden_layers = tuple(map(int, self.hidden_layers.text().split(',')))
            activation = self.activation.text()
            learning_rate = float(self.learning_rate.text())

            predictor = CancerPredictor(
                hidden_layer_sizes=hidden_layers,
                activation=activation,
                learning_rate_init=learning_rate
            )

            X_train, X_test, y_train, y_test = predictor.preprocess_data(self.parent.app_logic.df, "Cancer_Type")
            predictor.train(X_train, y_train)
            accuracy = predictor.evaluate(X_test, y_test)

            QMessageBox.information(self,
                                    self.tr("Training Complete"),
                                    self.tr(f"Model accuracy: {accuracy:.2%}"))
            self.accept()
        except Exception as e:
            QMessageBox.critical(self, self.tr("Error"), str(e))