from PyQt5 import QtCore, QtGui, QtWidgets
from dbworker import DBWorker


class UiProductInfo:
    def __init__(self, dialog: QtWidgets.QDialog, worker: DBWorker):
        self.product_name = QtWidgets.QLineEdit(dialog)
        self.product_unit = QtWidgets.QComboBox(dialog)
        self.label = QtWidgets.QLabel(dialog)
        self.cancel_button = QtWidgets.QPushButton(dialog)
        self.ok_button = QtWidgets.QPushButton(dialog)
        self.main_layout = QtWidgets.QVBoxLayout(dialog)
        self.buttons_layout = QtWidgets.QHBoxLayout(dialog)
        self.dialog = dialog
        self.db_worker = worker
        self.ok_button.clicked.connect(self.save_product)
        self.cancel_button.clicked.connect(self.dialog.close)

    def save_product(self):
        self.db_worker.add_product(self.product_name.text(), self.product_unit.currentText())
        self.dialog.close()

    def setup_ui(self, dialog: QtWidgets.QDialog):
        dialog.setObjectName("Dialog")
        font = QtGui.QFont()
        font.setPointSize(9)
        dialog.setFont(font)
        self.retranslate_ui(dialog)
        QtCore.QMetaObject.connectSlotsByName(dialog)
        self.buttons_layout.addWidget(self.ok_button)
        self.buttons_layout.addWidget(self.cancel_button)
        self.main_layout.addWidget(self.label)
        self.main_layout.addWidget(self.product_name)
        self.main_layout.addWidget(self.product_unit)
        self.main_layout.addLayout(self.buttons_layout)
        dialog.setLayout(self.main_layout)
        dialog.adjustSize()

    def retranslate_ui(self, dialog):
        _translate = QtCore.QCoreApplication.translate
        dialog.setWindowTitle(_translate("Dialog", "Добавление продукта"))
        self.ok_button.setText(_translate("Dialog", "OK"))
        self.cancel_button.setText(_translate("Dialog", "Cancel"))
        self.label.setText(_translate("Dialog", "Введите название:"))
        self.product_unit.addItem("шт", "шт")
        self.product_unit.addItem("кг", "кг")
        self.product_unit.addItem("г", "г")
