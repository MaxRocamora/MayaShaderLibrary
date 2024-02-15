# --------------------------------------------------------------------------------------------
# Maya Shader Library
# Author: maxirocamora@gmail.com
# https://github.com/MaxRocamora/MayaShaderLibrary
#
# Shader Generator
# Fills layouts with buttons widgets of shaders from the corresponding category
# Holds callback classes for button actions and menus
# --------------------------------------------------------------------------------------------

import os
import subprocess
from contextlib import contextmanager

from PySide2 import QtCore, QtGui
from PySide2.QtWidgets import QInputDialog, QMessageBox, QApplication, QLineEdit
from PySide2.QtWidgets import QMainWindow, QToolButton, QMenu, QAction

from msl.libs.shader import Shader
from msl.libs.logger import log
from msl.libs.qt_dialogs import warning_message
from msl.resources.css.shader_css import button_css
from msl.libs.signals import SIGNALS
from msl.resources.icons import get_icon
from msl.config import thumbnail_default_scene

RND_SCRIPT = os.path.join(os.path.dirname(__file__), 'utils', 'generate_thumbnail.py')
MAYAPY = os.path.join(os.getenv('MAYA_LOCATION'), 'bin', 'mayapy.exe')


class ShaderWidget(QToolButton):
    def __init__(self, shader: Shader, ui: QMainWindow, *args, **kwargs):
        """Shader Widget."""
        super().__init__(*args, **kwargs)
        self._shader = shader
        self.ui = ui
        self.name = shader.name

        # set widget properties
        self.setText(self.name)
        self.setIcon(QtGui.QIcon(shader.get_thumbnail()))
        self.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)
        self.setFixedSize(110, 110)
        self.iconSize()
        self.setIconSize(QtCore.QSize(80, 80))
        self.setStyleSheet(button_css)

        # connect signals
        self.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.context_menu)
        self.clicked.connect(self.selected)

    @property
    def shader(self):
        """Shader object."""
        return self._shader

    def selected(self):
        """Widget clicked callback."""
        SIGNALS.active_shader.emit(self.shader)
        SIGNALS.update_shader_ui.emit(
            f'{self.shader.name}_{self.shader.category.name()}',
            self.shader.shader_type,
            self.shader.notes,
            self.shader.id_name,
        )

    def context_menu(self, _):
        """Widget right click context menu callback."""

        self.menu = QMenu()

        text = f"Import '{self.name}'' into scene"
        action_import = QAction(get_icon('import'), text, self.menu)
        self.menu.addAction(action_import)
        action_import.triggered.connect(lambda: self.shader.import_shader())
        self.menu.addSeparator()

        text = f"Import '{self.name}'' and assign into selection"
        action_import_sel = QAction(get_icon('import'), text, self.menu)
        self.menu.addAction(action_import_sel)
        action_import_sel.triggered.connect(
            lambda: self.shader.import_shader(assign=True)
        )
        self.menu.addSeparator()

        text = f"Rename '{self.name}'"
        action_rename = QAction(get_icon('rename'), text, self.menu)
        self.menu.addAction(action_rename)
        action_rename.triggered.connect(self.rename_shader)
        self.menu.addSeparator()

        text = f"Browse '{self.name}' folder on disk"
        action_browse = QAction(get_icon('browse'), text, self.menu)
        self.menu.addAction(action_browse)
        action_browse.triggered.connect(self.shader.explore)
        self.menu.addSeparator()

        text = f'Generate {self.name} Thumbnail'
        action_thumbnail = QAction(get_icon('thumbnail'), text, self.menu)
        self.menu.addAction(action_thumbnail)
        action_thumbnail.triggered.connect(self.launch_thumbnail)
        self.menu.addSeparator()

        text = f"Delete '{self.name}' from lib"
        action_delete = QAction(get_icon('delete'), text, self.menu)
        self.menu.addAction(action_delete)
        action_delete.triggered.connect(self.delete_shader)
        self.menu.addSeparator()
        self.menu.popup(QtGui.QCursor.pos())

    def rename_shader(self):
        """Open qt dialog box for rename shader."""

        new_name, result = QInputDialog.getText(
            self.ui,
            'Rename Shader',
            'Enter Shader New Name',
            QLineEdit.Normal,
            'default',
        )

        if not result:
            return False

        try:
            new_name = str(new_name)
        except (UnicodeEncodeError, UnicodeDecodeError):
            warning_message('New name has a UnicodeEncodeError!')
            return False

        if len(new_name) <= 3:
            warning_message('New Shader name needs at least 4 characters.')
            return False

        if any(shader.name == new_name for shader in self.shader.category.shaders()):
            warning_message('Shader name already in use.')
            return False

        if self.shader.rename(new_name):
            self.shader.category.reload()

    def delete_shader(self):
        """Open qt dialog box for rename shader."""
        msg = QMessageBox(self.ui)
        msg.setWindowTitle('Confirm Deletion')
        msg.setStandardButtons(QMessageBox.Yes | QMessageBox.Cancel)
        msg.setStyleSheet('background: rgba(40, 40, 40, 255);')
        msg.setIcon(QMessageBox.Warning)
        msg.setWindowIcon(get_icon('app'))
        msg.setText('Delete selected shader files?')
        choice = msg.exec_()
        if choice == QMessageBox.Yes:
            self.shader.delete()
            self.shader.category.reload()

    def launch_thumbnail(self):
        """Launch python script for thumbnail generation.

        Render Command sends the script, the lightRig scene
        used for rendering, the shader maya file,
        and the target png file for the thumbnail.
        """
        maya_file = os.path.abspath(thumbnail_default_scene)
        if not os.path.exists(MAYAPY):
            log.error('mayapy.exe not found.', MAYAPY)
            return

        cmd = ' '.join(
            [MAYAPY, RND_SCRIPT, maya_file, self.shader.cg_file, self.shader.thumbnail]
        )

        with self.wait_cursor():
            process = subprocess.Popen(
                cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT
            )
            output, error = process.communicate()
            log.info(output)
            log.info(error)

        self.setIcon(QtGui.QIcon(self.shader.get_thumbnail()))  # reload thumbnail image

    @contextmanager
    def wait_cursor(self):
        """Context manager for wait cursor."""
        try:
            QApplication.setOverrideCursor(QtGui.QCursor(QtCore.Qt.WaitCursor))
            yield
        finally:
            QApplication.restoreOverrideCursor()
