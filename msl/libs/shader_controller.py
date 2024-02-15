# ----------------------------------------------------------------------------------------
# Maya Shader Library
# Author: maxirocamora@gmail.com
# https://github.com/MaxRocamora/MayaShaderLibrary
#
# Shader Library Controller
# Controller for selected shader related methods.
# ----------------------------------------------------------------------------------------
from PySide2 import QtCore, QtWidgets

from msl.libs.shader import Shader
from msl.libs.signals import SIGNALS
from msl.resources.icons import get_icon


class ShaderController:
    def __init__(self, ui: QtWidgets.QWidget):
        """Shader Controller."""
        self.ui = ui
        self.active_shader = None
        self.set_connections()

    def set_connections(self):
        """Ui widgets signals & attributes."""
        self.ui.btn_save_changes.clicked.connect(self.save_notes)
        self.ui.btn_save_changes.setIcon(get_icon('save'))
        self.ui.btn_save_changes.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.ui.btn_save_changes.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.ui.btn_save_changes.setStyleSheet('background:transparent;')
        self.ui.btn_save_changes.installEventFilter(self.ui)
        SIGNALS.update_shader_ui.connect(self.update_ui)
        SIGNALS.active_shader.connect(self.set_active_shader)

    def _overwrite_shader_dialog(self, name: str) -> bool:
        """Open qt dialog box when shader already exists."""
        msgBox = QtWidgets.QMessageBox(None)
        msgBox.setStyleSheet('background: rgba(40, 40, 40, 255);')
        msgBox.setIcon(QtWidgets.QMessageBox.Question)
        msgBox.setText('Shader name already exists, add a new copy?')
        msgBox.setWindowTitle(name)
        msgBox.setStandardButtons(QtWidgets.QMessageBox.Ok | QtWidgets.QMessageBox.Cancel)
        choice = msgBox.exec_()

        return choice == QtWidgets.QMessageBox.Ok

    def set_active_shader(self, shader: Shader):
        """Set active shader."""
        print('set_active_shader', shader, type(shader))
        self.active_shader = shader

    def save_notes(self):
        """Saving notes on selected shader."""
        if self.active_shader:
            self.active_shader.notes = str(self.ui.te_notes.document().toPlainText())
            self.active_shader.save_shader_properties()
            SIGNALS.show_message.emit('Notes saved!')

    def update_ui(self, name: str, shader_type: str, notes: str, id_name: str):
        """Update UI with selected shader info."""
        self.ui.lbl_shader_name.setText(name)
        self.ui.lbl_shader_type.setText(shader_type)
        self.ui.te_notes.setText(notes)
        self.ui.lbl_shader_code.setText(id_name)
