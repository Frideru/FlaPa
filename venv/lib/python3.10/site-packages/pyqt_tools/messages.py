import sys

from PyQt5 import QtCore
from PyQt5.QtWidgets import QMessageBox, QApplication


def show_message(text, title, icon, buttons=QMessageBox.Ok):
    # We can not create multiple instances, so we check if an instance exists
    instance = QtCore.QCoreApplication.instance()
    if instance is None:
        app = QApplication(sys.argv)

    msg = QMessageBox()
    msg.setIcon(icon)

    msg.setText(text)
    msg.setWindowTitle(title)
    msg.setStandardButtons(buttons)

    msg.show()

    if instance is None:
        return app.exec_()
    else:
        return msg.exec_()


def show_fatal(text, title):
    return show_message(text, title, QMessageBox.Critical)
