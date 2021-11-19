# --------------------------------------------------------------------------------------------
# Maya Shader Library
# Author: maxirocamora@gmail.com
#
# Shader Library: addCategory dialog
# This class handles adding a new category
# --------------------------------------------------------------------------------------------

from PySide2 import QtWidgets

from msl.libs.category import Category
from msl.libs.dialogs.dlg_inform import informationDialog

msg_unicode_error = 'UnicodeEncodeError!.'
msg_name_error = 'New Category name needs at least 4 characters.'
msg_name_exists = 'Category name already in use.'


class addCategoryDialog():

    def __init__(self, observer):
        ''' Add Category Dialog Class
        Args:
            observer (class) observer holding ui/category
        '''
        self.observer = observer
        self.ui = observer.ui
        self.category = observer.selectedCategory
        self.name = 'defaultCategory'

        name = self._new_category_dialog()
        if name:
            self.create_and_pin_category(name)

    def create_and_pin_category(self, name):
        '''creates and pin new category

        Args:
            name (str): category name
        '''
        name = name.upper()
        Category.create(name)
        self.observer.main.categoryCC.loadCategorys()
        for category in self.observer.categoryList:
            if category.name == name:
                self.observer.main.categoryCC.pinTab(category)

    def _new_category_dialog(self):
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
        except (UnicodeEncodeError, UnicodeDecodeError):
            informationDialog(msg_unicode_error, self.ui)
            return False

        for category in self.observer.categoryList:
            if category.name.upper() == name.upper():
                informationDialog(msg_name_exists, self.ui)
                return False

        if len(name) < 3:
            informationDialog(msg_name_error, self.ui)

        return name
