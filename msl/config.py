# ----------------------------------------------------------------------------------------
# Maya Shader Library
# Author: maxirocamora@gmail.com
# https://github.com/MaxRocamora/MayaShaderLibrary
#
# Shader Library Init, Loader
# ----------------------------------------------------------------------------------------
import os
import pkgutil
from enum import Enum

import maya.cmds as cmds

try:
    from PySide2.QtGui import QIcon
except ImportError:
    from PySide6.QtGui import QIcon

QT_WIN_NAME = 'Arcane2:Qt_ShaderLibrary_ui'

package = pkgutil.get_loader('msl')
if package:
    ROOT_PATH = os.path.dirname(package.get_filename())
else:
    ROOT_PATH = os.path.dirname(__file__)


# * Stylesheet / icons / Url
UI = os.path.join(ROOT_PATH, 'resources', 'ui', 'main.ui')
APP_QICON = QIcon(os.path.join(ROOT_PATH, 'resources', 'icons', 'app.png'))
QSS_FILE = os.path.join(ROOT_PATH, 'resources', 'css', 'stylesheet.qss')
URL_DOC = 'https://mayashaderlibrary.readthedocs.io'

# * Shader repository location, from env variable or default path
DEFAULT_LIBRARY_PATH = os.path.join(os.path.dirname(ROOT_PATH), 'library')
library_path = os.getenv('MAYA_SHADER_LIBRARY', DEFAULT_LIBRARY_PATH)
LIBRARY_PATH = os.path.join(library_path, 'shaders')

# * Default thumbnail maya scene
thumbnail_default_scene = os.path.join(library_path, 'scene', 'thumbnail_scene.ma')

# * Check core files existence
for filepath in [thumbnail_default_scene, LIBRARY_PATH, QSS_FILE]:
    if not os.path.exists(filepath):
        cmds.warning('Maya Shader Library: Missing Critical Path or File', filepath)


class WidgetViewMode(Enum):
    """Defines the widget type for shader widget display."""

    ICON = 0
    LIST = 1


class WidgetViewModeWidth(Enum):
    """Defines the widget type for shader widget display."""

    ICON = 140
    LIST = 300
