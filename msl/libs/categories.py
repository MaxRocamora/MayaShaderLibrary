# ----------------------------------------------------------------------------------------
# Maya Shader Library
# Author: maxirocamora@gmail.com
# https://github.com/MaxRocamora/MayaShaderLibrary
#
# ----------------------------------------------------------------------------------------
from PySide2.QtCore import QModelIndex
from PySide2.QtWidgets import QListWidget

from msl.libs.observer import Observer
from msl.libs.category import Category
from msl.libs.signals import SIGNALS


class CategoryList:
    def __init__(self, list_widget: QListWidget):
        """Category View Controller."""
        self.list = list_widget
        self.list.setAlternatingRowColors(True)
        self.observer = Observer()
        self.categories = []

        # connections
        SIGNALS.reload_categories.connect(self.update)
        self.list.clicked.connect(self.item_selected)

    def update(self, select_on_update: str = None):
        """Update the view with the given categories list.

        Args:
            select_on_update (str, optional): Category to select_on_update. Defaults to None.
        """
        self._categories = Category.load_stored_categories()

        self.list.clear()
        for category in self.get_categories():
            self.list.addItem(category.name())

        if select_on_update:
            print(f'select_on_update: {select_on_update}')
            for i, category in enumerate(self.get_categories()):
                if category.name() == select_on_update:
                    self.list.setCurrentRow(i)
                    break

        self.observer.status_message('Categories Loaded from Disk.')

    def get_categories(self) -> list:
        """Get all categories from the view."""
        return self._categories

    def current_category(self) -> Category:
        """Get the current selected category."""
        index = self.list.currentRow()
        if index < 0:
            return None

        return self._categories[index]

    def item_selected(self, index: QModelIndex):
        """Pin Category when user clicks on it."""
        item = self._categories[index.row()]
        item.pin()
