# -*- coding: utf-8 -*-
# --------------------------------------------------------------------------------------------
#
# ARCANE Shader Library deleteShader dialog
# This class ask for user confirmation on shader physical disk deletion
#
# --------------------------------------------------------------------------------------------

from mxr.core import QtWidgets


class deleteShaderDialog():
    msgStr = {
        'title': 'Confirm Deletion',
        'deleteConfirmation': 'You are about to delete shader files.'
    }

    def __init__(self, shaderClass, observer):
        '''
        QInput dialog class for user delete shader action
        Args:
            shaderClass (class) shader class calling this input
            observer (class) observer holding ui
        '''
        self.ui = observer.ui
        self.shader = shaderClass

    def __call__(self):
        ''' open qt dialog box for rename shader '''
        msgBox = QtWidgets.QMessageBox(self.ui)
        msgBox.setWindowTitle(self.msgStr['title'])
        msgBox.setStandardButtons(QtWidgets.QMessageBox.Ok | QtWidgets.QMessageBox.Cancel)
        msgBox.setStyleSheet("background: rgba(40, 40, 40, 255);")
        msgBox.setIcon(QtWidgets.QMessageBox.Warning)
        msgBox.setText(self.msgStr['deleteConfirmation'])
        choice = msgBox.exec_()
        if choice == QtWidgets.QMessageBox.Ok:
            self.shader.delete()
            self.ui.categoryCC.refreshCategoryTab()
