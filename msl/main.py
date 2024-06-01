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
from PySide2.QtWidgets import QMainWindow, QWidget, QGridLayout, QScrollArea, QToolButton

import maya.cmds as cmds

from msl.libs.add_category import AddCategoryDialog
from msl.libs.categories import CategoryList
from msl.libs.qt_dialogs import dirty_file_dialog
from msl.libs.signals import SIGNALS
from msl.libs.utils.get_maya_window import get_maya_main_window
from msl.libs.utils.folder import browse
from msl.config import APP_QICON, QT_WIN_NAME, UI
from msl.config import LIBRARY_PATH, thumbnail_default_scene, QSS_FILE, URL_DOC
from msl.resources.icons import get_icon
from msl.version import app_name, version


class ShaderLibraryAPP(QMainWindow):
    def __init__(self, parent=get_maya_main_window()):
        """Main window for the shader library app."""
        super().__init__(parent)
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose, True)
        self.setObjectName(QT_WIN_NAME)
        self.ui = QtUiTools.QUiLoader().load(UI)
        self.maya_window = parent
        self.setCentralWidget(self.ui)
        self.move(self.maya_window.geometry().center() - self.ui.geometry().center())
        self.setWindowIcon(APP_QICON)
        self.setWindowTitle(f'{app_name} {version}')
        self.settings = QtCore.QSettings('MayaTools', 'MayaShaderLibrary')
        with open(QSS_FILE) as fh:
            self.setStyleSheet(fh.read())

        self.setup_ui()
        self.categories_widget = CategoryList(self.ui.categories, self.ui)
        self._build_shader_ui()
        self._restore_session()
        self.show()
        self.activateWindow()
        self.status_message(f'{app_name} {version} loaded.')

    def setup_ui(self):
        """Ui widgets signals & attributes."""
        self.resize_timer = QtCore.QTimer(self)
        self.resize_timer.setSingleShot(True)
        self.resize_timer.timeout.connect(self.resize_finished)

        SIGNALS.show_message.connect(self.status_message)
        SIGNALS.display_shader_notes.connect(self.status_message)

        # create category button
        self.ui.btn_create = QToolButton()
        self.ui.toolbar.addWidget(self.ui.btn_create)
        self.ui.btn_create.clicked.connect(lambda: AddCategoryDialog())
        self.ui.btn_create.setToolTip('Create a new category.')
        self.ui.btn_create.setIcon(get_icon('new'))
        self.ui.btn_create.setPopupMode(QToolButton.InstantPopup)
        self.ui.btn_create.setArrowType(QtCore.Qt.NoArrow)

        # browse category folder button
        self.ui.btn_browse = QToolButton()
        self.ui.btn_browse.setText('Browse Folder')
        self.ui.toolbar.addWidget(self.ui.btn_browse)
        self.ui.btn_browse.clicked.connect(lambda: browse(LIBRARY_PATH))
        self.ui.btn_browse.setToolTip('Browse categories folder.')
        self.ui.btn_browse.setIcon(get_icon('browse'))
        self.ui.btn_browse.setPopupMode(QToolButton.InstantPopup)
        self.ui.btn_browse.setArrowType(QtCore.Qt.NoArrow)

        self.ui.toolbar.addSeparator()

        # open default light rig button
        self.ui.btn_open_thumb_file = QToolButton()
        self.ui.toolbar.addWidget(self.ui.btn_open_thumb_file)
        self.ui.btn_open_thumb_file.clicked.connect(self.open_default_light_rig)
        self.ui.btn_open_thumb_file.setToolTip('Open Thumbnail Render scene.')
        self.ui.btn_open_thumb_file.setIcon(get_icon('light'))
        self.ui.btn_open_thumb_file.setPopupMode(QToolButton.InstantPopup)
        self.ui.btn_open_thumb_file.setArrowType(QtCore.Qt.NoArrow)

        self.ui.toolbar.addSeparator()

        self.ui.btn_add_shader = QToolButton()
        self.ui.toolbar.addWidget(self.ui.btn_add_shader)
        self.ui.btn_add_shader.setToolTip('Add Selected Shader to category.')
        self.ui.btn_add_shader.setIcon(get_icon('add'))
        self.ui.btn_add_shader.setPopupMode(QToolButton.InstantPopup)
        self.ui.btn_add_shader.setArrowType(QtCore.Qt.NoArrow)

        self.ui.toolbar.addSeparator()

        # change modality button
        self.ui.btn_modal = QToolButton()
        self.ui.toolbar.addWidget(self.ui.btn_modal)
        self.ui.btn_modal.setToolTip('Toggle List/Icon View')
        self.ui.btn_modal.setIcon(get_icon('view_mode'))
        self.ui.btn_modal.setPopupMode(QToolButton.InstantPopup)
        self.ui.btn_modal.setArrowType(QtCore.Qt.NoArrow)
        self.ui.toolbar.addSeparator()

        # help button
        self.ui.btn_help = QToolButton()
        self.ui.toolbar.addWidget(self.ui.btn_help)
        self.ui.btn_help.setToolTip('Open Documentation')
        self.ui.btn_help.setIcon(get_icon('help'))
        self.ui.btn_help.setPopupMode(QToolButton.InstantPopup)
        self.ui.btn_help.setArrowType(QtCore.Qt.NoArrow)
        self.ui.btn_help.clicked.connect(lambda: webbrowser.open(URL_DOC))

        # connections
        self.ui.toolbar.topLevelChanged.connect(self.toolbar_moved)

    def _build_shader_ui(self):
        """Builds the UI."""

        # create shaders scroll area and grid layout
        self.ui.scroll_area = QScrollArea()
        self.ui.scroll_area.setWidgetResizable(True)
        self.ui.scroll_area.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.ui.scroll_area.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)

        # create scroll widget and layout
        self.ui.scroll_widget = QWidget()
        self.ui.scroll_layout = QGridLayout(self.ui.scroll_widget)
        self.ui.scroll_layout.setHorizontalSpacing(2)
        self.ui.scroll_layout.setVerticalSpacing(2)
        self.ui.scroll_layout.setContentsMargins(0, 0, 0, 0)
        self.ui.scroll_layout.setAlignment(QtCore.Qt.AlignTop)

        # add scroll area to main layout
        self.ui.scroll_area.setWidget(self.ui.scroll_widget)
        self.ui.vbox.addWidget(self.ui.scroll_area)

        self.ui.btn_modal.clicked.connect(self.change_category_view_mode)

    def change_category_view_mode(self):
        """Changes the modality of the shader widget buttons."""
        category = self.categories_widget.current_category()
        category.switch_widget_view()

    def _restore_session(self):
        """Load user preferences from the last session."""
        last = self.settings.value('last_selected', None)
        self.categories_widget.update(last)

        orientation = self.settings.value('toolbar_orientation', 1)
        if orientation:
            self.ui.toolbar.setOrientation(QtCore.Qt.Orientation(orientation))

        area = self.settings.value('toolbar_area', 4)
        if area:
            self.ui.addToolBar(QtCore.Qt.ToolBarArea(area), self.ui.toolbar)

        geometry = self.settings.value('geometry', None)
        if geometry:
            self.restoreGeometry(self.settings.value('geometry'))

        # prevent out of window position
        if self.pos().x() < 0 or self.pos().y() < 0:
            self.move(self.maya_window.geometry().center() - self.ui.geometry().center())

    def toolbar_moved(self, is_moving: bool):
        """Stores toolbar position when is docked to an area."""
        if is_moving:
            return

        self.settings.setValue('toolbar_orientation', int(self.ui.toolbar.orientation()))
        self.settings.setValue('toolbar_area', int(self.ui.toolBarArea(self.ui.toolbar)))

    def open_default_light_rig(self):
        """Opens the maya file used for render thumbnails."""
        self.status_message(thumbnail_default_scene)
        if os.path.exists(thumbnail_default_scene):
            dirty_file_dialog()
            cmds.file(thumbnail_default_scene, force=True, open=True)

    def status_message(self, message: str):
        """Writes a message into the statusbar."""
        self.ui.statusBar().showMessage(message)

    def resizeEvent(self, _):
        """Resize event callback."""
        self.resize_timer.start(100)  # 100 ms

    def resize_finished(self):
        """Resize finished callback."""
        index = self.ui.categories.currentRow()
        item = self.categories_widget.get_categories()[index]
        item.focus()

    def closeEvent(self, event: QtCore.QEvent):
        """Save user settings and close."""

        last_selected = self.categories_widget.current_category()
        if last_selected:
            self.settings.setValue('last_selected', last_selected.name())

        self.settings.setValue('geometry', self.saveGeometry())

        super().closeEvent(event)
