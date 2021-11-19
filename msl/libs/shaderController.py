# --------------------------------------------------------------------------------------------
# Maya Shader Library
# Author: maxirocamora@gmail.com
#
# Shader Library Controller
# Controller for selected shader related methods.
# --------------------------------------------------------------------------------------------
from PySide2 import QtCore

from msl.libs.dialogs.dlg_addShader import addShaderDialog
from msl.ui.icons import get_icon


class ShaderController():
    def __init__(self, ui, observer):
        self.ui = ui
        self.observer = observer
        self.set_connections()

    def set_connections(self):
        ''' Definition for ui widgets qt signals & attributes '''
        self.ui.btn_addShader.clicked.connect(self.addShaderCall)
        self.ui.btn_addShader.setIcon(get_icon("plus"))
        self.ui.btn_addShader.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.ui.btn_addShader.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.ui.btn_addShader.setStyleSheet("background:transparent;")
        self.ui.btn_addShader.installEventFilter(self.ui)
        self.ui.btn_saveChanges.clicked.connect(self.saveNotes)
        self.ui.btn_saveChanges.setIcon(get_icon("save"))
        self.ui.btn_saveChanges.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.ui.btn_saveChanges.setAttribute(
            QtCore.Qt.WA_TranslucentBackground)
        self.ui.btn_saveChanges.setStyleSheet("background:transparent;")
        self.ui.btn_saveChanges.installEventFilter(self.ui)

    def addShaderCall(self):
        ''' Calls for addShaderDialog '''
        addShaderDialog(self.observer)

    def saveNotes(self):
        ''' Saving notes on selected shader '''
        shader = self.observer.selectedShader
        if shader:
            shader.notes = str(self.ui.te_notes.document().toPlainText())
            shader.saveShaderProperties()
