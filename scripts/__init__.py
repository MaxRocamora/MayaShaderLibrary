# -*- coding: utf-8 -*-
# Shader Library Init

import os
from .libs.utils.error import EnvironmentVariableNotFound


# Main PATHS
try:
    ARCANE_SHADERLIB_PATH = os.environ['ARCANE_SHADERLIB_PATH']
except KeyError:
    raise EnvironmentVariableNotFound(
        'ARCANE_SHADERLIB_PATH Env Var not found.')


SHADERS_PATH = ARCANE_SHADERLIB_PATH + "/maya/shaders/"

appPath = os.path.dirname(__file__)
arcaneIcon = os.path.join(appPath, 'ui', 'icons', 'appIcon.png')
sshFile = os.path.join(appPath, 'ui', 'arcane.qss')
thumbnail_default_scene = os.path.join(ARCANE_SHADERLIB_PATH, 'maya', 'scene')
