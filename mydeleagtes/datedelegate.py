from PyQt5.QtWidgets import QStyledItemDelegate, QWidget, QDateEdit
from PyQt5.QtCore import QModelIndex, QAbstractItemModel
from PyQt5.QtCore import Qt as QtCoreQt
from datetime import date, datetime


class DateDelegate(QStyledItemDelegate):
    def createEditor(self, parent: QWidget, option, index: QModelIndex) -> QWidget:
        editor = QDateEdit(parent)
        editor.setFrame(False)
        editor.setMinimumDate(date(year=2021, month=1, day=1))
        return editor

    def setEditorData(self, editor: QDateEdit, index: QModelIndex) -> None:
        value = datetime.strptime(index.model().data(index, QtCoreQt.EditRole), '%d-%m-%Y').date()
        editor.setDate(value)

    def updateEditorGeometry(self, editor: QDateEdit, option, index: QModelIndex) -> None:
        editor.setGeometry(option.rect)

    def setModelData(self, editor: QDateEdit, model: QAbstractItemModel, index: QModelIndex) -> None:
        value = editor.date().toPyDate().strftime("%d-%m-%Y")
        model.setData(index, value, QtCoreQt.EditRole)
