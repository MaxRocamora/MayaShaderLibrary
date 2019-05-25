# -*- coding: utf-8 -*-
# --------------------------------------------------------------------------------------------
#
# ARCANE Shader Library addCategory dialog
# This class ask handles adding a new category
#
# --------------------------------------------------------------------------------------------

from PySide2 import QtWidgets
from ... import ARCANE_LIBRARY_SHADERS_PATH
from ..category import Category


class addCategoryDialog():
    libPath = ARCANE_LIBRARY_SHADERS_PATH
    msgStr = {
        'NewCatUnicodeError': 'UnicodeEncodeError!.',
        'NewCatNameLenghtError': 'New Category name needs at least 4 characters length.',
        'NewCatNameExist': 'Category name already in use.'
    }

    def __init__(self, observer):
        '''
        Add Category Class
        Args:
            observer (class) observer holding ui/category
        '''
        self.ui = observer.ui
        self.category = observer.selectedCategory
        self.name = 'defaultCategory'

        userInput = self.newCategoryDialog()
        if userInput:
            Category.create(userInput)
            self.ui.categoryCC.loadCategorys()

# --------------------------------------------------------------------------------------------
# addShader Support Dialogs
# --------------------------------------------------------------------------------------------

    def existingCategoryDialog(self, name):
        ''' open qt dialog box when shader already exists '''
        msgBox = QtWidgets.QMessageBox(self.ui)
        msgBox.setStyleSheet("background: rgba(40, 40, 40, 255);")
        msgBox.setIcon(QtWidgets.QMessageBox.Question)
        msgBox.setText(self.msgStr['overwriteShaderDialog'])
        msgBox.setWindowTitle(name)
        msgBox.setDetailedText(name)
        msgBox.setStandardButtons(QtWidgets.QMessageBox.Ok | QtWidgets.QMessageBox.Cancel)
        choice = msgBox.exec_()
        return True if choice == QtWidgets.QMessageBox.Ok else False

# --------------------------------------------------------------------------------------------
# Create Category Support Dialogs
# --------------------------------------------------------------------------------------------

    def newCategoryDialog(self):
        ''' open qt dialog box for new category'''
        title = "Add Category"
        question = 'Enter Category Name'
        lineEdit = QtWidgets.QLineEdit.Normal
        QInputDialog = QtWidgets.QInputDialog
        categoryName, result = QInputDialog.getText(self.ui, title, question, lineEdit, "default")
        if result is True:
            try:
                categoryName = str(categoryName)
                categoryName.decode('utf-8')
            except UnicodeEncodeError:
                self.informationDialog(self.msgStr['NewCatUnicodeError'])
                return False
            except UnicodeDecodeError:
                self.informationDialog(self.msgStr['NewCatUnicodeError'])
                return False
            for category in self.ui.observer.categoryList:
                if category.name.upper() == categoryName.upper():
                    self.informationDialog(self.msgStr['NewCatNameExist'])
                    return False
            if len(categoryName) <= 3:
                self.informationDialog(self.msgStr['NewCatNameLenghtError'])
                return False
            else:
                return categoryName
        else:
            return False

    def informationDialog(self, msg):
        ''' open qt dialog box when no shader is selected or found'''
        msgBox = QtWidgets.QMessageBox(self.ui)
        msgBox.setStyleSheet("background: rgba(40, 40, 40, 255);")
        msgBox.setIcon(QtWidgets.QMessageBox.Warning)
        msgBox.setText(msg)
        msgBox.setWindowTitle("Adding Category")
        msgBox.setStandardButtons(QtWidgets.QMessageBox.Close)
        msgBox.exec_()
