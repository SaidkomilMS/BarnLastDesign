import sys

from PyQt5.QtWidgets import QApplication

from dbworker import DBWorker
from modifiedclasses.mainwindow import MainWindow


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    app = QApplication([])
    try:
        db_worker = DBWorker()
        main_window = MainWindow(db_worker)
        main_window.showMaximized()
    except Exception as e:
        print(f'{e}')
    else:
        sys.exit(app.exec_())
