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
from PySide2.QtWidgets import QMainWindow, QWidget, QGridLayout, QScrollArea

import maya.cmds as cmds

from msl.libs.add_category import AddCategoryDialog
from msl.libs.categories import CategoryList
from msl.libs.observer import Observer
from msl.libs.qt_dialogs import dirty_file_dialog
from msl.libs.signals import SIGNALS
from msl.libs.shader_controller import ShaderController
from msl.libs.utils.get_maya_window import get_maya_main_window
from msl.libs.utils.folder import browse
from msl.config import APP_QICON, QT_WIN_NAME
from msl.config import LIBRARY_PATH, thumbnail_default_scene, QSS_FILE, URL_DOC
from msl.version import app_name, version

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
        self._build_ui()
        self._restore_session()
        self.show()
        self.activateWindow()
        self.status_message(f'{app_name} {version} loaded.')

    def _set_connections(self):
        """Ui widgets signals & attributes."""
        self.ui.mnu_open_default_light_rig.triggered.connect(self.open_default_light_rig)
        self.ui.mnu_help_web.triggered.connect(lambda: webbrowser.open(URL_DOC))
        self.ui.mnu_add_new_category.triggered.connect(lambda: AddCategoryDialog())
        self.ui.mnu_browse_category_folder.triggered.connect(lambda: browse(LIBRARY_PATH))
        SIGNALS.show_message.connect(self.status_message)

    def _build_ui(self):
        """Builds the UI."""

        # create shaders scroll area and grid layout
        self.ui.scroll_area = QScrollArea()
        self.ui.scroll_area.setWidgetResizable(True)
        self.ui.scroll_area.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.ui.scroll_area.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)

        # create scroll widget and layout
        self.ui.scroll_widget = QWidget()
        self.ui.scroll_layout = QGridLayout(self.ui.scroll_widget)
        self.ui.scroll_layout.setSpacing(5)
        self.ui.scroll_layout.setHorizontalSpacing(5)
        self.ui.scroll_layout.setVerticalSpacing(5)
        self.ui.scroll_layout.setContentsMargins(2, 2, 2, 2)
        self.ui.scroll_layout.setAlignment(QtCore.Qt.AlignTop)

        # add scroll area to main layout
        self.ui.scroll_area.setWidget(self.ui.scroll_widget)
        self.ui.vbox.addWidget(self.ui.scroll_area)

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

    def status_message(self, message: str):
        """Writes a message into the statusbar."""
        self.ui.statusBar().showMessage(message)

    def closeEvent(self, event: QtCore.QEvent):
        """Save user settings and close."""

        last_selected = self.view.current_category()
        if last_selected:
            self.settings.setValue('last_selected', last_selected.name())

        super().closeEvent(event)
