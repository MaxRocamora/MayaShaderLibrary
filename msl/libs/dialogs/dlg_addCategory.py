# -*- coding: utf-8 -*-
# --------------------------------------------------------------------------------------------
# Shader Library addCategory dialog
# This class ask handles adding a new category
# --------------------------------------------------------------------------------------------

from PySide2 import QtWidgets
from msl.libs.category import Category
from msl.libs.dialogs.dlg_inform import informationDialog

msgStr = {
    'newUnicodeError': 'UnicodeEncodeError!.',
    'newNameLengthError': 'New Category name needs at least 4 characters.',
    'newNameExist': 'Category name already in use.'
}


class addCategoryDialog():

    def __init__(self, observer):
        ''' Add Category Class
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
        msgBox.setStandardButtons(
            QtWidgets.QMessageBox.Ok | QtWidgets.QMessageBox.Cancel)
        choice = msgBox.exec_()
        return choice == QtWidgets.QMessageBox.Ok

# --------------------------------------------------------------------------------------------
# Create Category Support Dialogs
# --------------------------------------------------------------------------------------------

    def newCategoryDialog(self):
        ''' open qt dialog box for new category'''
        title = "Add Category"
        question = 'Enter Category Name'
        lineEdit = QtWidgets.QLineEdit.Normal
        QInputDialog = QtWidgets.QInputDialog
        name, result = QInputDialog.getText(self.ui,
                                            title,
                                            question,
                                            lineEdit,
                                            "default"
                                            )
        if not result:
            return False

        try:
            name = str(name)
            name.decode('utf-8')
        except (UnicodeEncodeError, UnicodeDecodeError):
            informationDialog(msgStr['newUnicodeError'], self.ui)
            return False

        for category in self.ui.observer.categoryList:
            if category.name.upper() == name.upper():
                informationDialog(msgStr['newNameExist'], self.ui)
                return False

        if len(name) < 3:
            informationDialog(msgStr['newNameLengthError'], self.ui)

        return name
