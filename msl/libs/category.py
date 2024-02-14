# ----------------------------------------------------------------------------------------
# Maya Shader Library
# Author: maxirocamora@gmail.com
# https://github.com/MaxRocamora/MayaShaderLibrary
#
# Category Class
#
# ----------------------------------------------------------------------------------------
import os

from PySide2 import QtCore

from msl.libs.observer import Observer

from msl.libs.shader import Shader
from msl.libs.shader_widget import ShaderWidget
from msl.libs.logger import log


class Category:
    def __init__(self, name: str, base_path: str):
        """When a category is created, stores all its shaders."""
        self._name = name
        self._base_path = base_path
        self._shaders = self._collect_shaders()
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

    def path(self) -> str:
        """Physical path of ths shader."""
        return os.path.abspath(os.path.join(self._base_path, self.name()))

    def shaders(self, _reload: bool = False) -> list[Shader]:
        """Returns list of shaders of this category.

        Args:
            _reload (boolean): If true, reload shaders from disk before return
        Returns:
            list: shaders objects
        """
        if _reload:
            self._shaders = self._collect_shaders()
        return self._shaders

    def _collect_shaders(self) -> list[Shader]:
        """Returns a list of shader objects from chosen category."""
        folders = [x.upper() for x in os.listdir(self.path())]
        return [Shader.load_shader(name=f, category=self) for f in folders]

    # ------------------------------------------------------------------------------------
    # Qt UI Grid Methods
    # ------------------------------------------------------------------------------------

    def focus(self):
        """Fills category tab with shaders buttons."""
        self._clear_grid()
        self._fill_shader_layout()
        log.info(f'Focus {self.name()}')

    def _clear_grid(self):
        """Clears shaders UI layout."""
        for i in reversed(range(self.observer.ui.scroll_layout.count())):
            widget = self.observer.ui.scroll_layout.itemAt(i).widget()
            if widget:
                widget.deleteLater()

    def _fill_shader_layout(self, wide: int = 4):
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

                self.observer.ui.scroll_layout.addWidget(
                    shader_widgets[b],
                    row,
                    col,
                    alignment=QtCore.Qt.AlignCenter,
                )

                b += 1
            row += 1

    def reload(self):
        """Rebuilds tab and reload shaders."""
        self.shaders(1)
        self.focus()
