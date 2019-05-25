# -*- coding: utf-8 -*-
# Shader Library Init

import os
from .libs.utils.error import EnvironmentVariableNotFound


# Main PATHS
try:
    ARCANE_PATH = os.environ['ARCANE_PATH_2019']
except KeyError:
    raise EnvironmentVariableNotFound(
        'ARCANE_PATH_2019 Env Var not found.')

# Location of libraries for tools
try:
    ARCANE_LIBRARY_PATH = os.environ['ARCANE_LIBRARY_PATH_2019']
except KeyError:
    raise EnvironmentVariableNotFound(
        'ARCANE_LIBRARY_PATH_2019 Env Var not found.')

ARCANE_LIBRARY_SHADERRIG_PATH = ARCANE_LIBRARY_PATH + '/shaderRigs/'
ARCANE_LIBRARY_SHADERS_PATH = ARCANE_LIBRARY_PATH + "/shaders/"

appPath = os.path.dirname(__file__)
arcaneIcon = os.path.join(appPath, 'ui', 'icons', 'appIcon.png')
sshFile = os.path.join(appPath, 'ui', 'arcane.qss')
