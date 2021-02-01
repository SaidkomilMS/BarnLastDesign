import time
from datetime import date, datetime
from typing import List

from PIL import Image, ImageDraw, ImageFont
from PyQt5 import QtCore, QtGui
from PyQt5.QtSql import QSqlTableModel, QSqlDatabase  # , QSqlRelationalTableModel, QSqlRelationalDelegate
from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QPushButton, QVBoxLayout, QHBoxLayout,
    QTableView, QLabel, QSpacerItem, QSizePolicy, QDialog,
    QLayout, QScrollArea, QGroupBox, QSplashScreen  # , QTableWidget
)

from dbworker import DBWorker
from dialogs.ask_cc_dialog import ChildCountUi
from dialogs.ask_new_product_info import UiProductInfo
from extrautils import *
from modifiedclasses.changingwidgets import AddDecrementWidget, AddIncrementWidget
from modifiedclasses.mysqlrelatioanltablemodel import SRTM
from modifiedclasses.productbutton import ProductButton
from mydeleagtes import DateDelegate


def get_now():
    return datetime.now().strftime('%H:%M')  # timezone("Asia/Tashkent")


def generate_image(text):
    image = Image.new('RGB', (500, 500), color='white')
    w, h = image.size
    draw = ImageDraw.Draw(image)

    font = ImageFont.truetype("resources/ds-digit.ttf", size=212)
    wt, ht = draw.textsize(text, font)
    draw.text(((w - wt) / 2, (h - ht) / 2), text, font=font, fill='#247ac6')
    font = ImageFont.truetype("resources/ubuntu.ttf", size=55)
    text = "Время в ташкенте:"
    wt, ht = draw.textsize(text, font)
    draw.text(((w - wt) / 2, int(0.5 * ht)), text, font=font, fill="#247ac6")

    image.save(r'images/spimage.jpg')


