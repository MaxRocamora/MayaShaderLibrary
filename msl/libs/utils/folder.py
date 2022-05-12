# ----------------------------------------------------------------------------------------
# Maya Shader Library
# Author: maxirocamora@gmail.com
# https://github.com/MaxRocamora/MayaShaderLibrary
#
# ----------------------------------------------------------------------------------------

import os
import subprocess


def browse(folder):
    location = os.path.abspath(folder)
    if os.path.exists(location):
        subprocess.Popen("explorer " + location)
