# ----------------------------------------------------------------------------------------
# Maya Shader Library
# Author: maxirocamora@gmail.com
# https://github.com/MaxRocamora/MayaShaderLibrary
#
# Shader Widget Base Class
# ----------------------------------------------------------------------------------------

import os
import subprocess
from contextlib import contextmanager

try:
    from PySide2 import QtCore
    from PySide2.QtGui import QIcon, QCursor
    from PySide2.QtWidgets import (
        QAction,
        QApplication,
        QInputDialog,
        QLineEdit,
        QMainWindow,
        QMenu,
        QMessageBox,
        QWidget,
    )
except ImportError:
    from PySide6 import QtCore
    from PySide6.QtGui import QAction, QCursor, QIcon
    from PySide6.QtWidgets import (
        QApplication,
        QInputDialog,
        QLineEdit,
        QMainWindow,
        QMenu,
        QMessageBox,
        QWidget,
    )

from msl.config import thumbnail_default_scene
from msl.libs.logger import log
from msl.libs.qt_dialogs import warning_message
from msl.libs.shader import Shader
from msl.libs.signals import SIGNALS
from msl.resources.icons import get_icon

RND_SCRIPT = os.path.join(os.path.dirname(__file__), 'utils', 'generate_thumbnail.py')
MAYAPY = os.path.join(os.getenv('MAYA_LOCATION'), 'bin', 'mayapy.exe')


class ShaderWidgetBase(QWidget):
    def __init__(self, shader: Shader, ui: QMainWindow, *args, **kwargs):
        """Shader Widget."""
        super().__init__(*args, **kwargs)
        self._shader = shader
        self.ui = ui

    @property
    def shader(self):
        """Shader object."""
        return self._shader

    def selected(self):
        """Widget clicked callback."""
        SIGNALS.display_shader_notes.emit(self.shader.notes)

    def context_menu(self, _):
        """Widget right click context menu callback."""

        self.menu = QMenu()

        text = self.shader.id_name
        action_label = QAction(get_icon('mnu_id'), text, self.menu)
        self.menu.addAction(action_label)

        self.menu.addSeparator()

        text = f"Import '{self.shader.name}'' into scene"
        action_import = QAction(get_icon('mnu_import'), text, self.menu)
        self.menu.addAction(action_import)
        action_import.triggered.connect(lambda: self.shader.import_shader())
        self.menu.addSeparator()

        text = f'Import {self.shader.name} and assign into selection'
        action_import_sel = QAction(get_icon('mnu_import_add'), text, self.menu)
        self.menu.addAction(action_import_sel)
        action_import_sel.triggered.connect(lambda: self.shader.import_shader(assign=True))
        self.menu.addSeparator()

        text = f'Rename: {self.shader.name}'
        action_rename = QAction(get_icon('mnu_rename'), text, self.menu)
        self.menu.addAction(action_rename)
        action_rename.triggered.connect(self.rename_shader)
        self.menu.addSeparator()

        text = f'Edit Notes on {self.shader.name}.'
        action_notes = QAction(get_icon('mnu_notes'), text, self.menu)
        self.menu.addAction(action_notes)
        action_notes.triggered.connect(self.edit_notes)
        self.menu.addSeparator()

        text = f"Browse '{self.shader.name}' folder on disk"
        action_browse = QAction(get_icon('mnu_browse'), text, self.menu)
        self.menu.addAction(action_browse)
        action_browse.triggered.connect(self.shader.explore)
        self.menu.addSeparator()

        text = f'Generate {self.shader.name} Thumbnail'
        action_thumbnail = QAction(get_icon('mnu_thumbnail'), text, self.menu)
        self.menu.addAction(action_thumbnail)
        action_thumbnail.triggered.connect(self.launch_thumbnail)
        self.menu.addSeparator()

        text = f"Delete '{self.shader.name}' from lib"
        action_delete = QAction(get_icon('mnu_delete'), text, self.menu)
        self.menu.addAction(action_delete)
        action_delete.triggered.connect(self.delete_shader)
        self.menu.addSeparator()
        self.menu.popup(QCursor.pos())

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

    def edit_notes(self):
        """Edit notes on selected shader."""
        text = self._notes_dialog()
        if text:
            self.shader.edit_notes(text)
            SIGNALS.show_message.emit('Notes saved!')

    def _notes_dialog(self):
        """Open qt dialog box for edit shader notes."""
        title = 'Edit Shader Notes'
        lineEdit = QLineEdit.Normal
        text, result = QInputDialog.getText(None, title, '', lineEdit, 'default')
        return text if result else None

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

        cmd = ' '.join([MAYAPY, RND_SCRIPT, maya_file, self.shader.cg_file, self.shader.thumbnail])

        with self.wait_cursor():
            process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            output, error = process.communicate()
            log.info(output)
            log.info(error)

        self.button.setIcon(QIcon(self.shader.get_thumbnail()))  # reload thumbnail image

    @contextmanager
    def wait_cursor(self):
        """Context manager for wait cursor."""
        try:
            QApplication.setOverrideCursor(QCursor(QtCore.Qt.WaitCursor))
            yield
        finally:
            QApplication.restoreOverrideCursor()
