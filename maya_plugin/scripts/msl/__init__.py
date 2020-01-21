# -*- coding: utf-8 -*-
# Shader Library Init

import os

# Flag for valid plugin environment, if this is false the maya plugin wont load
VALID_ENV = True

# Root Path to tool (msl package)
ROOT_PATH = os.path.join(os.path.dirname(os.path.split(__file__)[0]))

# UI / Stylesheet / icons
ICON_FILE = os.path.join(ROOT_PATH, 'msl', 'ui', 'icons', 'appIcon.png')
QSS_FILE = os.path.join(ROOT_PATH, 'msl', 'ui', 'stylesheet', 'arcane.qss')
QSS_BUTTON = os.path.join(ROOT_PATH, 'msl', 'ui', 'stylesheet', 'shaderButton.qss')

# Maya Files and default shader repositoy
try:
    library_path = os.environ['MAYA_SHADER_LIBRARY']
except KeyError:
    library_path = ''
    print 'Missing Maya.env entry: MAYA_SHADER_LIBRARY'
    VALID_ENV = False

LIBRARY_SHADERS_PATH = os.path.join(library_path, 'shaders')
thumbnail_default_scene = os.path.join(library_path, 'scene', 'thumbnail_scene.ma')

# Check files existance
for filepath in [thumbnail_default_scene, LIBRARY_SHADERS_PATH, QSS_FILE, ICON_FILE]:
    if not os.path.exists(filepath):
        VALID_ENV = False
        print 'Maya Shader Library: Warning: Missing Path or File', filepath


if __name__ == '__main__':
    pass
