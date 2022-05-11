# ----------------------------------------------------------------------------------------
# Maya Shader Library
# Author: maxirocamora@gmail.com
# https://github.com/MaxRocamora/MayaShaderLibrary
#
# Shader Category Controller
# Controller for category related methods.
# --------------------------------------------------------------------------------------------

import os
from PySide2 import QtCore, QtWidgets

from msl.config import LIBRARY_SHADERS_PATH
from msl.libs.shader_generator import generate_shader_buttons
from msl.libs.category import Category
from msl.libs.dialogs.dlg_add_category import AddCategoryDialog
from msl.ui.icons import get_icon
from msl.libs.logger import log

msg = {
    'CategoryNotFound': 'No Categories found, create one using the Create Category button',
    'LibraryFolderNotFound': 'Library Folder not found!'
}


class CategoryController():

    def __init__(self, main, observer):
        self.main = main
        self.ui = main.ui
        self.observer = observer
        self.set_connections()

    def set_connections(self):
        ''' Definition for ui widgets qt signals & attributes '''
        self.ui.mnu_browse_category_folder.triggered.connect(
            lambda: self.selected_category().browse())
        self.ui.mnu_reload_categories.triggered.connect(self.load_categories)
        self.ui.cbox_categories.activated.connect(
            lambda: self.focus_tab(self.ui.cbox_categories.currentText()))

        self.ui.btn_favorite.clicked.connect(self.pin_tab)
        self.ui.btn_favorite.setIcon(get_icon("pin"))
        self.ui.btn_favorite.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.ui.btn_favorite.setAttribute(
            QtCore.Qt.WA_TranslucentBackground)
        self.ui.btn_favorite.setStyleSheet("background:transparent;")
        self.ui.btn_favorite.installEventFilter(self.ui)
        self.ui.btn_unpin.clicked.connect(self.unpin_tab)
        self.ui.btn_unpin.setIcon(get_icon("delete"))
        self.ui.btn_unpin.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.ui.btn_unpin.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.ui.btn_unpin.setStyleSheet("background:transparent;")
        self.ui.btn_unpin.installEventFilter(self.ui)

        self.ui.btn_browse_category.clicked.connect(
            lambda: self.selected_categories.browse())
        self.ui.btn_browse_category.setIcon(get_icon("browse"))
        self.ui.btn_browse_category.setWindowFlags(
            QtCore.Qt.FramelessWindowHint)
        self.ui.btn_browse_category.setAttribute(
            QtCore.Qt.WA_TranslucentBackground)
        self.ui.btn_browse_category.setStyleSheet("background:transparent;")
        self.ui.btn_browse_category.installEventFilter(self.ui)

        self.ui.mnu_add_new_category.triggered.connect(self.add_category_call)
        self.ui.btn_add_category.setIcon(get_icon("add"))
        self.ui.btn_add_category.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.ui.btn_add_category.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.ui.btn_add_category.setStyleSheet("background:transparent;")
        self.ui.btn_add_category.installEventFilter(self.ui)
        self.ui.btn_add_category.clicked.connect(self.add_category_call)

        self.ui.tab_materials.currentChanged.connect(self.tab_changed)

    def load_categories(self):
        ''' Load Categories from disk and set up main storing list '''
        self.observer.categories = Category.collect_categories(self.ui)
        if not self.observer.categories:
            self.main.status_bar.warning(msg['CategoryNotFound'])
        else:
            self.ui.cbox_categories.clear()
            for category in self.observer.categories:
                self.ui.cbox_categories.addItem(category.name())
            self.ui.cbox_categories.activated.emit(1)

    def add_category_call(self):
        ''' Calls for addCategoryDialog '''
        AddCategoryDialog(self.observer)

    def selected_category(self):
        ''' alias for current selected category class'''
        return self.observer.selected_category

    def current_category_tab(self):
        ''' returns name of current category tab selected '''
        index = self.ui.tab_materials.currentIndex()
        return self.ui.tab_materials.tabText(index)

    # ------------------------------------------------------------------------------------
    # UI METHODS
    # ------------------------------------------------------------------------------------

    def tab_changed(self):
        ''' focus category when user changes tab '''
        index = self.ui.tab_materials.currentIndex()
        if index < 0:
            self.observer.selected_category = False
            return

        name = self.ui.tab_materials.tabText(index)
        for category in self.observer.categories:
            if category.name() == name:
                self.observer.selected_category = category
                break

    def focus_category(self, index):
        ''' forces a focus on category index, both tab and cbox '''
        self.ui.tab_materials.setCurrentIndex(index)

    def focus_tab(self, name):
        ''' forces a focus on category tab by name '''
        for index in range(self.ui.tab_materials.count()):
            if name == self.ui.tab_materials.tabText(index):
                self.ui.tab_materials.setCurrentIndex(index)

    def pin_tab(self, use_category=False):
        ''' Add selected category to main tab panel (pin tab)
        Args:
            use_category (class)
                if true uses given category data
                if false uses current cbox category
        '''
        new_tab = QtWidgets.QWidget(self.ui.tab_materials)
        index = self.ui.cbox_categories.currentIndex()
        category = use_category or self.observer.categories[index]

        path = os.path.join(LIBRARY_SHADERS_PATH, category.name())
        if not os.path.exists(path):
            log.warning('Input Tab name not found on disk', category.name())
            return False

        # Skipping and focusing tab if already exists
        for index in range(self.ui.tab_materials.count()):
            if category.name() == self.ui.tab_materials.tabText(index):
                self.focus_category(index)
                return

        # Creating, focus & Fill Tab
        self.ui.tab_materials.addTab(new_tab, category.name())
        tab = self.ui.tab_materials.widget(self.ui.tab_materials.count() - 1)
        self.ui.tab_materials.setCurrentWidget(tab)
        self.fill_category(tab, category)

    def unpin_tab(self):
        ''' removes current active tab from ui '''
        self.ui.tab_materials.remove_tab(self.ui.tab_materials.currentIndex())

    # ------------------------------------------------------------------------------------
    # LOAD & FILL METHODS
    # ------------------------------------------------------------------------------------

    def fill_category(self, tab, category):
        ''' Fills current tab with shaders buttons
        Args:
            tab (qtWidget) qt tab to fill
            category (class) category object
        '''
        widget = QtWidgets.QWidget()
        layout = QtWidgets.QGridLayout(widget)
        layout.setSpacing(5)
        layout.setHorizontalSpacing(5)
        layout.setVerticalSpacing(5)
        layout.setContentsMargins(2, 2, 2, 2)
        layout.setAlignment(QtCore.Qt.AlignTop)
        scroll = QtWidgets.QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        scroll.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        scroll.setWidget(widget)
        generate_shader_buttons(category.shaders(), self.observer, layout, 4)
        grid = QtWidgets.QGridLayout()
        grid.addWidget(scroll, 3, 0)
        tab.setLayout(grid)

    def refresh_category_tab(self):
        ''' Reload current category tab,
        use this method when a shader is added or renamed.
        '''
        _category = self.selected_category()
        if not _category:
            log.info('No Category Selected!')
            return

        index = self.ui.tab_materials.currentIndex()
        self.ui.tab_materials.removeTab(index)
        new_tab = QtWidgets.QWidget(self.ui.tab_materials)
        self.ui.tab_materials.addTab(new_tab, _category.name())
        tab = self.ui.tab_materials.widget(self.ui.tab_materials.count() - 1)
        self.ui.tab_materials.setCurrentWidget(tab)

        widget = QtWidgets.QWidget()
        layout = QtWidgets.QGridLayout(widget)
        layout.setSpacing(5)
        layout.setHorizontalSpacing(5)
        layout.setVerticalSpacing(5)
        layout.setContentsMargins(2, 2, 2, 2)
        layout.setAlignment(QtCore.Qt.AlignTop)
        scroll = QtWidgets.QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        scroll.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        scroll.setWidget(widget)

        new_shaders = _category.shaders(_reload=True)
        generate_shader_buttons(new_shaders, self.observer, layout, 4)

        grid = QtWidgets.QGridLayout()
        grid.addWidget(scroll, 3, 0)
        tab.setLayout(grid)
        log.info(f'Category {_category.name()} refreshed')
