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

from msl.libs.dialogs.dlg_add_category import AddCategoryDialog
from msl.libs.observer import Observer
from msl.libs.shader_controller import ShaderController
from msl.libs.utils.get_maya_window import get_maya_main_window
from msl.libs.utils.userSettings import UserSettings
from msl.libs.utils.folder import browse
from msl.libs.qt_dialogs import dirty_file_dialog
from msl.libs.category_view import CategoryView
from msl.version import app_name, version
from msl.config import (LIBRARY_SHADERS_PATH, URL_DOC,
                        thumbnail_default_scene, QSS_FILE, APP_QICON, QT_WIN_NAME)

ui_file = os.path.join(os.path.dirname(__file__), 'ui', 'ui', 'main.ui')


class ShaderLibraryAPP(QMainWindow):

    def __init__(self, parent=get_maya_main_window()):
        super().__init__(parent)
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose, True)
        self.setObjectName(QT_WIN_NAME)
        self.ui = QtUiTools.QUiLoader().load(ui_file)
        self.setCentralWidget(self.ui)
        self.move(parent.geometry().center() - self.ui.geometry().center())
        self.setFixedSize(self.ui.maximumWidth(), self.ui.maximumHeight())
        self.setWindowIcon(APP_QICON)
        self.setWindowTitle(f'{app_name} {version}')
        with open(QSS_FILE) as fh:
            self.setStyleSheet(fh.read())

        self.user_settings = UserSettings("shaderLibrary")
        self.observer = Observer()
        self.observer.ui = self.ui
        self.observer.status_bar = self.ui.statusBar()
        self.view = CategoryView(self.ui.view_category)
        self.observer.view = self.view
        self.shader_ctrl = ShaderController(self.ui)
        self.view.load_categories()
        self._set_connections()
        self.load_user_preferences()
        self.show()
        self.activateWindow()
        self.observer.status_message(f'{app_name} {version} loaded.')

    def _set_connections(self):
        '''ui widgets signals & attributes '''
        self.ui.mnu_open_default_light_rig.triggered.connect(self.open_default_light_rig)
        self.ui.mnu_help_web.triggered.connect(lambda: webbrowser.open(URL_DOC))
        self.ui.mnu_reload_categories.triggered.connect(self.observer.view.load_categories)
        self.ui.mnu_add_new_category.triggered.connect(lambda: AddCategoryDialog())
        self.ui.mnu_browse_category_folder.triggered.connect(
            lambda: browse(LIBRARY_SHADERS_PATH))

    # ------------------------------------------------------------------------------------
    # USER PREFERENCES
    # ------------------------------------------------------------------------------------

    def closeEvent(self, event):
        ''' Save user settings into a json file on close '''
        if QtCore is None:
            self.close()
            return

        # get categories pinned and save them into user preferences
        fav_categories = [cat.name() for cat in self.observer.categories() if cat.pinned()]
        self.user_pref = {'pinned': fav_categories}
        self.user_settings.save(self.user_pref)
        self.close()

    def load_user_preferences(self):
        ''' Loads user preferences '''
        self.user_pref = self.user_settings.load()
        if not self.user_pref:
            return

        # restore last pinned categories
        fav_tabs = self.user_pref.get("pinned", [])
        for category in self.observer.categories():
            if category.name() in fav_tabs:
                category.pin()

    # ------------------------------------------------------------------------------------
    # MENU OPTIONS
    # ------------------------------------------------------------------------------------

    def open_default_light_rig(self,):
        ''' Open default maya file used for render thumbnails '''
        self.status_bar.info(thumbnail_default_scene)
        if os.path.exists(thumbnail_default_scene):
            dirty_file_dialog()
            cmds.file(thumbnail_default_scene, force=True, open=True)
