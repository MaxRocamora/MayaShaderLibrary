# -*- coding: utf-8 -*-
'''
ARCANE Shader Library
Main interface class
Load Python Command:
# import shaderLibrary.shaderLibrary as sl; sl.load()

maxirocamora@gmail.com
www.arcanetools.com

to do:

    logg render output from subprocess to file

    instead of use a mayafile, make a json file for shaders, so we can rename or repath files, and import in
    other apps.

    update shader:
    when export a shader into category, if exist, make update options instead of overwrite

    get maps list connections
    copy to local maps / deploy maps

    import into selected: ask for replace shader

    ask to save current scene if dirty on dialog on open lightrig

    * generate library from selection!
        takes all shaders from selection and creates a new category
    * import all category

'''
# --------------------------------------------------------------------------------------------

# IMPORTS
import os
from version import *
from PySide2 import QtCore
import maya.cmds as cmds
from . import thumbnail_default_scene
from .libs.observer import ObserverUI
from .libs import categoryController as categoryCC
from .libs import shaderController as shaderCC
from .libs.qt.loadMayaUi import loadUi, getMayaWindow
from .libs.qt.qtStyle import cssMainWindow
from .ui.icons import getIcon
from .ui.userSettings import UserSettings

import mxr.ui.uiHelpers.uiStatus as uiStatus


appPath = os.path.dirname(__file__)
ui_main = os.path.join(appPath, 'ui', 'main_ui.ui')
form, base = loadUi(ui_main)

# --------------------------------------------------------------------------------------------
# Class: Main UI
# --------------------------------------------------------------------------------------------


class ProgramUI_shaderLibrary(base, form):

    msgStr = {
        'unsaveScene': 'YOU HAVE UNSAVED CHANGES ON YOUR CURRENT SCENE.'
    }

    def __init__(self, parent=getMayaWindow()):
        super(ProgramUI_shaderLibrary, self).__init__(parent)
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose, True)
        self.setupUi(self)
        cssMainWindow(appPath, self, qtWinName, __app__ + ' ' + __version__)
        self.userSettings = UserSettings("shaderLibrary")
        self.uiBar = uiStatus.uiStatusbar(self.statusBar)
        self.observer = ObserverUI(self)
        self.categoryCC = categoryCC.CategoryController(self)
        self.shaderCC = shaderCC.ShaderController(self)
        self.categoryCC.loadCategorys()
        self.setConnections()
        self.loadUserPreferences()

# --------------------------------------------------------------------------------------------
# Qt UI Signals and event Handler
# --------------------------------------------------------------------------------------------

    def setConnections(self):
        ''' Definition for ui widgets qt signals & attributes '''
        self.btn_refresh.clicked.connect(self.categoryCC.refreshCategoryTab)
        self.btn_refresh.setIcon(getIcon("refresh"))
        self.btn_refresh.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.btn_refresh.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.btn_refresh.setStyleSheet("background:transparent;")
        self.btn_refresh.installEventFilter(self)
        self.mnu_defaultLigthRigOpen.triggered.connect(self.openDefaultLightRig)

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
        ''' Save user settings on close '''
        if QtCore is None:
            self.close()
            return

        lastCategory = self.categoryCC.currentCategoryTab()
        favouriteCategorys = [
            self.tab_materials.tabText(i) for i in xrange(self.tab_materials.count())
        ]

        self.userPref = {"lastCategory": lastCategory,
                         'favouriteCategorys': favouriteCategorys
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
        for category in self.observer.categoryList:
            if category.name in favTabs:
                self.categoryCC.pinTab(category)
        self.categoryCC.focusTabName(lastTab)

# --------------------------------------------------------------------------------------------
# MENU OPTIONS
# --------------------------------------------------------------------------------------------

    def openDefaultLightRig(self,):
        ''' Open default maya file used for render thumbnails '''
        if os.path.exists(thumbnail_default_scene):
            cmds.file(thumbnail_default_scene, force=True, open=True)

# --------------------------------------------------------------------------------------------
# MAIN
# --------------------------------------------------------------------------------------------


def load():
    ''' maya load method '''
    if cmds.window(qtWinName, q=1, ex=1):
        cmds.deleteUI(qtWinName)
    app = ProgramUI_shaderLibrary()
    app.show()
