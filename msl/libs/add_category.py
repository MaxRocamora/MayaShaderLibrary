# ----------------------------------------------------------------------------------------
# Maya Shader Library
# Author: maxirocamora@gmail.com
# https://github.com/MaxRocamora/MayaShaderLibrary
#
# Shader Library: addCategory dialog
# This class handles adding a new category
# ----------------------------------------------------------------------------------------
import os

from PySide2 import QtWidgets

from msl.config import LIBRARY_PATH
from msl.libs.qt_dialogs import warning_message
from msl.libs.signals import SIGNALS


class AddCategoryDialog:
    def __init__(self):
        """Add Category Dialog Class."""

        input_name = self._new_category_dialog()
        if input_name:
            name = self.create_category(input_name)
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

    def create_category(self, name: str) -> str:
        """Create category, validates name and create folder."""

        msg_unicode_error = 'UnicodeEncodeError!.'
        msg_name_error = f'New Category {name} needs at least 3 characters.'
        msg_name_exists = f'Category name: {name}, already in use.'

        # string validation
        try:
            name = str(name)
        except (UnicodeEncodeError, UnicodeDecodeError):
            warning_message(msg_unicode_error)
            return

        # name length validation
        if len(name) < 3:
            warning_message(msg_name_error)
            return

        name = name.upper()

        path = os.path.abspath(os.path.join(LIBRARY_PATH, name))

        # name in use validation
        if os.path.exists(path):
            warning_message(msg_name_exists)
            return

        try:
            os.mkdir(path)
        except (OSError, WindowsError) as e:
            warning_message(f'Error Creating folder: {e}')
            return

        return name
