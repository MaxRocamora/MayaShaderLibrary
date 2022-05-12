# ----------------------------------------------------------------------------------------
# Maya Shader Library
# Author: maxirocamora@gmail.com
# https://github.com/MaxRocamora/MayaShaderLibrary
#
# Shader Category Controller
# Controller for category related methods.
# ----------------------------------------------------------------------------------------

from PySide2 import QtCore, QtWidgets

from msl.libs.observer import Observer
from msl.libs.shader_generator import generate_shader_buttons
from msl.libs.category import Category
from msl.libs.dialogs.dlg_add_category import AddCategoryDialog
from msl.ui.icons import get_icon
from msl.libs.logger import log


class CategoryController():

    def __init__(self, main):
        self.ui = main.ui
        self.observer = Observer()
        self.set_connections()

    def set_connections(self):
        '''ui widgets signals & attributes '''
        self.ui.mnu_browse_category_folder.triggered.connect(
            lambda: self.selected_category().explore())
        self.ui.mnu_reload_categories.triggered.connect(self.load_categories)
        self.ui.cbox_categories.activated.connect(
            lambda: self.focus_tab(self.ui.cbox_categories.currentText()))
        self.ui.mnu_add_new_category.triggered.connect(self.add_category_call)
        self._style_button(self.ui.btn_pin_cat, 'pin', self.pin_tab)
        self._style_button(self.ui.btn_unpin_cat, 'delete', self.unpin_tab)
        self._style_button(self.ui.btn_add_cat, 'add', self.add_category_call)
        self.ui.tab_materials.currentChanged.connect(self.tab_changed)

    def _style_button(self, button, icon, method):
        button.setIcon(get_icon(icon))
        button.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        button.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        button.setStyleSheet("background:transparent;")
        button.installEventFilter(self.ui)
        button.clicked.connect(method)

    def load_categories(self):
        ''' Load Categories from disk to ui and observer '''
        self.observer.set_categories(Category.generate_categories(self.ui))
        if self.observer.categories():
            self.ui.cbox_categories.clear()
            for category in self.observer.categories():
                self.ui.cbox_categories.addItem(category.name())
            self.ui.cbox_categories.activated.emit(1)

    def add_category_call(self):
        ''' Calls for addCategoryDialog '''
        AddCategoryDialog(self.observer)

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
            self.observer.select_category(False)
            return

        name = self.ui.tab_materials.tabText(index)
        for category in self.observer.categories():
            if category.name() == name:
                self.observer.select_category(category)
                break

    def focus_category(self, index):
        ''' forces a focus on category index, both tab and cbox '''
        self.ui.tab_materials.setCurrentIndex(index)

    def focus_tab(self, name):
        ''' forces a focus on category tab by name '''
        for index in range(self.ui.tab_materials.count()):
            if name == self.ui.tab_materials.tabText(index):
                self.ui.tab_materials.setCurrentIndex(index)

    def pin_tab(self):
        ''' Add selected category to main tab panel (pin tab) '''
        category = self.observer.categories()[self.ui.cbox_categories.currentIndex()]
        category.pin()

    def unpin_tab(self):
        ''' removes current active tab from ui '''
        category = self.observer.categories()[self.ui.cbox_categories.currentIndex()]
        category.unpin()

    # ------------------------------------------------------------------------------------
    # LOAD & FILL METHODS
    # ------------------------------------------------------------------------------------

    def refresh_category_tab(self):
        ''' Reload current category tab,
        use this method when a shader is added or renamed.
        '''
        _category = self.observer.category()
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
