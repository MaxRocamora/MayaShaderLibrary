# ----------------------------------------------------------------------------------------
# Maya Shader Library
# Author: maxirocamora@gmail.com
# https://github.com/MaxRocamora/MayaShaderLibrary
#
# ----------------------------------------------------------------------------------------
from PySide2.QtCore import QObject, Signal


class GlobalSignals(QObject):
    """A container for global signals, which allow cross-application communication."""

    show_message = Signal(str)
    reload_categories = Signal(str)
    update_shader_ui = Signal(str, str, str, str)
    active_shader = Signal(object)


SIGNALS = GlobalSignals()
