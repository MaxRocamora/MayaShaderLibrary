# ----------------------------------------------------------------------------------------
# Maya Shader Library
# Author: maxirocamora@gmail.com
#
# Shader Library Init, Loader
# ----------------------------------------------------------------------------------------

import maya.cmds as cmds

from msl.main import ShaderLibraryAPP
from msl.config import QT_WIN_NAME


def run():
    # load qt window
    if cmds.window(QT_WIN_NAME, q=1, ex=1):
        cmds.deleteUI(QT_WIN_NAME)
    ShaderLibraryAPP()
