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
from msl.libs.signals import SIGNALS


class AddCategoryDialog:
    def __init__(self):
        """Add Category Dialog Class."""

        input_name = self._new_category_dialog()
        if input_name:
            name = Category.create(input_name)
            if name:
                SIGNALS.reload_categories.emit(name)

    def _new_category_dialog(self):
        """Open qt dialog box for new category."""
        title = 'Add Category'
        question = 'Enter Category Name'
        lineEdit = QtWidgets.QLineEdit.Normal
        QInputDialog = QtWidgets.QInputDialog
        name, result = QInputDialog.getText(None, title, question, lineEdit, 'default')
        if not result:
            return False

        return name
