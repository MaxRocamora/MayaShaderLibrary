# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------
# Shader Library addShader dialog
# This class ask handles adding a new shader
# ------------------------------------------------------------------------
from PySide2 import QtWidgets

from msl.libs.shader import Shader as Shader

msgStr = {
    'noCategorySelected': 'No categorys tab found, create one using \
    the Create Category button',
    'overwriteShaderDialog': 'Shader name already exists, add a new copy?',
    'failedExport': 'Add Shader save operation Failed.'
}


class addShaderDialog():

    def __init__(self, observer):
        ''' Add Shader Class
        Args:
            observer (class) observer holding ui/category
        '''
        self.ui = observer.ui
        self.category = observer.selectedCategory

        if not self.category:
            self.informationDialog(msgStr['noCategorySelected'])
            return

        shaderData, msg = Shader.getShader(self.category)
        if not shaderData:
            self.informationDialog(msg)
            return

        for s in self.category.shaders(reload=True):
            if s.name == shaderData['name']:
                if not self.overwriteShaderDialog(s.name):
                    return

        virtualShader = Shader.createShader(shaderData, self.category)
        if virtualShader.save():
            self.ui.categoryCC.refreshCategoryTab()
        else:
            self.informationDialog(msgStr['failedExport'])

# --------------------------------------------------------------------------------------------
# addShader Support Dialogs
# --------------------------------------------------------------------------------------------

    def informationDialog(self, msg):
        ''' open qt dialog box when no shader is selected or found'''
        msgBox = QtWidgets.QMessageBox(self.ui)
        msgBox.setStyleSheet("background: rgba(40, 40, 40, 255);")
        msgBox.setIcon(QtWidgets.QMessageBox.Warning)
        msgBox.setText(msg)
        msgBox.setWindowTitle("Adding Shader")
        msgBox.setStandardButtons(QtWidgets.QMessageBox.Close)
        msgBox.exec_()

    def overwriteShaderDialog(self, name):
        ''' open qt dialog box when shader already exists '''
        msgBox = QtWidgets.QMessageBox(self.ui)
        msgBox.setStyleSheet("background: rgba(40, 40, 40, 255);")
        msgBox.setIcon(QtWidgets.QMessageBox.Question)
        msgBox.setText(msgStr['overwriteShaderDialog'])
        msgBox.setWindowTitle(name)
        msgBox.setDetailedText(name)
        msgBox.setStandardButtons(
            QtWidgets.QMessageBox.Ok | QtWidgets.QMessageBox.Cancel)
        choice = msgBox.exec_()
        return choice == QtWidgets.QMessageBox.Ok
