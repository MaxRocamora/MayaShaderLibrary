# -*- coding: utf-8 -*-
###########################################################################
#
# Maya Plugin
# Author: Maximiliano Rocamora - maxirocamora@gmail.com
# Release: 05/2019
#
###########################################################################

import sys
import os
import maya.OpenMayaMPx as OpenMayaMPx


class EnvironmentVariableNotFound(Exception):
    '''Raise when a required environment variable os not found. '''
    pass


# Main PATHS
try:
    ARCANE_SHADERLIB_PATH = os.environ['ARCANE_SHADERLIB_PATH']
    sys.path.append(ARCANE_SHADERLIB_PATH)
except KeyError:
    raise EnvironmentVariableNotFound(
        'ARCANE_SHADERLIB_PATH Env Var not found.')

kPluginCmdName = "ARCANE Tools ShaderLibrary 1.0"


def initializePlugin(mobject):
    ''' Initialize the script plug-in '''
    mplugin = OpenMayaMPx.MFnPlugin(mobject)
    from plugin.ui.menu import menuCreator
    menuCreator()


def uninitializePlugin(mobject):
    ''' Uninitialize the script plug-in '''
    mplugin = OpenMayaMPx.MFnPlugin(mobject)
    from plugin.ui.menu import menuCreator
    menuCreator().unloadMenu()
