# --------------------------------------------------------------------------------------------
# Maya Shader Library
#
# Shader Category Controller
# Controller for category related methods.
# --------------------------------------------------------------------------------------------

import os
from PySide2 import QtCore, QtWidgets

from msl import LIBRARY_SHADERS_PATH
from msl.libs.shaderGenerator import generateShaderButtons
from msl.libs.category import Category
from msl.libs.dialogs.dlg_addCategory import addCategoryDialog
from msl.ui.icons import get_icon

msgStr = {
    'CategoryNotFound': 'No Categories found, \
    create one using the Create Category button',
    'LibraryFolderNotFound': 'Library Folder not found!'
}


class CategoryController():

    def __init__(self, main, observer):
        self.main = main
        self.ui = main
        self.observer = observer
        self.set_connections()

    def set_connections(self):
        ''' Definition for ui widgets qt signals & attributes '''
        self.ui.mnu_browseCategoryFolder.triggered.connect(
            lambda: self.selectedCategory.browse())
        self.ui.mnu_reloadCategorys.triggered.connect(self.loadCategorys)
        self.ui.cbox_categorys.activated.connect(
            lambda: self.focusTabName(self.ui.cbox_categorys.currentText()))

        self.ui.btn_favoriteCat.clicked.connect(self.pinTab)
        self.ui.btn_favoriteCat.setIcon(get_icon("pin"))
        self.ui.btn_favoriteCat.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.ui.btn_favoriteCat.setAttribute(
            QtCore.Qt.WA_TranslucentBackground)
        self.ui.btn_favoriteCat.setStyleSheet("background:transparent;")
        self.ui.btn_favoriteCat.installEventFilter(self.ui)
        self.ui.btn_unPinTab.clicked.connect(self.unPinTab)
        self.ui.btn_unPinTab.setIcon(get_icon("delete"))
        self.ui.btn_unPinTab.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.ui.btn_unPinTab.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.ui.btn_unPinTab.setStyleSheet("background:transparent;")
        self.ui.btn_unPinTab.installEventFilter(self.ui)

        self.ui.btn_browseCategory.clicked.connect(
            lambda: self.selectedCategory.browse())
        self.ui.btn_browseCategory.setIcon(get_icon("browse"))
        self.ui.btn_browseCategory.setWindowFlags(
            QtCore.Qt.FramelessWindowHint)
        self.ui.btn_browseCategory.setAttribute(
            QtCore.Qt.WA_TranslucentBackground)
        self.ui.btn_browseCategory.setStyleSheet("background:transparent;")
        self.ui.btn_browseCategory.installEventFilter(self.ui)

        self.ui.mnu_addNewCategory.triggered.connect(self.addCategoryCall)
        self.ui.btn_addCategory.setIcon(get_icon("add"))
        self.ui.btn_addCategory.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.ui.btn_addCategory.setAttribute(
            QtCore.Qt.WA_TranslucentBackground)
        self.ui.btn_addCategory.setStyleSheet("background:transparent;")
        self.ui.btn_addCategory.installEventFilter(self.ui)
        self.ui.btn_addCategory.clicked.connect(self.addCategoryCall)

        self.ui.tab_materials.currentChanged.connect(self.tabChanged)

    def loadCategorys(self):
        ''' Load Categorys from disk and set up main storing list '''
        self.observer.categoryList = Category.collectCategorys(self.ui)
        if len(self.observer.categoryList) == 0:
            self.main.uiBar.warning(msgStr['CategoryNotFound'])
        else:
            self.ui.cbox_categorys.clear()
            for category in self.observer.categoryList:
                self.ui.cbox_categorys.addItem(category.name)
            self.ui.cbox_categorys.activated.emit(1)

    def addCategoryCall(self):
        ''' Calls for addCategoryDialog '''
        addCategoryDialog(self.observer)

# --------------------------------------------------------------------------------------------
# UI PROPERTIES
# --------------------------------------------------------------------------------------------

    @property
    def selectedCategory(self):
        ''' alias for current selected category class'''
        return self.observer.selectedCategory

    def currentCategoryTab(self):
        ''' returns name of current category tab selected '''
        index = self.ui.tab_materials.currentIndex()
        return self.ui.tab_materials.tabText(index)

# --------------------------------------------------------------------------------------------
# UI METHODS
# --------------------------------------------------------------------------------------------

    def tabChanged(self):
        ''' focus category when user changes tab '''
        index = self.ui.tab_materials.currentIndex()
        if index < 0:
            self.observer.selectedCategory = False
            return

        name = self.ui.tab_materials.tabText(index)
        categoryList = self.observer.categoryList
        for category in categoryList:
            if category.name == name:
                self.observer.selectedCategory = category
                break

    def focusCategory(self, index):
        ''' forces a focus on category index, both tab and cbox '''
        self.ui.tab_materials.setCurrentIndex(index)

    def focusTabName(self, name):
        ''' forces a focus on category tab by name '''
        for index in range(self.ui.tab_materials.count()):
            if name == self.ui.tab_materials.tabText(index):
                self.ui.tab_materials.setCurrentIndex(index)

    def pinTab(self, use_category=False):
        ''' Add selected category to main tab panel (pin tab)
        Args:
            use_category (class)
                if true uses given category data
                if false uses current cbox category
        '''
        newTab = QtWidgets.QWidget(self.ui.tab_materials)
        index = self.ui.cbox_categorys.currentIndex()
        category = use_category or self.observer.categoryList[index]

        path = os.path.join(LIBRARY_SHADERS_PATH, category.name)
        if not os.path.exists(path):
            print('Input Tab name not found on disk', category.name)
            return False

        # Skipping and focusing tab if already exists
        for index in range(self.ui.tab_materials.count()):
            if category.name == self.ui.tab_materials.tabText(index):
                self.focusCategory(index)
                return

        # Creating, focus & Fill Tab
        self.ui.tab_materials.addTab(newTab, category.name)
        tab = self.ui.tab_materials.widget(self.ui.tab_materials.count() - 1)
        self.ui.tab_materials.setCurrentWidget(tab)
        self.fillCategory(tab, category)

    def unPinTab(self):
        ''' removes current active tab from ui '''
        self.ui.tab_materials.removeTab(self.ui.tab_materials.currentIndex())

# --------------------------------------------------------------------------------------------
# LOAD & FILL METHODS
# --------------------------------------------------------------------------------------------

    def fillCategory(self, tab, category):
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
        generateShaderButtons(category.shaders(), self.observer, layout, 4)
        grid = QtWidgets.QGridLayout()
        grid.addWidget(scroll, 3, 0)
        tab.setLayout(grid)

    def refreshCategoryTab(self):
        '''
        Reload current category tab, use this method when a shader
        is added or renamed.
        '''
        categoryPlaceHolder = self.selectedCategory
        index = self.ui.tab_materials.currentIndex()
        self.ui.tab_materials.removeTab(index)
        newTab = QtWidgets.QWidget(self.ui.tab_materials)
        self.ui.tab_materials.addTab(newTab, categoryPlaceHolder.name)
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

        shadersUpdated = categoryPlaceHolder.shaders(reload=True)
        generateShaderButtons(shadersUpdated, self.observer, layout, 4)

        grid = QtWidgets.QGridLayout()
        grid.addWidget(scroll, 3, 0)
        tab.setLayout(grid)
        print('Category {} refreshed'.format(categoryPlaceHolder.name))
