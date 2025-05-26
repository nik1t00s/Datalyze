# gui.py
import sys
import os
import pandas as pd
from PyQt6.QtWidgets import (
    QMainWindow, QApplication, QWidget, QVBoxLayout, QPushButton, QMessageBox,
    QFileDialog, QComboBox, QDialog, QLineEdit, QFormLayout, QTableView,
    QTabWidget, QLabel, QProgressBar
)
from PyQt6.QtCore import Qt, QAbstractTableModel, QThread, pyqtSignal, QObject
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from main import MainApplication
from neural_network import CancerPredictor
import joblib


class PandasModel(QAbstractTableModel):
    def __init__(self, data):
        super().__init__()
        self._data = data

    def rowCount(self, parent=None):
        return self._data.shape[0]

    def columnCount(self, parent=None):
        return self._data.shape[1]

    def data(self, index, role=Qt.ItemDataRole.DisplayRole):
        if role == Qt.ItemDataRole.DisplayRole:
            return str(self._data.iloc[index.row(), index.column()])
        return None

    def headerData(self, section, orientation, role):
        if role == Qt.ItemDataRole.DisplayRole:
            if orientation == Qt.Orientation.Horizontal:
                return str(self._data.columns[section])
            else:
                return str(self._data.index[section])
        return None


class Worker(QObject):
    finished = pyqtSignal()
    progress = pyqtSignal(int)
    result = pyqtSignal(object)

    def __init__(self, task, *args):
        super().__init__()
        self.task = task
        self.args = args

    def run(self):
        try:
            result = self.task(*self.args)
            self.result.emit(result)
        finally:
            self.finished.emit()


