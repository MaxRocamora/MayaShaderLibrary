# -*- coding: utf-8 -*-
# Shader Library Init

import os

# Root Path to tool (msl package)
rootPath = os.path.join(os.path.dirname(os.path.split(__file__)[0]))

# UI / Stylesheet / icons
arcaneIcon = os.path.join(rootPath, 'msl', 'ui', 'icons', 'appIcon.png')
sshFile = os.path.join(rootPath, 'msl', 'ui', 'stylesheet', 'arcane.qss')
sshButton = os.path.join(rootPath, 'msl', 'ui', 'stylesheet', 'shaderButton.qss')

# Maya Files and default shader repositoy
DEFAULT_SHADERS_PATH = os.path.join(rootPath, 'maya', 'shaders')
thumbnail_default_scene = os.path.join(rootPath, 'maya', 'scene', 'thumbnail_scene.ma')

# Check files
for filepath in [thumbnail_default_scene, DEFAULT_SHADERS_PATH, sshFile, arcaneIcon]:
    if not os.path.exists(filepath):
        print 'Arcane Shader Library: Warning: Missing Path', filepath
