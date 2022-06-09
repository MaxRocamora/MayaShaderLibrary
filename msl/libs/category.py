# ----------------------------------------------------------------------------------------
# Maya Shader Library
# Author: maxirocamora@gmail.com
# https://github.com/MaxRocamora/MayaShaderLibrary
#
# Category Class
#
# ----------------------------------------------------------------------------------------
import os
from PySide2 import QtCore, QtWidgets

from msl.config import LIBRARY_SHADERS_PATH
from msl.libs.observer import Observer
from msl.libs.qt_dialogs import warning_message
from msl.libs.shader import Shader as Shader
from msl.libs.shader_generator import generate_shader_buttons
from msl.libs.logger import log


class Category():
    def __init__(self, name: str, base_path: str):
        ''' When a category is created, stores all its shaders '''
        self._name = name
        self._base_path = base_path
        self._shaders = self._collect_shaders()
        self._pinned = False
        self._index = -1
        self.observer = Observer()

    def __str__(self):
        return f"Category: {self.name()}"

    def name(self):
        return self._name

    def path(self):
        ''' physical path of ths shader '''
        return os.path.abspath(os.path.join(self._base_path, self.name()))

    def shaders(self, _reload: bool = False):
        ''' Returns list of shaders of this category
        Args:
            _reload (boolean): If true, reload shaders from disk before return
        Returns:
            list: shaders objects
        '''
        if _reload:
            self._shaders = self._collect_shaders()
        return self._shaders

    def pinned(self):
        ''' ui pin state '''
        return self._pinned

    def index(self):
        ''' tab index'''
        return self._index

    def _collect_shaders(self):
        ''' Returns a list of shader objects from chosen category '''
        folders = [x.upper() for x in os.listdir(self.path())]
        return [Shader.load_shader(name=f, category=self) for f in folders]

    # ------------------------------------------------------------------------------------
    # Static Methods
    # ------------------------------------------------------------------------------------

    @staticmethod
    def create(name):
        ''' create category folder '''
        if os.path.exists(LIBRARY_SHADERS_PATH):
            os.mkdir(os.path.abspath(os.path.join(LIBRARY_SHADERS_PATH, name)))

    @staticmethod
    def generate_categories():
        ''' Load Categories from disk and set up main storing list '''
        if not os.path.exists(LIBRARY_SHADERS_PATH):
            warning_message("Warning: Categories Folder not found.")
            log.warning('Path:', LIBRARY_SHADERS_PATH)
            return []

        folders = [x.upper() for x in os.listdir(LIBRARY_SHADERS_PATH)]
        if not folders:
            return []

        return [Category(name, LIBRARY_SHADERS_PATH) for name in folders]

    # ------------------------------------------------------------------------------------
    # Qt UI Methods
    # ------------------------------------------------------------------------------------

    def fill_tab(self):
        ''' Fills category tab with shaders buttons '''
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
        generate_shader_buttons(self.shaders(), self.observer, layout, 4)
        grid = QtWidgets.QGridLayout()
        grid.addWidget(scroll, 3, 0)
        self.tab.setLayout(grid)

    def pin(self):
        ''' Add selected category to main tab panel (pin tab)
        Args:
            use_category (class)
                if true uses given category data
                if false uses current cbox category
        '''

        if self.pinned():
            return

        # tab stores widget
        log.info(f'Pin {self.name()}')
        self.tab = QtWidgets.QWidget(self.observer.ui.tab_materials)

        # Creating, focus & Fill Tab
        self.observer.ui.tab_materials.addTab(self.tab, self.name())
        self._index = self.observer.ui.tab_materials.count() - 1
        last_tab = self.observer.ui.tab_materials.widget(self.index())
        self.observer.ui.tab_materials.setCurrentWidget(last_tab)
        self._pinned = True
        self.fill_tab()

    def unpin(self):
        log.info(f'UnPin {self.name()}')
        self.observer.ui.tab_materials.removeTab(self.index())
        self._pinned = False

    def focus(self):
        ''' forces a focus on tab '''
        self.observer.ui.tab_materials.setCurrentIndex(self.index())

    def reload(self):
        ''' rebuilds tab and reload shaders '''
        self.unpin()
        self.shaders(1)
        self.pin()
