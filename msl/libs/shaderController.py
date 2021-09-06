# -*- coding: utf-8 -*-
'''
ARCANE Shader Library Controller
Controller for selected shader related methods.
'''
from PySide2 import QtCore
from .dialogs.dlg_addShader import addShaderDialog
from ..ui.icons import getIcon


class ShaderController():
    def __init__(self, parent):
        self.ui = parent
        self.setConnections()

    def setConnections(self):
        ''' Definition for ui widgets qt signals & attributes '''
        self.ui.btn_addShader.clicked.connect(self.addShaderCall)
        self.ui.btn_addShader.setIcon(getIcon("plus"))
        self.ui.btn_addShader.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.ui.btn_addShader.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.ui.btn_addShader.setStyleSheet("background:transparent;")
        self.ui.btn_addShader.installEventFilter(self.ui)
        self.ui.btn_saveChanges.clicked.connect(self.saveNotes)
        self.ui.btn_saveChanges.setIcon(getIcon("save"))
        self.ui.btn_saveChanges.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.ui.btn_saveChanges.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.ui.btn_saveChanges.setStyleSheet("background:transparent;")
        self.ui.btn_saveChanges.installEventFilter(self.ui)

    def addShaderCall(self):
        ''' Calls for addShaderDialog '''
        addShaderDialog(self.ui.observer)

    def saveNotes(self):
        ''' Saving notes on selected shader '''
        shader = self.ui.observer.selectedShader
        if shader:
            shader.notes = str(self.ui.te_notes.document().toPlainText())
            shader.saveShaderProperties()
