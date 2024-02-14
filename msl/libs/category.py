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

from msl.config import LIBRARY_PATH
from msl.libs.observer import Observer
from msl.libs.qt_dialogs import warning_message
from msl.libs.shader import Shader
from msl.libs.shader_widget import ShaderWidget
from msl.libs.logger import log


class Category:
    def __init__(self, name: str, base_path: str):
        """When a category is created, stores all its shaders."""
        self._name = name
        self._base_path = base_path
        self._shaders = self._collect_shaders()
        self._pinned = False
        self._index = -1
        self.observer = Observer()

    def __str__(self) -> str:
        """Returns name of the category."""
        return self.name()

    def __len__(self) -> int:
        """Number of shaders in this category."""
        return len(self.shaders())

    def __bool__(self) -> bool:
        """Returns if category has shaders."""
        return bool(self.name())

    def name(self) -> str:
        """Category name."""
        return self._name

    def path(self):
        """Physical path of ths shader."""
        return os.path.abspath(os.path.join(self._base_path, self.name()))

    def shaders(self, _reload: bool = False):
        """Returns list of shaders of this category.

        Args:
            _reload (boolean): If true, reload shaders from disk before return
        Returns:
            list: shaders objects
        """
        if _reload:
            self._shaders = self._collect_shaders()
        return self._shaders

    def pinned(self):
        """Pin to UI state."""
        return self._pinned

    def index(self):
        """Current tab index."""
        return self._index

    def _collect_shaders(self):
        """Returns a list of shader objects from chosen category."""
        folders = [x.upper() for x in os.listdir(self.path())]
        return [Shader.load_shader(name=f, category=self) for f in folders]

    # ------------------------------------------------------------------------------------
    # Static Methods
    # ------------------------------------------------------------------------------------

    @staticmethod
    def create(name: str) -> str:
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

    @staticmethod
    def load_stored_categories():
        """Load Categories from disk and set up main storing list."""
        if not os.path.exists(LIBRARY_PATH):
            warning_message('Warning: Categories Folder not found.')
            log.warning(f'Path: {LIBRARY_PATH} not found.')
            return []

        folders = [x.upper() for x in os.listdir(LIBRARY_PATH)]
        if not folders:
            return []

        return [Category(name, LIBRARY_PATH) for name in folders]

    # ------------------------------------------------------------------------------------
    # Qt UI Methods
    # ------------------------------------------------------------------------------------

    def fill_tab(self):
        """Fills category tab with shaders buttons."""
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
        self._fill_shader_layout(layout, 4)
        grid = QtWidgets.QGridLayout()
        grid.addWidget(scroll, 3, 0)
        self.tab.setLayout(grid)

    def _fill_shader_layout(self, layout, wide: int):
        """Fills given layout with buttons shaders.

        Args:
            layout (widget): layout widget to fill
            wide (int): maximum columns to split buttons
        """
        shader_widgets = [ShaderWidget(shader) for shader in self.shaders()]
        b = 0
        row = 0
        while b < len(shader_widgets):
            for col in range(wide):
                if b >= len(shader_widgets):
                    break
                layout.addWidget(shader_widgets[b], row, col)
                b += 1
            row += 1

    def pin(self):
        """Add selected category to main tab panel (pin tab)."""

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

    def reload(self):
        """Rebuilds tab and reload shaders."""
        self.unpin()
        self.shaders(1)
        self.pin()
