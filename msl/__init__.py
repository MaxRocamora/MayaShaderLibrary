# ----------------------------------------------------------------------------------------
# Maya Shader Library
# Author: maxirocamora@gmail.com
#
# Shader Library Init, Loader
# ----------------------------------------------------------------------------------------

import maya.cmds as cmds

from msl.config import QT_WIN_NAME
from msl.main import ShaderLibraryAPP


def run():
    """Run the ShaderLibraryAPP."""
    if cmds.window(QT_WIN_NAME, q=1, ex=1):
        cmds.deleteUI(QT_WIN_NAME)
    ShaderLibraryAPP()
