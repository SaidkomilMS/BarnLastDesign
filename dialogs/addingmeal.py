from PyQt5 import QtCore, QtGui, QtWidgets
from dbworker import DBWorker


class MealInfoUI:
    def __init__(self, dialog: QtWidgets.QDialog, db_worker: DBWorker):
        self.dialog = dialog
        self.db_worker = db_worker
        self.label = QtWidgets.QLabel("Введите название блюда:", dialog)
        self.meal_name = QtWidgets.QLineEdit(dialog)
        self.ok_button = QtWidgets.QPushButton("Oк", dialog)
        self.cancel_button = QtWidgets.QPushButton("Отмена", dialog)
        self.main_layout = QtWidgets.QVBoxLayout(dialog)
        self.buttons_layout = QtWidgets.QHBoxLayout(dialog)
        self.setup_ui(dialog)
        self.ok_button.clicked.connect(self.add_meal)
        self.cancel_button.clicked.connect(self.dialog.close)

    def add_meal(self):
        self.db_worker.add_meal(self.meal_name.text())
        self.dialog.close()

    def setup_ui(self, dialog):
        font = QtGui.QFont()
        font.setPointSize(9)
        dialog.setFont(font)
        QtCore.QMetaObject.connectSlotsByName(dialog)
        dialog.setWindowTitle("Добавление блюда")
        self.buttons_layout.addWidget(self.ok_button)
        self.cancel_button.addWidget(self.cancel_button)
        self.main_layout.addWidget(self.label)
        self.main_layout.addWidget(self.meal_name)
        self.main_layout.addLayout(self.buttons_layout)
        dialog.setLayout(self.main_layout)
