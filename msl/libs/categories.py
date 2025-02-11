# ----------------------------------------------------------------------------------------
# Maya Shader Library
# Author: maxirocamora@gmail.com
# https://github.com/MaxRocamora/MayaShaderLibrary
#
# ----------------------------------------------------------------------------------------
import os

try:
    from PySide2.QtCore import QModelIndex
    from PySide2.QtWidgets import QListWidget, QMainWindow, QMessageBox
except ImportError:
    from PySide6.QtCore import QModelIndex
    from PySide6.QtWidgets import QListWidget, QMainWindow, QMessageBox

from msl.config import LIBRARY_PATH
from msl.libs.category import Category
from msl.libs.logger import log
from msl.libs.qt_dialogs import warning_message
from msl.libs.shader import Shader
from msl.libs.signals import SIGNALS


class CategoryList:
    def __init__(self, list_widget: QListWidget, ui: QMainWindow):
        """Category View Controller."""
        self.list = list_widget
        self.list.setAlternatingRowColors(True)
        self.categories = []
        self.ui = ui

        # connections
        SIGNALS.reload_categories.connect(self.update)
        self.list.clicked.connect(self.item_selected)
        self.ui.btn_add_shader.clicked.connect(self.add_shader_dialog)

    def load_stored_categories(self):
        """Load Categories from disk and set up main storing list."""
        if not os.path.exists(LIBRARY_PATH):
            warning_message('Warning: Categories Folder not found.')
            log.warning(f'Path: {LIBRARY_PATH} not found.')
            return []

        folders = [x.upper() for x in os.listdir(LIBRARY_PATH)]
        if not folders:
            return []

        return [Category(name, LIBRARY_PATH, self.ui) for name in folders]

    def update(self, select_on_update: str = None):
        """Update the view with the given categories list.

        Args:
            select_on_update (str, optional): Category to select after update.
        """
        self._categories = self.load_stored_categories()

        self.list.clear()
        for category in self.get_categories():
            self.list.addItem(category.name())

        if select_on_update:
            for i, category in enumerate(self.get_categories()):
                if category.name() == select_on_update:
                    self.list.setCurrentRow(i)
                    category.focus()
                    break

        SIGNALS.show_message.emit('Categories Updated.')

    def get_categories(self) -> list:
        """Get all categories from the view."""
        return self._categories

    def current_category(self) -> Category:
        """Get the current selected category."""
        index = self.list.currentRow()
        return self._categories[index] if index >= 0 else None

    def item_selected(self, index: QModelIndex):
        """Pin Category when user clicks on it."""
        item = self._categories[index.row()]
        item.focus()

    def add_shader_dialog(self):
        """Adds a new shader."""

        msg_no_category = 'No categories found, create one first.'
        msg_failed_export = 'Add Shader save operation Failed.'

        category = self.current_category()

        if not category:
            warning_message(msg_no_category)
            return

        shader, msg = Shader.get_shader(category)
        if not shader:
            warning_message(msg)
            return

        for s in category.shaders(True):
            if s.name == shader['name']:
                overwrite = self._overwrite_shader_dialog(s.name)
                if not overwrite:
                    return
                break

        new_shader = Shader.create_shader(shader, category)
        if not new_shader.save():
            warning_message(msg_failed_export)
            return

        category.reload()

    def _overwrite_shader_dialog(self, name: str) -> bool:
        """Open qt dialog box when shader already exists."""
        msgBox = QMessageBox(None)
        msgBox.setStyleSheet('background: rgba(40, 40, 40, 255);')
        msgBox.setIcon(QMessageBox.Question)
        msgBox.setText('Shader name already exists, add a new copy?')
        msgBox.setWindowTitle(name)
        msgBox.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
        choice = msgBox.exec_()

        return choice == QMessageBox.Ok
