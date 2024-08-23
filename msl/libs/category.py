# ----------------------------------------------------------------------------------------
# Maya Shader Library
# Author: maxirocamora@gmail.com
# https://github.com/MaxRocamora/MayaShaderLibrary
#
# Category Class
#
# ----------------------------------------------------------------------------------------
import os

from PySide2.QtWidgets import QMainWindow

from msl.config import WidgetViewMode, WidgetViewModeWidth
from msl.libs.logger import log
from msl.libs.shader import Shader
from msl.libs.shader_icon_widget import ShaderIconWidget
from msl.libs.shader_list_widget import ShaderListWidget


class Category:
    def __init__(self, name: str, base_path: str, ui: QMainWindow):
        """When a category is created, stores all its shaders."""
        self._name = name
        self._base_path = base_path
        self.ui = ui
        self._shaders = self._collect_shaders()
        self.widget_view = WidgetViewMode.LIST

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

    def path(self) -> str:
        """Physical path of ths shader."""
        return os.path.abspath(os.path.join(self._base_path, self.name()))

    def switch_widget_view(self):
        """Switches between list and icon widget modality."""
        if self.widget_view == WidgetViewMode.LIST:
            self.widget_view = WidgetViewMode.ICON
        else:
            self.widget_view = WidgetViewMode.LIST

        self.focus()

    def shaders(self, reload: bool = False) -> list:
        """Returns list of shaders of this category.

        Args:
            reload (bool): If true, reload shaders from disk before return
        Returns:
            list: shaders objects
        """
        if reload:
            self._shaders = self._collect_shaders()

        return self._shaders

    def _collect_shaders(self) -> list:
        """Returns a list of shader objects from chosen category."""
        folders = [x.upper() for x in os.listdir(self.path())]
        shaders = [Shader.load_shader(name=f, category=self) for f in folders]
        return sorted(shaders, key=lambda x: x.name)

    def focus(self):
        """Fills category tab with shaders buttons."""
        self._clear_grid()
        self._fill_shader_layout()
        log.info(f'Focus {self.name()}')

    def _clear_grid(self):
        """Clears shaders UI layout."""
        for i in reversed(range(self.ui.scroll_layout.count())):
            widget = self.ui.scroll_layout.itemAt(i).widget()
            if widget:
                widget.deleteLater()

    def _fill_shader_layout(self):
        """Fills given layout with buttons shaders."""

        # how many widgets can fit in a row, based on widget modality
        if self.widget_view == WidgetViewMode.ICON:
            wide = int(self.ui.width() / WidgetViewModeWidth.ICON.value)
            shader_widgets = [
                ShaderIconWidget(shader, self.ui) for shader in self.shaders()
            ]

        if self.widget_view == WidgetViewMode.LIST:
            wide = int(self.ui.width() / WidgetViewModeWidth.LIST.value)
            shader_widgets = [
                ShaderListWidget(shader, self.ui) for shader in self.shaders()
            ]

        index = 0
        row = 0

        while index < len(shader_widgets):
            for column in range(wide):
                if index >= len(shader_widgets):
                    break

                self.ui.scroll_layout.addWidget(shader_widgets[index], row, column)

                index += 1
            row += 1

    def reload(self):
        """Rebuilds tab and reload shaders."""
        self.shaders(reload=True)
        self.focus()
