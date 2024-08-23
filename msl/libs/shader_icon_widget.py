# ----------------------------------------------------------------------------------------
# Maya Shader Library
# Author: maxirocamora@gmail.com
# https://github.com/MaxRocamora/MayaShaderLibrary
#
# Shader Generator
# Fills layouts with buttons widgets of shaders from the corresponding category
# Holds callback classes for button actions and menus
# ----------------------------------------------------------------------------------------

from PySide2 import QtCore, QtGui
from PySide2.QtWidgets import QFrame, QLabel, QMainWindow, QToolButton, QVBoxLayout

from msl.libs.shader import Shader
from msl.libs.shader_widget_base import ShaderWidgetBase
from msl.resources.css.shader_css import button_css, label_css, shader_css


class ShaderIconWidget(ShaderWidgetBase):
    def __init__(self, shader: Shader, ui: QMainWindow, *args, **kwargs):
        """Shader Icon Widget."""
        super().__init__(shader, ui, *args, **kwargs)

        # setup this widget
        self.setStyleSheet(shader_css)
        self.setMaximumSize(120, 180)

        # add a vertical layout
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(2, 2, 2, 2)
        self.layout.setSpacing(0)

        # q frame
        self.frame = QFrame(self)
        self.frame.setFrameShape(QFrame.StyledPanel)
        self.frame.setFrameShadow(QFrame.Raised)
        self.layout.addWidget(self.frame)

        self.in_layout = QVBoxLayout(self)
        self.in_layout.setContentsMargins(2, 2, 2, 2)
        self.in_layout.setSpacing(0)
        self.frame.setLayout(self.in_layout)

        # add top label
        self.label = QLabel(self.shader.name, self)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setStyleSheet(label_css)
        self.in_layout.addWidget(self.label)

        # main button
        self.button = QToolButton(self)
        self.button.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)
        self.button.setStyleSheet(button_css)
        self.button.setFixedSize(110, 110)
        self.button.setIconSize(QtCore.QSize(80, 80))
        self.button.setIcon(QtGui.QIcon(shader.get_thumbnail()))
        self.button.setText(self.shader.shader_type)
        self.button.clicked.connect(self.selected)
        self.button.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.button.customContextMenuRequested.connect(self.context_menu)
        self.in_layout.addWidget(self.button)
