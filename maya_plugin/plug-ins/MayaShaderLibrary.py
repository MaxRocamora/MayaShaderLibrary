# -*- coding: utf-8 -*-
###########################################################################
#
# Maya Plugin 2018
# Author: Maximiliano Rocamora - maxirocamora@gmail.com
# First Release: 05/2019
#
###########################################################################

import maya.OpenMayaMPx as OpenMayaMPx
from msl import VALID_ENV


kPluginCmdName = "Maya Shader Library 1.1"


def initializePlugin(mobject):
    ''' Initialize the script plug-in '''
    if not VALID_ENV:
        print 'Unable to initializePlugin', kPluginCmdName
        return

    mplugin = OpenMayaMPx.MFnPlugin(mobject)


def uninitializePlugin(mobject):
    ''' Uninitialize the script plug-in '''
    mplugin = OpenMayaMPx.MFnPlugin(mobject)