class MainWindow(QMainWindow):
    child_count_is_known = False

    def __init__(self, db_worker: DBWorker, parent=None):
        generate_image(get_now())
        QMainWindow.__init__(self, parent)
        self.setWindowTitle("Амбарная книга")
        self.splash_for_time = QSplashScreen(QtGui.QPixmap(r'images/spimage.jpg'))
        self.splash_for_time.showMessage(
            "Сохраните своё время с нами!\n\nПодключение к базе данных...\n\r",
            QtCore.Qt.AlignCenter | QtCore.Qt.AlignBottom,
            QtCore.Qt.black
        )
        self.splash_for_time.show()
        time.sleep(2)
        self.db_worker: DBWorker = db_worker
        self.con = QSqlDatabase.addDatabase("QSQLITE")
        self.con.setDatabaseName('ambar_book.db')
        self.con.open()
        self.stm: SRTM = SRTM(self)
        self.stm.setEditStrategy(QSqlTableModel.OnManualSubmit)
        generate_image(get_now())
        self.splash_for_time.setPixmap(QtGui.QPixmap(r'images/spimage.jpg'))
        self.splash_for_time.showMessage(
            "Сохраните своё время с нами!\n\nЗагрузка элементов экрана...\n\r",
            QtCore.Qt.AlignCenter | QtCore.Qt.AlignBottom,
            QtCore.Qt.black
        )
        time.sleep(2)
        self.central_widget: QWidget = QWidget(self)
        self.main_layout: QLayout = QVBoxLayout()
        self.table_labels_row: QLayout = QHBoxLayout()
        self.control_buttons_row: QLayout = QHBoxLayout()
        self.table_title_layout: QLayout = QVBoxLayout()
        self.pbcwg = QGroupBox("Выберите продукт:")
        self.pbc: QLayout = QVBoxLayout()  # ProductButtonsColumn
        self.pbcwg.setLayout(self.pbc)
        self.pbcw = QScrollArea(self)
        self.pbcw.setWidget(self.pbcwg)
        self.pbcw.setWidgetResizable(True)
        self.labels_increment_decrement_column = QVBoxLayout()
        self.product_buttons: List[ProductButton] = list()
        self.table_title: QLabel = QLabel("", parent=self)
        self.table: QTableView = QTableView(self)
        # self.table = QTableWidget(self)
        self.child_count_label = QLabel("", parent=self)
        self.date_label = QLabel(date.today().strftime("%d.%m.%Y"))
        self.add_increment_widget = AddIncrementWidget(parent=self)
        self.add_increment_widget.button.clicked.connect(self.add_increment)
        self.add_decrement_widget = AddDecrementWidget(parent=self)
        self.add_decrement_widget.button.clicked.connect(self.add_decrement)
        self.add_row_button = QPushButton("Добавить строку", parent=self)
        self.add_row_button.clicked.connect(self.add_row)
        self.delete_row_button = QPushButton("Убрать строку", parent=self)
        self.delete_row_button.clicked.connect(self.delete_row)
        self.setup_menu_bar()
        self.load_ui()
        self.setStyleSheet(css_style)
        self.chosen_product = self.product_buttons[0]
        self.chosen_product.setObjectName("chosenProductButton")
        self.table_title.setText(centralize_text(self.chosen_product.text()))
        self.load_changings()
        self.add_decrement_widget.quantity_checker.setEnabled(self.child_count_is_known)

    def edit_remainders(self) -> None:
        return

    def show_remainders(self) -> None:
        return

    def setup_menu_bar(self):
        menu_bar = self.menuBar()
        my_menu_add = menu_bar.addMenu("&Добавить")
        my_menu_add.addAction(
            "&Продукт", self.add_product,
            QtCore.Qt.CTRL + QtCore.Qt.Key_N + QtCore.Qt.Key_P)
        menu_remainders = menu_bar.addMenu("&Остатки")
        menu_remainders.addAction("&Редактировать", self.edit_remainders,
                                  QtCore.Qt.CTRL + QtCore.Qt.Key_O + QtCore.Qt.Key_R)
        menu_remainders.addAction("&Посмотреть", self.show_remainders,
                                  QtCore.Qt.CTRL + QtCore.Qt.Key_S + QtCore.Qt.Key_O)

    def add_product(self):
        dialog: QDialog = QDialog(self)
        dialog.ui = UiProductInfo(dialog, self.db_worker)
        dialog.ui.setup_ui(dialog)
        dialog.show()

    def add_increment(self):
        product_id = self.chosen_product.product_id
        quantity = self.add_increment_widget.quantity_value.value()
        mdate = self.add_increment_widget.otherday_edit.date().toPyDate()
        price = self.add_increment_widget.price_value.value()
        agreement_info = self.add_increment_widget.agreement_info.toPlainText()
        invoice_info = self.add_increment_widget.invoice_info.toPlainText()
        self.db_worker.add_changing(
            product_id,
            quantity,
            mdate=mdate,
            price=price,
            agreement_info=agreement_info,
            invoice_info=invoice_info
        )
        self.stm.select()

    def add_decrement(self):
        product_id = self.chosen_product.product_id
        if self.add_decrement_widget.quantity_checker.isChecked():
            decrement = (
                    self.add_decrement_widget.quantity_value.value() * self.child_count
            )
        else:
            decrement = self.add_decrement_widget.quantity_value.value()
        mdate = self.add_decrement_widget.otherday_edit.date().toPyDate()
        self.db_worker.add_changing(
            product_id,
            decrement=decrement,
            mdate=mdate
        )
        self.stm.select()

    def add_row(self):
        rec = self.con.record('changings')
        rec.setValue('product_id', self.chosen_product.product_id)
        rec.setValue('unit', self.chosen_product.product_unit)
        rec.setValue('date', date.today().strftime("%d-%m-%Y"))
        rec.setValue('price', 0)
        rec.setValue('increment', 0)
        rec.setValue('decrement', 0)
        self.stm.insertRowIntoTable(rec)
        self.stm.submitAll()
        self.stm.select()

    def delete_row(self):
        self.stm.removeRow(self.table.currentIndex().row())
        self.stm.select()

    def load_changings(self):
        self.stm.setTable('changings')
        self.stm.setSort(1, QtCore.Qt.DescendingOrder)
        self.stm.setFilter(f"product_id = {self.chosen_product.product_id}")
        self.stm.select()
        self.stm.setHeaderData(1, QtCore.Qt.Horizontal, "Дата")
        self.stm.setHeaderData(2, QtCore.Qt.Horizontal, "Доверенность")
        self.stm.setHeaderData(3, QtCore.Qt.Horizontal, "Счёт-фактура")
        self.stm.setHeaderData(4, QtCore.Qt.Horizontal, "Цена")
        self.stm.setHeaderData(5, QtCore.Qt.Horizontal, "Приход")
        self.stm.setHeaderData(6, QtCore.Qt.Horizontal, "Расход")
        self.stm.setHeaderData(7, QtCore.Qt.Horizontal, "Остаток")
        self.stm.setHeaderData(8, QtCore.Qt.Horizontal, "ед. изм")
        self.table.setModel(self.stm)
        self.table.hideColumn(0)
        self.table.hideColumn(9)
        self.table.setItemDelegateForColumn(1, DateDelegate())

    def ask_child_count(self):
        dialog = QDialog(self)
        dialog.ui = ChildCountUi(dialog)
        dialog.ui.setupUi(dialog)
        dialog.show()

    def load_child_count(self):
        try:
            value = self.db_worker.get_child_count()
        except AssertionError:
            today = date.today()
            if today.weekday() < week_lim:
                self.ask_child_count()
            else:
                self.child_count_label.hide()
        else:
            self.child_count_is_known = True
            self.child_count_label.setText(f'Кол-во детей:{value:4}')

    def change_product(self, btn: ProductButton):
        self.chosen_product.setObjectName("")
        self.chosen_product = btn
        btn.setObjectName("chosenProductButton")
        self.table_title.setText(centralize_text(btn.text()))
        self.setStyleSheet(css_style)
        self.load_changings()

    def load_ui(self):
        self.pbc.setObjectName("pbc_layout")
        products = self.db_worker.get_products_by_fields(['id', 'name', 'unit'])
        for product in products:
            self.product_buttons.append(
                ProductButton(
                    parent=self.pbcw, product_id=product[0],
                    product_name=product[1],
                    product_unit=product[2]
                )
            )
        for pr_button in self.product_buttons:
            pr_button.clicked.connect(self.change_product)
            self.pbc.addWidget(pr_button)
        self.load_child_count()
        spacer_item1 = QSpacerItem(
            0, 0, QSizePolicy.Expanding, QSizePolicy.Minimum
        )
        spacer_item2 = QSpacerItem(
            0, 0, QSizePolicy.Minimum, QSizePolicy.Expanding
        )
        self.pbcw.setMaximumWidth(170)
        self.pbcwg.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.pbc.setObjectName("pbc_layout")
        self.pbc.setContentsMargins(2, 0, 10, 0)
        self.control_buttons_row.addItem(spacer_item1)
        self.control_buttons_row.addWidget(self.add_row_button)
        self.control_buttons_row.addWidget(self.delete_row_button)
        self.table_title_layout.addWidget(self.table_title)
        self.table_title_layout.addWidget(self.table)
        self.labels_increment_decrement_column.addWidget(self.date_label)
        self.labels_increment_decrement_column.addWidget(self.child_count_label)
        self.labels_increment_decrement_column.addWidget(self.add_increment_widget)
        self.labels_increment_decrement_column.addWidget(self.add_decrement_widget)
        self.pbc.addItem(spacer_item2)
        self.labels_increment_decrement_column.addItem(spacer_item2)
        self.table_labels_row.addLayout(self.table_title_layout)
        self.table_labels_row.addWidget(self.pbcw)
        self.table_labels_row.addLayout(self.labels_increment_decrement_column)
        self.main_layout.addLayout(self.table_labels_row)
        # self.main_layout.addLayout(self.control_buttons_row)
        self.central_widget.setLayout(self.main_layout)
        self.setCentralWidget(self.central_widget)
