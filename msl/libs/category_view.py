# ----------------------------------------------------------------------------------------
# Maya Shader Library
# Author: maxirocamora@gmail.com
# https://github.com/MaxRocamora/MayaShaderLibrary
#
# ----------------------------------------------------------------------------------------
from PySide2.QtCore import QSize

from msl.libs.category_model import CategoryModel
from msl.libs.observer import Observer
from msl.libs.category import Category


class CategoryView():

    def __init__(self, view):
        self.view = view
        self.observer = Observer()
        self.model = CategoryModel([])
        self.view.setModel(self.model)
        self.view.setAlternatingRowColors(True)
        self.view.setIconSize(QSize(16, 16))

        # connections
        self.view.clicked.connect(self.item_selected)
        self.view.doubleClicked.connect(self.item_selected_double)
        self.observer.ui.tab_materials.currentChanged.connect(self.tab_changed)

    def update_view(self, categories):
        self.model.categories = categories
        self.model.layoutChanged.emit()

    def item_selected(self, index):
        item = self.model.categories[index.row()]
        self.observer.status_bar.info(f'{item} Pinned!')
        self.observer.select_category(item)
        item.pin()
        item.focus()

    def item_selected_double(self, index):
        item = self.model.categories[index.row()]
        self.observer.select_category(item)
        self.observer.status_bar.info(f'{item} UnPinned!')
        item.unpin()

    def load_categories(self):
        ''' Load Categories from disk to ui and observer '''
        self.observer.set_categories(Category.generate_categories())
        self.observer.status_bar.info('Categories Loaded from Disk.')

    def tab_changed(self):
        ''' focus category when user changes tab '''
        index = self.observer.ui.tab_materials.currentIndex()
        if index < 0:
            self.observer.select_category(False)
            return

        for category in self.observer.categories():
            if category.index() == index:
                self.observer.select_category(category)
                break
