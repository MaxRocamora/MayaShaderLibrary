# -*- coding: utf-8 -*-
''' Maya Shader Library
Author: maxirocamora@gmail.com

# Load Python Command:
import shaderLibrary.shaderLibrary as sl; sl.load()

'''
# --------------------------------------------------------------------------------------------
import os

from PySide2 import QtCore
from PySide2 import QtUiTools
from PySide2.QtWidgets import QMainWindow

import maya.cmds as cmds

from msl.libs.observer import ObserverUI
from msl.libs import categoryController as categoryCC
from msl.libs import shaderController as shaderCC
from msl.libs.qt.loadMayaUi import get_maya_main_window
from msl.libs.qt.qtStyle import cssMainWindow
from msl.libs.utils.userSettings import UserSettings
from msl.libs.utils.uiStatus import Statusbar
from msl.libs.dialogs.dirty_dialog import dirty_file_dialog
from msl.ui.icons import get_icon
from msl.version import app_name, version, qtWinName
from msl import thumbnail_default_scene

root_path = os.path.dirname(__file__)
ui_file = os.path.join(root_path, 'ui', 'ui', 'main.ui')

msgStr = {
    'unsavedScene': 'YOU HAVE UNSAVED CHANGES ON YOUR CURRENT SCENE.'
}

# --------------------------------------------------------------------------------------------
# Class: Main UI
# --------------------------------------------------------------------------------------------


class ProgramUI_shaderLibrary(QMainWindow):

    def __init__(self, parent=get_maya_main_window()):
        super(ProgramUI_shaderLibrary, self).__init__(parent)
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose, True)
        self.ui = QtUiTools.QUiLoader().load(ui_file)
        self.setCentralWidget(self.ui)
        self.move(parent.geometry().center() - self.ui.geometry().center())

        cssMainWindow(root_path, self, qtWinName, app_name + ' ' + version)
        self.userSettings = UserSettings("shaderLibrary")
        self.uiBar = Statusbar(self.statusBar)
        self.observer = ObserverUI(self)
        self.categoryCC = categoryCC.CategoryController(self)
        self.shaderCC = shaderCC.ShaderController(self)
        self.setConnections()
        self.loadUserPreferences()
        self.show()
        self.activateWindow()

# --------------------------------------------------------------------------------------------
# Qt UI Signals and event Handler
# --------------------------------------------------------------------------------------------

    def setConnections(self):
        ''' Definition for ui widgets qt signals & attributes '''
        self.ui.btn_refresh.clicked.connect(self.categoryCC.refreshCategoryTab)
        self.ui.btn_refresh.setIcon(get_icon("refresh"))
        self.ui.btn_refresh.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.ui.btn_refresh.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.ui.btn_refresh.setStyleSheet("background:transparent;")
        self.ui.btn_refresh.installEventFilter(self)
        self.ui.mnu_defaultLightRigOpen.triggered.connect(
            self.openDefaultLightRig)
        self.ui.mnu_setFolder.triggered.connect(self.setShaderFolder)

    def eventFilter(self, obj, event):
        '''Connect signals on mouse over'''
        if QtCore is None:
            return
        if event.type() == QtCore.QEvent.Enter:
            self.oldMessage = self.statusBar.currentMessage()
            self.statusBar.showMessage(obj.statusTip(), 0)
        elif event.type() == QtCore.QEvent.Leave:
            self.statusBar.showMessage(self.oldMessage, 0)
        event.accept()
        return False

# --------------------------------------------------------------------------------------------
# USER PREFERENCES
# --------------------------------------------------------------------------------------------

    def closeEvent(self, event):
        ''' Save user settings into a json file on close '''
        if QtCore is None:
            self.close()
            return

        lastCategory = self.categoryCC.currentCategoryTab()
        total_tabs = self.tab_materials.count()
        fCategorys = [self.tab_materials.tabText(i) for i in range(total_tabs)]

        self.userPref = {"lastCategory": lastCategory,
                         'favouriteCategorys': fCategorys
                         }
        self.userSettings.saveUS(self.userPref)
        self.close()

    def loadUserPreferences(self):
        ''' Loads user preferences '''
        self.userPref = self.userSettings.loadUS()
        if not self.userPref:
            return False

        lastTab = self.userPref.get("lastCategory", 0)
        favTabs = self.userPref.get("favouriteCategorys", [])

        self.categoryCC.loadCategorys()
        for category in self.observer.categoryList:
            if category.name in favTabs:
                self.categoryCC.pinTab(category)
        self.categoryCC.focusTabName(lastTab)

# --------------------------------------------------------------------------------------------
# MENU OPTIONS
# --------------------------------------------------------------------------------------------

    def openDefaultLightRig(self,):
        ''' Open default maya file used for render thumbnails '''
        self.uiBar.inform(thumbnail_default_scene)
        if os.path.exists(thumbnail_default_scene):
            dirty_file_dialog()
            cmds.file(thumbnail_default_scene, force=True, open=True)

    def setShaderFolder(self):
        ''' ask user for shader storage folder '''
        pass

# --------------------------------------------------------------------------------------------
# MAIN
# --------------------------------------------------------------------------------------------


def load():
    ''' maya load method '''
    if cmds.window(qtWinName, q=1, ex=1):
        cmds.deleteUI(qtWinName)
    app = ProgramUI_shaderLibrary()
    app.show()
