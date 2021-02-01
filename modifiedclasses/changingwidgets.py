from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QDateEdit, QLabel, QPushButton,
    QSpinBox, QDoubleSpinBox, QRadioButton, QCheckBox, QApplication,
    QPlainTextEdit
)
from PyQt5.QtCore import QSize
from datetime import date
import sys

from extrautils.extrafuncs import centralize_text


class AddIncrementWidget(QWidget):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        #  Creating and setting the components and their characteristics
        size = QSize(400, 370)
        self.setFixedSize(size)
        self.main_layout = QVBoxLayout()
        title: str = centralize_text("Добавление прихода продукта:")
        self.title = QLabel(title, parent=self)
        self.data_layout = QHBoxLayout()
        self.price_quantity_layout = QVBoxLayout()
        self.price_title = QLabel("Цена:", parent=self)
        self.price_value = QSpinBox()
        self.price_value.setValue(0)
        self.price_value.setRange(0, 1000000)
        self.price_value.setSingleStep(1000)
        self.quantity_title = QLabel("Кол-во:", parent=self)
        self.quantity_value = QDoubleSpinBox(parent=self)
        self.quantity_value.setSingleStep(1.0)
        self.quantity_value.setRange(0.0, 1000000.0)
        self.quantity_value.setDecimals(3)
        self.agreement_title = QLabel(
            "Информация о доверенности:",
            parent=self)
        self.agreement_info = QPlainTextEdit(parent=self)
        self.date_layout = QVBoxLayout()
        self.date_title = QLabel("Выберите дату:", parent=self)
        self.today_radio = QRadioButton("Сегодня", parent=self)
        self.today_radio.setChecked(True)
        self.today_radio.clicked.connect(self.disable_date_edit)
        self.otherday_radio = QRadioButton("Другой день", parent=self)
        self.otherday_radio.clicked.connect(self.enable_date_edit)
        self.otherday_edit = QDateEdit(date=date.today(), parent=self)
        self.otherday_edit.setDisabled(True)
        self.invoice_title = QLabel("Информация о счёт-фактуре:", parent=self)
        self.invoice_info = QPlainTextEdit(parent=self)
        self.button = QPushButton("Добавить &приход", parent=self)
        #  Locating the components in the widget
        self.setLayout(self.main_layout)
        self.main_layout.addWidget(self.title)
        self.main_layout.addLayout(self.data_layout)
        self.data_layout.addLayout(self.price_quantity_layout)
        self.price_quantity_layout.addWidget(self.price_title)
        self.price_quantity_layout.addWidget(self.price_value)
        self.price_quantity_layout.addWidget(self.quantity_title)
        self.price_quantity_layout.addWidget(self.quantity_value)
        self.price_quantity_layout.addWidget(self.agreement_title)
        self.price_quantity_layout.addWidget(self.agreement_info)
        self.data_layout.addLayout(self.date_layout)
        self.date_layout.addWidget(self.date_title)
        self.date_layout.addWidget(self.today_radio)
        self.date_layout.addWidget(self.otherday_radio)
        self.date_layout.addWidget(self.otherday_edit)
        self.date_layout.addWidget(self.invoice_title)
        self.date_layout.addWidget(self.invoice_info)
        self.main_layout.addWidget(self.button)

    def enable_date_edit(self):
        #  The user would choose another date
        self.otherday_edit.setEnabled(True)

    def disable_date_edit(self):
        #  The user chose today
        self.otherday_edit.setDate(date.today())
        self.otherday_edit.setDisabled(True)


class AddDecrementWidget(QWidget):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        #  Creating and setting the components and their characteristics
        size = QSize(400, 250)
        self.setFixedSize(size)
        self.main_layout = QVBoxLayout()
        title: str = centralize_text("Добавить расход продукта")
        self.title = QLabel(title, parent=self)
        self.data_layout = QHBoxLayout()
        self.quantity_layout = QVBoxLayout()
        self.quantity_title = QLabel("Кол-во:", parent=self)
        self.quantity_value = QDoubleSpinBox(parent=self)
        self.quantity_value.setSingleStep(1.0)
        self.quantity_value.setRange(0.0, 1000000.0)
        self.quantity_value.setDecimals(3)
        self.quantity_checker = QCheckBox("На 1 ребёнка", parent=self)
        self.date_layout = QVBoxLayout()
        self.date_title = QLabel("Выберите дату:", parent=self)
        self.today_radio = QRadioButton("Сегодня", parent=self)
        self.today_radio.setChecked(True)
        self.today_radio.clicked.connect(self.disable_date_edit)
        self.otherday_radio = QRadioButton("Другой день", parent=self)
        self.otherday_radio.clicked.connect(self.enable_date_edit)
        self.otherday_edit = QDateEdit(date=date.today(), parent=self)
        self.otherday_edit.setDisabled(True)
        self.button = QPushButton("Добавить &расход", parent=self)
        #  Locating the components in the widget
        self.setLayout(self.main_layout)
        self.main_layout.addWidget(self.title)
        self.main_layout.addLayout(self.data_layout)
        self.data_layout.addLayout(self.quantity_layout)
        self.quantity_layout.addWidget(self.quantity_title)
        self.quantity_layout.addWidget(self.quantity_value)
        self.quantity_layout.addWidget(self.quantity_checker)
        self.data_layout.addLayout(self.date_layout)
        self.date_layout.addWidget(self.date_title)
        self.date_layout.addWidget(self.today_radio)
        self.date_layout.addWidget(self.otherday_radio)
        self.date_layout.addWidget(self.otherday_edit)
        self.main_layout.addWidget(self.button)

    def enable_date_edit(self):
        #  The user would choose another date
        self.otherday_edit.setEnabled(True)

    def disable_date_edit(self):
        #  The user chose today
        self.otherday_edit.setDate(date.today())
        self.otherday_edit.setDisabled(True)


if __name__ == '__main__':
    app = QApplication([])
    main_window = AddIncrementWidget()
    main_window.show()
    sys.exit(app.exec_())
