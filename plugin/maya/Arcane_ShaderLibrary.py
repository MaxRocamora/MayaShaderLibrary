# -*- coding: utf-8 -*-
###########################################################################
#
# Maya Plugin 2018
# Author: Maximiliano Rocamora - maxirocamora@gmail.com
# Release: 05/2019
#
###########################################################################

import sys
import os
import maya.OpenMayaMPx as OpenMayaMPx

# Add ASL package root
try:
    arcanePath = os.environ['ARCANE_SHADER_LIBRARY']
except KeyError:
    print 'Missing Maya.env entry: ARCANE_SHADER_LIBRARY'

if arcanePath not in sys.path:
    sys.path.append(arcanePath)

kPluginCmdName = "ARCANE Tools ShaderLibrary 1.0"


def initializePlugin(mobject):
    ''' Initialize the script plug-in '''
    mplugin = OpenMayaMPx.MFnPlugin(mobject)
    from msl.ui.menu.menu import menuCreator
    menuCreator()


def uninitializePlugin(mobject):
    ''' Uninitialize the script plug-in '''
    mplugin = OpenMayaMPx.MFnPlugin(mobject)
    from msl.ui.menu.menu import menuCreator
    menuCreator().unloadMenu()
