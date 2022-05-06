# --------------------------------------------------------------------------------------------
# Maya Shader Library
# Author: maxirocamora@gmail.com
#
# Shader Generator
# Fills layouts with buttons widgets of shaders from the corresponding category
# Holds callback classes for button actions and menus
# --------------------------------------------------------------------------------------------

import os
import subprocess
from contextlib import contextmanager

from PySide2 import QtCore, QtGui, QtWidgets

from msl import thumbnail_default_scene, QSS_BUTTON
from msl.ui.icons import get_icon
from msl.libs.dialogs.dlg_renameShader import renameShaderDialog
from msl.libs.dialogs.dlg_deleteShader import deleteShaderDialog

renderScript = os.path.join(
    os.path.dirname(__file__), 'utils', 'generateThumbnail.py')

MAYAPY = os.path.join(os.getenv('MAYA_LOCATION'), 'bin', 'mayapy.exe')


def generateShaderButtons(shaderList, observer, layout, wide):
    '''Generate a list of button widgets from each shader object
    Args:
        shaderList (list) List of shader objects
        observer (class) Observer class to set selected shader
    '''
    shaderButtons = []
    for shader in shaderList:
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
        b.customContextMenuRequested.connect(
            CallMenu(shader.name, shader, observer))
        b.clicked.connect(CallUser(shader, observer, b))
        shaderButtons.append(b)
    fillShaderLayout(layout, wide, shaderButtons)


def fillShaderLayout(layout, wide, buttonList):
    '''
    Fills given layout with buttons shaders
    Args:
        layout (widget) layout widget to fill
        wide (int) maximun columns to split buttons
        buttonList (list) list of button widgets
    '''
    b = 0
    row = 0
    while b < len(buttonList):
        for col in range(wide):
            if b >= len(buttonList):
                break
            layout.addWidget(buttonList[b], row, col)
            b += 1
        row += 1


class CallUser:
    ''' Menu for click on shader button '''

    def __init__(self, shaderClass, observer, button):
        self.shader = shaderClass
        self.observer = observer
        self.button = button

    def __call__(self):
        self.observer.selectedShader = self.shader


class CallMenu:
    ''' Menu for right click on shader button '''

    def __init__(self, name, shaderClass, observer):
        self.name = name
        self.shader = shaderClass
        self.observer = observer

    def __call__(self, mousePosition):
        self.observer.selectedShader = self.shader
        self.menu = QtWidgets.QMenu()

        actionStr = f"Import '{self.name}'' into scene"
        smImport = QtWidgets.QAction(get_icon("impMaya"), actionStr, self.menu)
        self.menu.addAction(smImport)
        smImport.triggered.connect(lambda: self.shader.importShader())
        self.menu.addSeparator()

        actionStr = f"Import '{self.name}'' and assign into selection"
        smImportSet = QtWidgets.QAction(
            get_icon("impMaya"), actionStr, self.menu)
        self.menu.addAction(smImportSet)
        smImportSet.triggered.connect(
            lambda: self.shader.importShader(assign=True))
        self.menu.addSeparator()

        actionStr = f"Rename '{self.name}'"
        smRename = QtWidgets.QAction(get_icon("rename"), actionStr, self.menu)
        self.menu.addAction(smRename)
        smRename.triggered.connect(
            renameShaderDialog(self.shader, self.observer))
        self.menu.addSeparator()

        actionStr = f"Browse '{self.name}' folder on disk"
        smBrowse = QtWidgets.QAction(get_icon("browse"), actionStr, self.menu)
        self.menu.addAction(smBrowse)
        smBrowse.triggered.connect(self.shader.browse)
        self.menu.addSeparator()

        actionStr = f"Generate {self.name} Thumbnail"
        smBrowse = QtWidgets.QAction(get_icon("wips"), actionStr, self.menu)
        self.menu.addAction(smBrowse)
        smBrowse.triggered.connect(lambda: self.launchThumbnail(self.shader))
        self.menu.addSeparator()

        actionStr = f"Delete '{self.name}' from lib"
        smDelete = QtWidgets.QAction(get_icon("delete"), actionStr, self.menu)
        self.menu.addAction(smDelete)
        smDelete.triggered.connect(
            deleteShaderDialog(self.shader, self.observer))
        self.menu.addSeparator()
        self.menu.popup(QtGui.QCursor.pos())

    def launchThumbnail(self, shader):
        ''' Launch python script for thumbnail generation
        Render Command sends the script, the lightrig scene
        used for rendering, the shader maya file,
        and the target png file for the thumbnail.
        '''
        # from StringIO import StringIO
        shaderRig = os.path.abspath(thumbnail_default_scene)
        if not os.path.exists(MAYAPY):
            print('mayapy.exe not found.', MAYAPY)
            return

        cmd = ' '.join([MAYAPY, renderScript, shaderRig,
                       shader.cgFile, shader.thumbnail]
                       )

        with self.waitCursor():
            process = subprocess.Popen(
                cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            output, error = process.communicate()
            # log_subprocess_output(StringIO(output))
            print(output)
            print(error)

    @contextmanager
    def waitCursor(self):
        try:
            QtWidgets.QApplication.setOverrideCursor(
                QtGui.QCursor(QtCore.Qt.WaitCursor))
            yield
        finally:
            QtWidgets.QApplication.restoreOverrideCursor()
