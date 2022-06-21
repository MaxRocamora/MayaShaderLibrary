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

from PySide2 import QtCore, QtGui, QtWidgets

from msl.libs.logger import log
from msl.libs.observer import Observer
from msl.libs.qt_dialogs import warning_message
from msl.ui.icons import get_icon
from msl.config import QSS_BUTTON, thumbnail_default_scene

RND_SCRIPT = os.path.join(os.path.dirname(__file__), 'utils', 'generate_thumbnail.py')
MAYAPY = os.path.join(os.getenv('MAYA_LOCATION'), 'bin', 'mayapy.exe')


class ShaderWidget(QtWidgets.QToolButton):

    def __init__(self, shader, *args, **kwargs):
        super().__init__(**kwargs)
        self.observer = Observer()
        self._shader = shader
        self.name = shader.name

        self.setText(self.name)
        self.setIcon(QtGui.QIcon(shader.get_thumbnail()))
        self.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)
        self.setFixedSize(110, 110)
        self.iconSize()
        self.setIconSize(QtCore.QSize(80, 80))
        with open(QSS_BUTTON) as fh:
            self.setStyleSheet(fh.read())

        self.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.context_menu)
        self.clicked.connect(self.selected)

    @property
    def shader(self):
        return self._shader

    def selected(self):
        ''' widget clicked callback '''
        self.observer.select_shader(self.shader)

    def context_menu(self, mousePosition):
        ''' widget right click context menu callback '''
        self.observer.select_shader(self.shader)

        self.menu = QtWidgets.QMenu()

        text = f"Import '{self.name}'' into scene"
        action_import = QtWidgets.QAction(get_icon("import"), text, self.menu)
        self.menu.addAction(action_import)
        action_import.triggered.connect(lambda: self.shader.import_shader())
        self.menu.addSeparator()

        text = f"Import '{self.name}'' and assign into selection"
        action_import_sel = QtWidgets.QAction(get_icon("import"), text, self.menu)
        self.menu.addAction(action_import_sel)
        action_import_sel.triggered.connect(lambda: self.shader.import_shader(assign=True))
        self.menu.addSeparator()

        text = f"Rename '{self.name}'"
        action_rename = QtWidgets.QAction(get_icon("rename"), text, self.menu)
        self.menu.addAction(action_rename)
        action_rename.triggered.connect(self.rename_shader)
        self.menu.addSeparator()

        text = f"Browse '{self.name}' folder on disk"
        action_browse = QtWidgets.QAction(get_icon("browse"), text, self.menu)
        self.menu.addAction(action_browse)
        action_browse.triggered.connect(self.shader.explore)
        self.menu.addSeparator()

        text = f"Generate {self.name} Thumbnail"
        action_thumbnail = QtWidgets.QAction(get_icon("thumbnail"), text, self.menu)
        self.menu.addAction(action_thumbnail)
        action_thumbnail.triggered.connect(self.launch_thumbnail)
        self.menu.addSeparator()

        text = f"Delete '{self.name}' from lib"
        action_delete = QtWidgets.QAction(get_icon("delete"), text, self.menu)
        self.menu.addAction(action_delete)
        action_delete.triggered.connect(self.delete_shader)
        self.menu.addSeparator()
        self.menu.popup(QtGui.QCursor.pos())

    def rename_shader(self):
        ''' open qt dialog box for rename shader '''

        new_name, result = QtWidgets.QInputDialog.getText(
            self.observer.ui,
            "Rename Shader",
            'Enter Shader New Name',
            QtWidgets.QLineEdit.Normal,
            "default"
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
        ''' open qt dialog box for rename shader '''
        msg = QtWidgets.QMessageBox(self.observer.ui)
        msg.setWindowTitle('Confirm Deletion')
        msg.setStandardButtons(QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.Cancel)
        msg.setStyleSheet("background: rgba(40, 40, 40, 255);")
        msg.setIcon(QtWidgets.QMessageBox.Warning)
        msg.setWindowIcon(get_icon('app'))
        msg.setText('Delete selected shader files?')
        choice = msg.exec_()
        if choice == QtWidgets.QMessageBox.Yes:
            self.shader.delete()
            self.shader.category.reload()

    def launch_thumbnail(self):
        ''' Launch python script for thumbnail generation
        Render Command sends the script, the lightRig scene
        used for rendering, the shader maya file,
        and the target png file for the thumbnail.
        '''
        maya_file = os.path.abspath(thumbnail_default_scene)
        if not os.path.exists(MAYAPY):
            log.error('mayapy.exe not found.', MAYAPY)
            return

        cmd = ' '.join([MAYAPY, RND_SCRIPT, maya_file,
                        self.shader.cg_file, self.shader.thumbnail]
                       )

        with self.wait_cursor():
            process = subprocess.Popen(
                cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            output, error = process.communicate()
            log.info(output)
            log.info(error)

        # reload thumbnail image
        self.setIcon(QtGui.QIcon(self.shader.get_thumbnail()))

    @contextmanager
    def wait_cursor(self):
        try:
            QtWidgets.QApplication.setOverrideCursor(
                QtGui.QCursor(QtCore.Qt.WaitCursor))
            yield
        finally:
            QtWidgets.QApplication.restoreOverrideCursor()
