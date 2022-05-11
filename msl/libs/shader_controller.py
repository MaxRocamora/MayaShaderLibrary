# ----------------------------------------------------------------------------------------
# Maya Shader Library
# Author: maxirocamora@gmail.com
# https://github.com/MaxRocamora/MayaShaderLibrary
#
# Shader Library Controller
# Controller for selected shader related methods.
# ----------------------------------------------------------------------------------------
from PySide2 import QtCore

from msl.libs.dialogs.dlg_add_shader import AddShaderDialog
from msl.ui.icons import get_icon


class ShaderController():
    def __init__(self, ui, observer):
        self.ui = ui
        self.observer = observer
        self.set_connections()

    def set_connections(self):
        ''' Definition for ui widgets qt signals & attributes '''
        self.ui.btn_add_shader.clicked.connect(self.add_shader_call)
        self.ui.btn_add_shader.setIcon(get_icon("plus"))
        self.ui.btn_add_shader.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.ui.btn_add_shader.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.ui.btn_add_shader.setStyleSheet("background:transparent;")
        self.ui.btn_add_shader.installEventFilter(self.ui)
        self.ui.btn_save_changes.clicked.connect(self.save_notes)
        self.ui.btn_save_changes.setIcon(get_icon("save"))
        self.ui.btn_save_changes.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.ui.btn_save_changes.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.ui.btn_save_changes.setStyleSheet("background:transparent;")
        self.ui.btn_save_changes.installEventFilter(self.ui)

    def add_shader_call(self):
        ''' Calls for addShaderDialog '''
        AddShaderDialog(self.observer)

    def save_notes(self):
        ''' Saving notes on selected shader '''
        shader = self.observer.selected_shader
        if shader:
            shader.notes = str(self.ui.te_notes.document().toPlainText())
            shader.save_shader_properties()
