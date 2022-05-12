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

from msl.config import thumbnail_default_scene, QSS_BUTTON
from msl.libs.dialogs.dlg_rename_shader import RenameShaderDialog
from msl.libs.dialogs.dlg_delete_shader import DeleteShaderDialog
from msl.libs.logger import log
from msl.ui.icons import get_icon

RND_SCRIPT = os.path.join(os.path.dirname(__file__), 'utils', 'generate_thumbnail.py')

MAYAPY = os.path.join(os.getenv('MAYA_LOCATION'), 'bin', 'mayapy.exe')


def generate_shader_buttons(shaders, observer, layout, wide):
    '''Generate a list of button widgets from each shader object
    Args:
        shaders (list) List of shader objects
        observer (class) Observer class to set selected shader
    '''
    shader_buttons = []
    for shader in shaders:
        b = QtWidgets.QToolButton()
        b.setText(shader.name)
        b.setIcon(QtGui.QIcon(shader.get_thumbnail()))
        b.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)
        b.setFixedSize(110, 110)
        b.iconSize()
        b.setIconSize(QtCore.QSize(80, 80))
        with open(QSS_BUTTON) as fh:
            b.setStyleSheet(fh.read())
        b.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        b.customContextMenuRequested.connect(CallMenu(shader.name, shader, observer))
        b.clicked.connect(CallUser(shader, observer, b))
        shader_buttons.append(b)
    fill_shader_layout(layout, wide, shader_buttons)


def fill_shader_layout(layout, wide, buttons):
    ''' Fills given layout with buttons shaders
    Args:
        layout (widget) layout widget to fill
        wide (int) maximun columns to split buttons
        buttons (list) list of button widgets
    '''
    b = 0
    row = 0
    while b < len(buttons):
        for col in range(wide):
            if b >= len(buttons):
                break
            layout.addWidget(buttons[b], row, col)
            b += 1
        row += 1


class CallUser:
    ''' Menu for click on shader button '''

    def __init__(self, _shader, observer, button):
        self.shader = _shader
        self.observer = observer
        self.button = button

    def __call__(self):
        self.observer.select_shader(self.shader)


class CallMenu:
    ''' Menu for right click on shader button '''

    def __init__(self, name, _shader, observer):
        self.name = name
        self.shader = _shader
        self.observer = observer

    def __call__(self, mousePosition):
        self.observer.select_shader(self.shader)
        self.menu = QtWidgets.QMenu()

        text = f"Import '{self.name}'' into scene"
        smImport = QtWidgets.QAction(get_icon("impMaya"), text, self.menu)
        self.menu.addAction(smImport)
        smImport.triggered.connect(lambda: self.shader.importShader())
        self.menu.addSeparator()

        text = f"Import '{self.name}'' and assign into selection"
        smImportSet = QtWidgets.QAction(
            get_icon("impMaya"), text, self.menu)
        self.menu.addAction(smImportSet)
        smImportSet.triggered.connect(
            lambda: self.shader.importShader(assign=True))
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
        smBrowse.triggered.connect(lambda: self.launch_thumbnail(self.shader))
        self.menu.addSeparator()

        text = f"Delete '{self.name}' from lib"
        smDelete = QtWidgets.QAction(get_icon("delete"), text, self.menu)
        self.menu.addAction(smDelete)
        smDelete.triggered.connect(DeleteShaderDialog(self.shader))
        self.menu.addSeparator()
        self.menu.popup(QtGui.QCursor.pos())

    def launch_thumbnail(self, shader):
        ''' Launch python script for thumbnail generation
        Render Command sends the script, the lightrig scene
        used for rendering, the shader maya file,
        and the target png file for the thumbnail.
        '''
        maya_file = os.path.abspath(thumbnail_default_scene)
        if not os.path.exists(MAYAPY):
            log.error('mayapy.exe not found.', MAYAPY)
            return

        cmd = ' '.join([MAYAPY, RND_SCRIPT, maya_file,
                       shader.cg_file, shader.thumbnail]
                       )

        with self.waitCursor():
            process = subprocess.Popen(
                cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            output, error = process.communicate()
            log.info(output)
            log.info(error)

    @contextmanager
    def waitCursor(self):
        try:
            QtWidgets.QApplication.setOverrideCursor(
                QtGui.QCursor(QtCore.Qt.WaitCursor))
            yield
        finally:
            QtWidgets.QApplication.restoreOverrideCursor()
