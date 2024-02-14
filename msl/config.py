# ----------------------------------------------------------------------------------------
# Maya Shader Library
# Author: maxirocamora@gmail.com
# https://github.com/MaxRocamora/MayaShaderLibrary
#
# Shader Library Init, Loader
# ----------------------------------------------------------------------------------------
import os
import pkgutil

from PySide2.QtGui import QIcon

import maya.cmds as cmds

QT_WIN_NAME = 'Arcane2:Qt_ShaderLibrary_ui'

package = pkgutil.get_loader('msl')
if package:
    ROOT_PATH = os.path.dirname(package.get_filename())
else:
    ROOT_PATH = os.path.dirname(__file__)


# Stylesheet / icons / Url
APP_QICON = QIcon(os.path.join(ROOT_PATH, 'ui', 'icons', 'app.png'))
QSS_FILE = os.path.join(ROOT_PATH, 'ui', 'stylesheet', 'arcane.qss')
QSS_BUTTON = os.path.join(ROOT_PATH, 'ui', 'stylesheet', 'shaderButton.qss')
URL_DOC = 'https://mayashaderlibrary.readthedocs.io'

# Shader repository location, from env variable or default
DEFAULT_LIBRARY_PATH = os.path.join(os.path.dirname(ROOT_PATH), 'library')
library_path = os.getenv('MAYA_SHADER_LIBRARY', DEFAULT_LIBRARY_PATH)
LIBRARY_PATH = os.path.join(library_path, 'shaders')

# Default thumbnail maya scene
thumbnail_default_scene = os.path.join(library_path, 'scene', 'thumbnail_scene.ma')

# Check core files existence
for filepath in [thumbnail_default_scene, LIBRARY_PATH, QSS_FILE]:
    if not os.path.exists(filepath):
        cmds.warning('Maya Shader Library: Missing Critical Path or File', filepath)
