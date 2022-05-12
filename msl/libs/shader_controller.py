# ----------------------------------------------------------------------------------------
# Maya Shader Library
# Author: maxirocamora@gmail.com
# https://github.com/MaxRocamora/MayaShaderLibrary
#
# Shader Library Controller
# Controller for selected shader related methods.
# ----------------------------------------------------------------------------------------
from PySide2 import QtCore, QtWidgets

from msl.libs.observer import Observer
from msl.libs.shader import Shader
from msl.libs.qt_dialogs import warning_message
from msl.ui.icons import get_icon

msg_no_category = 'No categories found, create one using the Create Category button',
msg_overwrite = 'Shader name already exists, add a new copy?'
msg_failed_export = 'Add Shader save operation Failed.'


class ShaderController():
    def __init__(self, ui):
        self.ui = ui
        self.observer = Observer()
        self.set_connections()

    def set_connections(self):
        '''ui widgets signals & attributes '''
        self.ui.btn_add_shader.clicked.connect(self.add_shader_dialog)
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

    def add_shader_dialog(self):
        ''' adds a new shader '''

        if not self.observer.category():
            warning_message(msg_no_category, self.observer.ui)
            return

        shader, msg = Shader.get_shader(self.observer.category())
        if not shader:
            warning_message(msg, self.observer.ui)
            return

        for s in self.observer.category().shaders(True):
            if s.name == shader['name']:
                overwrite = self._overwrite_shader_dialog(s.name)
                if not overwrite:
                    return
                break

        _shader = Shader.create_shader(shader, self.observer.category())
        if not _shader.save():
            warning_message(msg_failed_export, self.observer.ui)
            return

        self.observer.category_ctrl.refresh_category_tab()

    def _overwrite_shader_dialog(self, name):
        ''' open qt dialog box when shader already exists '''
        msgBox = QtWidgets.QMessageBox(self.observer.ui)
        msgBox.setStyleSheet("background: rgba(40, 40, 40, 255);")
        msgBox.setIcon(QtWidgets.QMessageBox.Question)
        msgBox.setText(msg_overwrite)
        msgBox.setWindowTitle(name)
        msgBox.setStandardButtons(
            QtWidgets.QMessageBox.Ok | QtWidgets.QMessageBox.Cancel)
        choice = msgBox.exec_()
        return choice == QtWidgets.QMessageBox.Ok

    def save_notes(self):
        ''' Saving notes on selected shader '''
        shader = self.observer.shader()
        if shader:
            shader.notes = str(self.ui.te_notes.document().toPlainText())
            shader.save_shader_properties()
