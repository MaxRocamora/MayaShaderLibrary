# --------------------------------------------------------------------------------------------
# Maya Shader Library
# Author: maxirocamora@gmail.com
#
# Load Python Command:
# import shaderLibrary.shaderLibrary as sl; sl.load()
# --------------------------------------------------------------------------------------------
import os
import webbrowser

from PySide2 import QtCore
from PySide2 import QtUiTools
from PySide2.QtWidgets import QMainWindow

import maya.cmds as cmds

from msl.libs.observer import ObserverUI
from msl.libs.categoryController import CategoryController
from msl.libs.shaderController import ShaderController
from msl.libs.utils.get_maya_window import get_maya_main_window
from msl.libs.utils.userSettings import UserSettings
from msl.libs.utils.statusbar import Statusbar
from msl.libs.dialogs.dirty_dialog import dirty_file_dialog
from msl.ui.icons import get_icon
from msl.version import app_name, version, qtWinName
from msl import thumbnail_default_scene, QSS_FILE, APP_QICON

root_path = os.path.dirname(__file__)
ui_file = os.path.join(root_path, 'ui', 'ui', 'main.ui')
url = 'https://mayashaderlibrary.readthedocs.io'


class ProgramUI_shaderLibrary(QMainWindow):

    def __init__(self, parent=get_maya_main_window()):
        super(ProgramUI_shaderLibrary, self).__init__(parent)
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose, True)
        self.setObjectName(qtWinName)
        self.ui = QtUiTools.QUiLoader().load(ui_file)
        self.setCentralWidget(self.ui)
        self.move(parent.geometry().center() - self.ui.geometry().center())
        self.setWindowIcon(APP_QICON)
        self.setWindowTitle(app_name + ' ' + version)
        with open(QSS_FILE, "r") as fh:
            self.setStyleSheet(fh.read())

        self.userSettings = UserSettings("shaderLibrary")
        self.uiBar = Statusbar(self.ui.statusBar())
        self.observer = ObserverUI(self, self.ui)
        self.categoryCC = CategoryController(self, self.observer)
        self.shaderCC = ShaderController(self.ui, self.observer)
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
        self.ui.mnu_help_web.triggered.connect(self.open_web_help)

    def eventFilter(self, obj, event):
        '''Connect signals on mouse over'''
        if QtCore is None:
            return
        if event.type() == QtCore.QEvent.Enter:
            self.old_message = self.uiBar.statusbar.currentMessage()
            self.uiBar.inform(obj.statusTip())
        elif event.type() == QtCore.QEvent.Leave:
            self.uiBar.inform(self.old_message)
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
        total_tabs = self.ui.tab_materials.count()
        fCategorys = [self.ui.tab_materials.tabText(
            i) for i in range(total_tabs)]

        self.userPref = {"lastCategory": lastCategory,
                         'favoriteCategorys': fCategorys
                         }
        self.userSettings.saveUS(self.userPref)
        self.close()

    def loadUserPreferences(self):
        ''' Loads user preferences '''
        self.userPref = self.userSettings.loadUS()
        if not self.userPref:
            return False

        lastTab = self.userPref.get("lastCategory", 0)
        favTabs = self.userPref.get("favoriteCategorys", [])

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

    def open_web_help(self):
        ''' opens a browser to the help docs'''
        webbrowser.open(url)

# --------------------------------------------------------------------------------------------
# MAIN
# --------------------------------------------------------------------------------------------


def load():
    ''' maya load method '''
    if cmds.window(qtWinName, q=1, ex=1):
        cmds.deleteUI(qtWinName)
    app = ProgramUI_shaderLibrary()
    app.show()