class MainWindow(QMainWindow):
    def __init__(self, app_logic):
        super().__init__()
        self.app_logic = app_logic
        self.initUI()
        self.setup_connections()
        self.current_plot = None
        self.progress_bar = QProgressBar()
        self.statusBar().addPermanentWidget(self.progress_bar)
        self.progress_bar.hide()

    def initUI(self):
        self.setWindowTitle("Medical Data Analyzer")
        self.setGeometry(100, 100, 1000, 800)
        self.tabs = QTabWidget()
        self.main_tab = QWidget()
        self.nn_tab = QWidget()
        self.visualization_tab = QWidget()

        self.tabs.addTab(self.main_tab, self.tr("Main"))
        self.tabs.addTab(self.nn_tab, self.tr("Neural Network"))
        self.tabs.addTab(self.visualization_tab, self.tr("Visualization"))

        self.setup_main_tab()
        self.setup_nn_tab()
        self.setup_visualization_tab()

        self.setCentralWidget(self.tabs)
        self.statusBar().showMessage(self.tr("Ready"))

    def setup_main_tab(self):
        layout = QVBoxLayout()
        self.lang_combo = QComboBox()
        self.lang_combo.addItems(["English", "Русский"])
        layout.addWidget(self.lang_combo)

        self.import_btn = QPushButton(self.tr("Import Data"))
        self.table_btn = QPushButton(self.tr("View Table"))
        self.exit_btn = QPushButton(self.tr("Exit"))

        layout.addWidget(self.import_btn)
        layout.addWidget(self.table_btn)
        layout.addWidget(self.exit_btn)

        self.main_tab.setLayout(layout)

    def setup_nn_tab(self):
        layout = QVBoxLayout()
        self.nn_btn = QPushButton(self.tr("Train Model"))
        self.predict_btn = QPushButton(self.tr("Predict New Data"))
        layout.addWidget(self.nn_btn)
        layout.addWidget(self.predict_btn)
        self.nn_tab.setLayout(layout)

    def setup_visualization_tab(self):
        layout = QVBoxLayout()
        self.plot_canvas = FigureCanvas(Figure(figsize=(8, 6)))
        self.x_combo = QComboBox()
        self.y_combo = QComboBox()
        self.plot_type_combo = QComboBox()
        self.plot_type_combo.addItems(["Bar Chart", "Line Chart"])

        controls = QWidget()
        controls_layout = QFormLayout()
        controls_layout.addRow(QLabel(self.tr("X Axis:")), self.x_combo)
        controls_layout.addRow(QLabel(self.tr("Y Axis:")), self.y_combo)
        controls_layout.addRow(QLabel(self.tr("Plot Type:")), self.plot_type_combo)
        controls.setLayout(controls_layout)

        self.plot_btn = QPushButton(self.tr("Generate Plot"))

        layout.addWidget(controls)
        layout.addWidget(self.plot_btn)
        layout.addWidget(self.plot_canvas)
        self.visualization_tab.setLayout(layout)

    def setup_connections(self):
        self.lang_combo.currentIndexChanged.connect(self.change_language)
        self.import_btn.clicked.connect(self.handle_import)
        self.table_btn.clicked.connect(self.show_table)
        self.exit_btn.clicked.connect(self.close)
        self.nn_btn.clicked.connect(self.show_nn_dialog)
        self.predict_btn.clicked.connect(self.show_predict_dialog)
        self.plot_btn.clicked.connect(self.generate_plot)

    def change_language(self):
        lang = "RU" if self.lang_combo.currentIndex() == 1 else "ENG"
        self.app_logic.localizer.language = lang
        self.app_logic.localizer.load_strings()
        self.update_texts()

    def update_texts(self):
        self.setWindowTitle(self.tr("Medical Data Analyzer"))
        self.tabs.setTabText(0, self.tr("Main"))
        self.tabs.setTabText(1, self.tr("Neural Network"))
        self.tabs.setTabText(2, self.tr("Visualization"))
        self.import_btn.setText(self.tr("Import Data"))
        self.table_btn.setText(self.tr("View Table"))
        self.exit_btn.setText(self.tr("Exit"))
        self.nn_btn.setText(self.tr("Train Model"))
        self.predict_btn.setText(self.tr("Predict New Data"))
        self.plot_btn.setText(self.tr("Generate Plot"))

    def handle_import(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self, self.tr("Select File"), "", "CSV Files (*.csv);;Excel Files (*.xlsx)")
        if file_path:
            self.start_loading_animation()
            self.run_async_task(self.app_logic.importer.import_data, file_path)

    def run_async_task(self, task, *args):
        self.thread = QThread()
        self.worker = Worker(task, *args)
        self.worker.moveToThread(self.thread)

        self.thread.started.connect(self.worker.run)
        self.worker.finished.connect(self.thread.quit)
        self.worker.finished.connect(self.worker.deleteLater)
        self.thread.finished.connect(self.thread.deleteLater)
        self.worker.result.connect(self.handle_task_result)

        self.thread.start()
        self.progress_bar.show()
        QApplication.setOverrideCursor(Qt.CursorShape.WaitCursor)

    def handle_task_result(self, result):
        success, df = result
        if success:
            self.app_logic.df = df
            self.update_visualization_controls()
            QMessageBox.information(self, self.tr("Success"),
                                    self.tr("Loaded {} rows").format(len(df)))
        self.progress_bar.hide()
        QApplication.restoreOverrideCursor()

    def show_table(self):
        if self.app_logic.df.empty:
            QMessageBox.warning(self, self.tr("Warning"), self.tr("No data loaded"))
            return

        dialog = QDialog(self)
        dialog.setWindowTitle(self.tr("Data Table"))
        layout = QVBoxLayout()
        table = QTableView()
        model = PandasModel(self.app_logic.df)
        table.setModel(model)
        layout.addWidget(table)
        dialog.setLayout(layout)
        dialog.exec()

    def update_visualization_controls(self):
        if not self.app_logic.df.empty:
            self.x_combo.clear()
            self.y_combo.clear()
            columns = self.app_logic.df.columns.tolist()
            self.x_combo.addItems(columns)
            self.y_combo.addItems(columns)

    def generate_plot(self):
        try:
            x_col = self.x_combo.currentText()
            y_col = self.y_combo.currentText()
            plot_type = self.plot_type_combo.currentText().lower().replace(" ", "_")

            self.start_loading_animation()
            self.run_async_plot_task(x_col, y_col, plot_type)
        except Exception as e:
            QMessageBox.critical(self, self.tr("Error"), str(e))

    def run_async_plot_task(self, x_col, y_col, plot_type):
        self.thread = QThread()
        self.worker = Worker(
            self.app_logic.visualizer._plot_chart,
            self.app_logic.df, plot_type, x_col, [y_col]
        )
        self.worker.moveToThread(self.thread)

        self.thread.started.connect(self.worker.run)
        self.worker.finished.connect(self.thread.quit)
        self.worker.finished.connect(self.worker.deleteLater)
        self.thread.finished.connect(self.thread.deleteLater)
        self.worker.result.connect(lambda: self.update_plot(x_col, y_col, plot_type))

        self.thread.start()

    def update_plot(self, x_col, y_col, plot_type):
        try:
            self.plot_canvas.figure.clear()
            ax = self.plot_canvas.figure.add_subplot(111)

            if plot_type == "bar_chart":
                self.app_logic.df.plot.bar(x=x_col, y=y_col, ax=ax)
            else:
                self.app_logic.df.plot.line(x=x_col, y=y_col, ax=ax)

            self.plot_canvas.draw()
        except Exception as e:
            QMessageBox.critical(self, self.tr("Error"), str(e))
        finally:
            self.progress_bar.hide()
            QApplication.restoreOverrideCursor()

    def start_loading_animation(self):
        self.progress_bar.setRange(0, 0)
        self.progress_bar.show()
        QApplication.setOverrideCursor(Qt.CursorShape.WaitCursor)

    def show_nn_dialog(self):
        dialog = NeuralNetworkDialog(self)
        dialog.exec()

    def show_predict_dialog(self):
        dialog = PredictDialog(self.app_logic, self)
        dialog.exec()


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

        self.train_btn = QPushButton(self.tr("Train Model"))
        self.train_btn.clicked.connect(self.train_model)

        layout.addLayout(form)
        layout.addWidget(self.train_btn)
        self.setLayout(layout)

    def train_model(self):
        try:
            hidden_layers = tuple(map(int, self.hidden_layers.text().split(',')))
            activation = self.activation.text()
            learning_rate = float(self.learning_rate.text())

            self.parent.start_loading_animation()
            self.parent.run_async_task(
                self.train_model_task,
                hidden_layers,
                activation,
                learning_rate
            )
        except Exception as e:
            QMessageBox.critical(self, self.tr("Error"), str(e))

    def train_model_task(self, hidden_layers, activation, learning_rate):
        predictor = CancerPredictor(
            hidden_layer_sizes=hidden_layers,
            activation=activation,
            learning_rate_init=learning_rate
        )

        X_train, X_test, y_train, y_test = predictor.preprocess_data(
            self.parent.app_logic.df, "Cancer_Type"
        )
        predictor.train(X_train, y_train)
        return predictor.evaluate(X_test, y_test)


