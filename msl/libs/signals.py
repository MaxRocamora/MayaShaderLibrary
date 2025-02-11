# ----------------------------------------------------------------------------------------
# Maya Shader Library
# Author: maxirocamora@gmail.com
# https://github.com/MaxRocamora/MayaShaderLibrary
#
# ----------------------------------------------------------------------------------------
try:
    from PySide2.QtCore import QObject, Signal
except ImportError:
    from PySide6.QtCore import QObject, Signal


class GlobalSignals(QObject):
    """A container for global signals, which allow cross-application communication."""

    show_message = Signal(str)
    reload_categories = Signal(str)
    display_shader_notes = Signal(str)


SIGNALS = GlobalSignals()
