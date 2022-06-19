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

from msl.libs.dialogs.dlg_rename_shader import RenameShaderDialog
from msl.libs.dialogs.dlg_delete_shader import DeleteShaderDialog
from msl.libs.logger import log
from msl.libs.observer import Observer
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
        smImport = QtWidgets.QAction(get_icon("impMaya"), text, self.menu)
        self.menu.addAction(smImport)
        smImport.triggered.connect(lambda: self.shader.import_shader())
        self.menu.addSeparator()

        text = f"Import '{self.name}'' and assign into selection"
        smImportSet = QtWidgets.QAction(
            get_icon("impMaya"), text, self.menu)
        self.menu.addAction(smImportSet)
        smImportSet.triggered.connect(lambda: self.shader.import_shader(assign=True))
        self.menu.addSeparator()

        text = f"Rename '{self.name}'"
        smRename = QtWidgets.QAction(get_icon("rename"), text, self.menu)
        self.menu.addAction(smRename)
        smRename.triggered.connect(RenameShaderDialog(self.shader, self.observer))
        self.menu.addSeparator()

        text = f"Browse '{self.name}' folder on disk"
        smBrowse = QtWidgets.QAction(get_icon("browse"), text, self.menu)
        self.menu.addAction(smBrowse)
        smBrowse.triggered.connect(self.shader.explore)
        self.menu.addSeparator()

        text = f"Generate {self.name} Thumbnail"
        smBrowse = QtWidgets.QAction(get_icon("wips"), text, self.menu)
        self.menu.addAction(smBrowse)
        smBrowse.triggered.connect(self.launch_thumbnail)
        self.menu.addSeparator()

        text = f"Delete '{self.name}' from lib"
        smDelete = QtWidgets.QAction(get_icon("delete"), text, self.menu)
        self.menu.addAction(smDelete)
        smDelete.triggered.connect(DeleteShaderDialog(self.shader))
        self.menu.addSeparator()
        self.menu.popup(QtGui.QCursor.pos())

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
