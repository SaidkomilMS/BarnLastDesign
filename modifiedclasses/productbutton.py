from PyQt5.QtWidgets import QPushButton, QWidget
from PyQt5 import QtCore


class ProductButton(QPushButton):
    clicked = QtCore.pyqtSignal(QPushButton)

    def __init__(self, parent: QWidget=None, **kwargs):
        QPushButton.__init__(self, parent)
        self.setText(kwargs['product_name'])
        self.product_name = kwargs['product_name']
        self.product_id = kwargs['product_id']
        self.product_unit = kwargs['product_unit']

    def mousePressEvent(self, e) -> None:
        self.clicked.emit(self)
        QPushButton.mousePressEvent(self, e)
