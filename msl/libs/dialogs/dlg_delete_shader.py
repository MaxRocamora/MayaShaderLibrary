# ----------------------------------------------------------------------------------------
# Maya Shader Library
# Author: maxirocamora@gmail.com
# https://github.com/MaxRocamora/MayaShaderLibrary
#
# Shader Library deleteShader dialog
# This class ask for user confirmation on shader physical disk deletion
# ----------------------------------------------------------------------------------------
from PySide2 import QtWidgets

from msl.libs.observer import Observer

dlg_title = 'Confirm Deletion'
dlg_msg = 'You are about to delete selected shader files.'


class DeleteShaderDialog():

    def __init__(self, _shader):
        '''
        QInput dialog class for user delete shader action
        Args:
            _shader (class) shader class calling this input
        '''
        self.observer = Observer()
        self.shader = _shader

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
            self.shader.category.reload()
