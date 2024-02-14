# ----------------------------------------------------------------------------------------
# Maya Shader Library
# Author: maxirocamora@gmail.com
# https://github.com/MaxRocamora/MayaShaderLibrary
#
# ----------------------------------------------------------------------------------------
from PySide2.QtCore import QObject, Signal


class GlobalSignals(QObject):
    """A container for global signals, which allow cross-application communication."""

    reload_categories = Signal(str)
    # update_shot_files = Signal(str)


SIGNALS = GlobalSignals()
