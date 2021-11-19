# -*- coding: utf-8 -*-
# Shader Library Init

from os import path as os_path
from os import environ as os_env
import pkgutil

# Flag for valid plugin environment, if this is false the maya plugin wont load
VALID_ENV = True

# Root Path to tool (msl package)
package = pkgutil.get_loader("msl")
ROOT_PATH = os_path.join(os_path.dirname(package.filename), 'msl')

# UI / Stylesheet / icons
ICON_FILE = os_path.join(ROOT_PATH, 'ui', 'icons', 'appIcon.png')
QSS_FILE = os_path.join(ROOT_PATH, 'ui', 'stylesheet', 'arcane.qss')
QSS_BUTTON = os_path.join(ROOT_PATH, 'ui', 'stylesheet', 'shaderButton.qss')

# Maya Files and default shader repository
try:
    library_path = os_env['MAYA_SHADER_LIBRARY']
except KeyError:
    library_path = ''
    print('Missing Maya.env entry: MAYA_SHADER_LIBRARY')
    VALID_ENV = False

LIBRARY_SHADERS_PATH = os_path.join(library_path, 'shaders')
thumbnail_default_scene = os_path.join(
    library_path, 'scene', 'thumbnail_scene.ma')

# Check core files existence
for filepath in [thumbnail_default_scene, LIBRARY_SHADERS_PATH, QSS_FILE, ICON_FILE]:
    if not os_path.exists(filepath):
        VALID_ENV = False
        print('Maya Shader Library: Warning: Missing Path or File', filepath)
