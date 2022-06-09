# ----------------------------------------------------------------------------------------
# Maya Shader Library
# Author: maxirocamora@gmail.com
# https://github.com/MaxRocamora/MayaShaderLibrary
#
# Shader Library: addCategory dialog
# This class handles adding a new category
# ----------------------------------------------------------------------------------------

from PySide2 import QtWidgets

from msl.libs.category import Category
from msl.libs.qt_dialogs import warning_message
from msl.libs.observer import Observer

msg_unicode_error = 'UnicodeEncodeError!.'
msg_name_error = 'New Category name needs at least 4 characters.'
msg_name_exists = 'Category name already in use.'


class AddCategoryDialog():

    def __init__(self):
        ''' Add Category Dialog Class '''
        self.observer = Observer()
        self.category = self.observer.category()

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
        self.observer.set_categories(Category.generate_categories())
        for category in self.observer.categories:
            if category.name() == name:
                category.pin()

    def _new_category_dialog(self):
        ''' open qt dialog box for new category'''
        title = "Add Category"
        question = 'Enter Category Name'
        lineEdit = QtWidgets.QLineEdit.Normal
        QInputDialog = QtWidgets.QInputDialog
        name, result = QInputDialog.getText(None,
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
            warning_message(msg_unicode_error)
            return False

        for category in self.observer.categories():
            if category.name().upper() == name.upper():
                warning_message(msg_name_exists)
                return False

        if len(name) < 3:
            warning_message(msg_name_error)

        return name
