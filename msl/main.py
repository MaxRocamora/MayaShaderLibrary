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

from msl.libs.add_category import AddCategoryDialog
from msl.libs.observer import Observer
from msl.libs.shader_controller import ShaderController
from msl.libs.utils.get_maya_window import get_maya_main_window
from msl.libs.utils.folder import browse
from msl.libs.qt_dialogs import dirty_file_dialog
from msl.libs.categories import CategoryList
from msl.version import app_name, version
from msl.config import (
    LIBRARY_PATH,
    URL_DOC,
    thumbnail_default_scene,
    QSS_FILE,
    APP_QICON,
    QT_WIN_NAME,
)

ui_file = os.path.join(os.path.dirname(__file__), 'ui', 'ui', 'main.ui')


class ShaderLibraryAPP(QMainWindow):
    def __init__(self, parent=get_maya_main_window()):
        """Main window for the shader library app."""
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

        self.settings = QtCore.QSettings('MayaTools', 'MayaShaderLibrary')
        self.observer = Observer()
        self.observer.ui = self.ui
        self.shader_ctrl = ShaderController(self.ui)
        self.view = CategoryList(self.ui.categories)
        self._set_connections()
        self._restore_session()
        self.show()
        self.activateWindow()
        self.observer.status_message(f'{app_name} {version} loaded.')

    def _set_connections(self):
        """Ui widgets signals & attributes."""
        self.ui.mnu_open_default_light_rig.triggered.connect(self.open_default_light_rig)
        self.ui.mnu_help_web.triggered.connect(lambda: webbrowser.open(URL_DOC))
        self.ui.mnu_add_new_category.triggered.connect(lambda: AddCategoryDialog())
        self.ui.mnu_browse_category_folder.triggered.connect(lambda: browse(LIBRARY_PATH))

    def _restore_session(self):
        """Load user preferences from the last session."""
        last = self.settings.value('last_selected', None)
        self.view.update(last)

    def open_default_light_rig(self):
        """Opens the maya file used for render thumbnails."""
        self.status_bar.info(thumbnail_default_scene)
        if os.path.exists(thumbnail_default_scene):
            dirty_file_dialog()
            cmds.file(thumbnail_default_scene, force=True, open=True)

    def closeEvent(self, event):
        """Save user settings into a json file on close."""
        if QtCore is None:
            self.close()
            return

        last_selected = self.view.current_category()
        if last_selected:
            self.settings.setValue('last_selected', last_selected.name())

        self.close()