class PredictDialog(QDialog):
    def __init__(self, app_logic, parent=None):
        super().__init__(parent)
        self.app_logic = app_logic
        self.setup_ui()

    def setup_ui(self):
        self.setWindowTitle(self.tr("Predict New Data"))
        layout = QFormLayout()

        self.inputs = {}
        valid_columns = [
            col for col in self.app_logic.df.columns
            if col not in ['Cancer_Type', 'Mutation_Type', 'Risk_Level']
        ]

        for col in valid_columns:
            self.inputs[col] = QLineEdit()
            layout.addRow(QLabel(col), self.inputs[col])

        self.predict_btn = QPushButton(self.tr("Predict"))
        self.predict_btn.clicked.connect(self.run_prediction)
        layout.addWidget(self.predict_btn)

        self.setLayout(layout)

    def run_prediction(self):
        try:
            new_data = {}
            for col, widget in self.inputs.items():
                dtype = self.app_logic.df[col].dtype
                value = widget.text()
                new_data[col] = [float(value)] if pd.api.types.is_numeric_dtype(dtype) else [value]

            self.parent().start_loading_animation()
            self.parent().run_async_task(
                self.app_logic._predict_new_data
            )
            QMessageBox.information(self, self.tr("Success"), self.tr("Prediction completed"))
        except Exception as e:
            QMessageBox.critical(self, self.tr("Error"), str(e))


def run_gui(app_logic):
    app = QApplication(sys.argv)
    window = MainWindow(app_logic)
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    app_logic = MainApplication()
    run_gui(app_logic)