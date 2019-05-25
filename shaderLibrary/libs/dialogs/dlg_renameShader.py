# -*- coding: utf-8 -*-
# --------------------------------------------------------------------------------------------
#
# ARCANE Shader Library renameShader dialog
#
# This class ask for user a new shader name, and handles errors
#
# --------------------------------------------------------------------------------------------

from mxr.core import QtWidgets


class renameShaderDialog(QtWidgets.QInputDialog):
    msgStr = {
        'shaderNameUnicodeError': 'New name has a UnicodeEncodeError!',
        'shaderNameLenghtError': 'New Shader name needs at least 4 characters length.',
        'shaderNameExist': 'Shader name already in use.',
        'overwriteShaderDialog': 'Shader already exists, overwrite?'
    }

    def __init__(self, shaderClass, observer):
        '''
        QInput dialog class for user rename shader action
        Args:
            shaderClass (class) shader class calling this input
            observer (class) observer holding ui
        '''
        super(renameShaderDialog, self).__init__()
        self.ui = observer.ui
        self.shader = shaderClass

    def __call__(self):
        ''' open qt dialog box for rename shader '''
        title = "Rename Shader"
        question = 'Enter Shader New Name'
        lineEdit = QtWidgets.QLineEdit.Normal
        QInputDialog = QtWidgets.QInputDialog
        newName, result = QInputDialog.getText(self.ui, title, question, lineEdit, "default")
        if result is True:
            try:
                newName = str(newName)
                newName.decode('utf-8')
            except UnicodeEncodeError:
                self.errorShaderDialog(self.msgStr['shaderNameUnicodeError'])
                return False
            except UnicodeDecodeError:
                self.errorShaderDialog(self.msgStr['shaderNameUnicodeError'])
                return False
            if len(newName) <= 3:
                self.errorShaderDialog(self.msgStr['shaderNameLenghtError'])
                return False
            if self.nameInUse(newName):
                self.errorShaderDialog(self.msgStr['shaderNameExist'])
                return False
            else:
                if self.shader.rename(newName):
                    self.ui.categoryCC.refreshCategoryTab()
        else:
            return False

    def errorShaderDialog(self, msg):
        ''' open qt dialog box when no shader is selected or found'''
        msgBox = QtWidgets.QMessageBox(self.ui)
        msgBox.setStyleSheet("background: rgba(40, 40, 40, 255);")
        msgBox.setIcon(QtWidgets.QMessageBox.Warning)
        msgBox.setText(msg)
        msgBox.setWindowTitle("Renaming Shader")
        msgBox.setStandardButtons(QtWidgets.QMessageBox.Close)
        msgBox.exec_()

    def nameInUse(self, name):
        ''' returns true if shader new name is already in use '''
        for shader in self.ui.observer.selectedCategory.shaders():
            if shader.name == name:
                return True
        return False
