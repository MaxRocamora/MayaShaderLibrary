# --------------------------------------------------------------------------------------------
# Maya Shader Library
# Author: maxirocamora@gmail.com
#
# Shader Library deleteShader dialog
# This class ask for user confirmation on shader physical disk deletion
# --------------------------------------------------------------------------------------------
from PySide2 import QtWidgets

dlg_title = 'Confirm Deletion'
dlg_msg = 'You are about to delete selected shader files.'


class DeleteShaderDialog():

    def __init__(self, shaderClass, observer):
        '''
        QInput dialog class for user delete shader action
        Args:
            shaderClass (class) shader class calling this input
            observer (class) observer holding ui
        '''
        self.observer = observer
        self.shader = shaderClass

    def __call__(self):
        ''' open qt dialog box for rename shader '''
        msgBox = QtWidgets.QMessageBox(self.observer.ui)
        msgBox.setWindowTitle(dlg_title)
        msgBox.setStandardButtons(
            QtWidgets.QMessageBox.Ok | QtWidgets.QMessageBox.Cancel)
        msgBox.setStyleSheet("background: rgba(40, 40, 40, 255);")
        msgBox.setIcon(QtWidgets.QMessageBox.Warning)
        msgBox.setText(dlg_msg)
        choice = msgBox.exec_()
        if choice == QtWidgets.QMessageBox.Ok:
            self.shader.delete()
            self.observer.main.categoryCC.refreshCategoryTab()
