# --------------------------------------------------------------------------------------------
# Maya Shader Library
# Author: maxirocamora@gmail.com
#
# Shader Library Init
# --------------------------------------------------------------------------------------------
import sys
import os
import pkgutil

from PySide2.QtGui import QIcon

# Flag for valid plugin environment, if this is false the maya plugin wont load
VALID_ENV = True

# Root Path to tool (msl package)
PY_VERSION = sys.version_info.major

package = pkgutil.get_loader("msl")
if not package:
    ROOT_PATH = os.path.dirname(__file__)
else:
    if PY_VERSION >= 3:
        ROOT_PATH = os.path.dirname(package.get_filename())
    else:
        ROOT_PATH = os.path.join(os.path.dirname(package.filename), 'msl')


# UI / Stylesheet / icons
APP_QICON = QIcon(os.path.join(ROOT_PATH, 'ui', 'icons', 'appIcon.png'))
QSS_FILE = os.path.join(ROOT_PATH, 'ui', 'stylesheet', 'arcane.qss')
QSS_BUTTON = os.path.join(ROOT_PATH, 'ui', 'stylesheet', 'shaderButton.qss')

# Maya Files and default shader repository
try:
    library_path = os.environ['MAYA_SHADER_LIBRARY']
except KeyError:
    library_path = ''
    print('Missing Maya.env entry: MAYA_SHADER_LIBRARY')
    VALID_ENV = False

LIBRARY_SHADERS_PATH = os.path.join(library_path, 'shaders')
thumbnail_default_scene = os.path.join(
    library_path, 'scene', 'thumbnail_scene.ma')

# Check core files existence
for filepath in [thumbnail_default_scene,
                 LIBRARY_SHADERS_PATH,
                 QSS_FILE, ]:
    if not os.path.exists(filepath):
        VALID_ENV = False
        print('Maya Shader Library: Warning: Missing Path or File', filepath)
