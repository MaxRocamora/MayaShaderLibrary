from PySide2 import QtWidgets


def input_path_dialog(msg, ui):
    ''' open qt dialog box when no shader is selected or found'''
    msgBox = QtWidgets.QMessageBox(ui)
    msgBox.setStyleSheet("background: rgba(40, 40, 40, 255);")
    msgBox.setIcon(QtWidgets.QMessageBox.Warning)
    msgBox.setText(msg)
    msgBox.setWindowTitle()
    msgBox.setStandardButtons(QtWidgets.QMessageBox.Close)
    msgBox.exec_()
