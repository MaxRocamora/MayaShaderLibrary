# ----------------------------------------------------------------------------------------
# Maya Shader Library
# Author: maxirocamora@gmail.com
#
# Shader Library Init, Loader
# ----------------------------------------------------------------------------------------
import os
import pkgutil

from PySide2.QtGui import QIcon

QT_WIN_NAME = 'Arcane2:Qt_ShaderLibrary_ui'

# Flag for valid plugin environment, if this is false the maya plugin wont load
VALID_ENV = True

package = pkgutil.get_loader("msl")
if package:
    ROOT_PATH = os.path.dirname(package.get_filename())
else:
    ROOT_PATH = os.path.dirname(__file__)


# Stylesheet / icons / Url
APP_QICON = QIcon(os.path.join(ROOT_PATH, 'ui', 'icons', 'appIcon.png'))
QSS_FILE = os.path.join(ROOT_PATH, 'ui', 'stylesheet', 'arcane.qss')
QSS_BUTTON = os.path.join(ROOT_PATH, 'ui', 'stylesheet', 'shaderButton.qss')
URL_DOC = 'https://mayashaderlibrary.readthedocs.io'

# Maya Files and default shader repository
try:
    library_path = os.environ['MAYA_SHADER_LIBRARY']
except KeyError:
    library_path = ''
    print('Missing Maya.env entry: MAYA_SHADER_LIBRARY')
    VALID_ENV = False

LIBRARY_SHADERS_PATH = os.path.join(library_path, 'shaders')
thumbnail_default_scene = os.path.join(library_path, 'scene', 'thumbnail_scene.ma')

# Check core files existence
for filepath in [thumbnail_default_scene,
                 LIBRARY_SHADERS_PATH,
                 QSS_FILE, ]:
    if not os.path.exists(filepath):
        VALID_ENV = False
        print('Maya Shader Library: Warning: Missing Path or File', filepath)
