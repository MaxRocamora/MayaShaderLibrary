# -*- coding: utf-8 -*-
###########################################################################
#
# Maya Plugin 2018
# Author: Maximiliano Rocamora - maxirocamora@gmail.com
# Release: 05/2019
#
###########################################################################

import maya.OpenMayaMPx as OpenMayaMPx


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
