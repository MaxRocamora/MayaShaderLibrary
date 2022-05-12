# ----------------------------------------------------------------------------------------
# Maya Shader Library
# Author: maxirocamora@gmail.com
# https://github.com/MaxRocamora/MayaShaderLibrary
#
# ----------------------------------------------------------------------------------------
import os
import webbrowser

from PySide2 import QtCore
from PySide2 import QtUiTools
from PySide2.QtWidgets import QMainWindow

import maya.cmds as cmds

from msl.libs.observer import Observer
from msl.libs.category_controller import CategoryController
from msl.libs.shader_controller import ShaderController
from msl.libs.utils.get_maya_window import get_maya_main_window
from msl.libs.utils.userSettings import UserSettings
from msl.libs.utils.statusbar import Statusbar
from msl.libs.qt_dialogs import dirty_file_dialog
from msl.ui.icons import get_icon
from msl.version import app_name, version
from msl.config import thumbnail_default_scene, QSS_FILE, APP_QICON, QT_WIN_NAME

ui_file = os.path.join(os.path.dirname(__file__), 'ui', 'ui', 'main.ui')
url = 'https://mayashaderlibrary.readthedocs.io'


class ShaderLibraryAPP(QMainWindow):

    def __init__(self, parent=get_maya_main_window()):
        super().__init__(parent)
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose, True)
        self.setObjectName(QT_WIN_NAME)
        self.ui = QtUiTools.QUiLoader().load(ui_file)
        self.setCentralWidget(self.ui)
        self.move(parent.geometry().center() - self.ui.geometry().center())
        self.setWindowIcon(APP_QICON)
        self.setWindowTitle(f'{app_name} {version}')
        with open(QSS_FILE) as fh:
            self.setStyleSheet(fh.read())

        self.user_settings = UserSettings("shaderLibrary")
        self.status_bar = Statusbar(self.ui.statusBar())
        self.observer = Observer()
        self.observer.ui = self.ui
        self.category_ctrl = CategoryController(self)
        self.observer.category_ctrl = self.category_ctrl
        self.shader_ctrl = ShaderController(self.ui)
        self.set_connections()
        self.load_user_preferences()
        self.show()
        self.activateWindow()

    # ------------------------------------------------------------------------------------
    # Qt UI Signals and event Handler
    # ------------------------------------------------------------------------------------

    def set_connections(self):
        '''ui widgets signals & attributes '''
        self.ui.btn_refresh_cat.clicked.connect(self.category_ctrl.refresh_category_tab)
        self.ui.btn_refresh_cat.setIcon(get_icon("refresh"))
        self.ui.btn_refresh_cat.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.ui.btn_refresh_cat.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.ui.btn_refresh_cat.setStyleSheet("background:transparent;")
        self.ui.btn_refresh_cat.installEventFilter(self)
        self.ui.mnu_open_default_light_rig.triggered.connect(self.open_default_light_rig)
        self.ui.mnu_help_web.triggered.connect(self.open_web_help)

    def eventFilter(self, obj, event):
        '''Connect signals on mouse over'''
        if QtCore is None:
            return
        if event.type() == QtCore.QEvent.Enter:
            self.old_message = self.status_bar.statusbar.currentMessage()
            self.status_bar.inform(obj.statusTip())
        elif event.type() == QtCore.QEvent.Leave:
            self.status_bar.inform(self.old_message)
        event.accept()
        return False

    # ------------------------------------------------------------------------------------
    # USER PREFERENCES
    # ------------------------------------------------------------------------------------

    def closeEvent(self, event):
        ''' Save user settings into a json file on close '''
        if QtCore is None:
            self.close()
            return

        last_category = self.category_ctrl.current_category_tab()
        total_tabs = self.ui.tab_materials.count()
        fav_categories = [self.ui.tab_materials.tabText(i) for i in range(total_tabs)]

        self.userPref = {"lastCategory": last_category,
                         'favoriteCategories': fav_categories
                         }
        self.user_settings.saveUS(self.userPref)
        self.close()

    def load_user_preferences(self):
        ''' Loads user preferences '''
        self.userPref = self.user_settings.loadUS()
        if not self.userPref:
            return False

        last_tab = self.userPref.get("lastCategory", 0)
        fav_tabs = self.userPref.get("favoriteCategories", [])

        self.category_ctrl.load_categories()
        for category in self.observer.categories():
            if category.name in fav_tabs:
                self.category.pin()
        self.category_ctrl.focus_tab(last_tab)

    # ------------------------------------------------------------------------------------
    # MENU OPTIONS
    # ------------------------------------------------------------------------------------

    def open_default_light_rig(self,):
        ''' Open default maya file used for render thumbnails '''
        self.status_bar.inform(thumbnail_default_scene)
        if os.path.exists(thumbnail_default_scene):
            dirty_file_dialog()
            cmds.file(thumbnail_default_scene, force=True, open=True)

    def open_web_help(self):
        ''' opens a browser to the help docs'''
        webbrowser.open(url)
