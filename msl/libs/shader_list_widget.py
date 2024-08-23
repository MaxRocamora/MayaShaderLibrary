# ----------------------------------------------------------------------------------------
# Maya Shader Library
# Author: maxirocamora@gmail.com
# https://github.com/MaxRocamora/MayaShaderLibrary
#
# Shader Generator
# Fills layouts with buttons widgets of shaders from the corresponding category
# Holds callback classes for button actions and menus
# ----------------------------------------------------------------------------------------

from PySide2 import QtCore
from PySide2.QtWidgets import QMainWindow, QToolButton, QVBoxLayout

from msl.libs.shader import Shader
from msl.libs.shader_widget_base import ShaderWidgetBase


class ShaderListWidget(ShaderWidgetBase):
    def __init__(self, shader: Shader, ui: QMainWindow, *args, **kwargs):
        """Shader List Widget."""
        super().__init__(shader, ui, *args, **kwargs)

        self.setMaximumSize(260, 32)

        # add a vertical layout
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(2, 2, 2, 2)
        self.layout.setSpacing(0)

        # main button
        self.button = QToolButton(self)
        self.button.setFixedSize(250, 24)
        self.button.setText(self.shader.name)
        self.button.clicked.connect(self.selected)
        self.button.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.button.customContextMenuRequested.connect(self.context_menu)
        self.layout.addWidget(self.button)
