# ----------------------------------------------------------------------------------------
# Maya Shader Library
# Author: maxirocamora@gmail.com
# https://github.com/MaxRocamora/MayaShaderLibrary
#
# UI StatusBar Class
# imported as uiStatusBar
# instanced as: self.statusbar = uiStatus.uiStatusbar()
# ----------------------------------------------------------------------------------------


class Statusbar():
    def __init__(self, widget):
        ''' Display custom messages over the ui status bar widget.
        Args:
            widget (widget) main ui statusbar widget
        '''
        self.statusbar = widget

    def ok(self, msg, timed=0):
        '''Color green message / for successful operations'''
        if timed > 0:
            self.statusbar.showMessage(msg, timed)
        else:
            self.statusbar.showMessage(msg)
        self.statusbar.setStyleSheet(
            "color: lime; background: rgba(20, 20, 20, 255);")  # green warning

    def info(self, msg, timed=0):
        '''Color orange message / for inform messages'''
        if timed > 0:
            self.statusbar.showMessage(msg, timed)
        else:
            self.statusbar.showMessage(msg)
        self.statusbar.setStyleSheet(
            "color: orange; background: rgba(20, 20, 20, 255);")

    def warning(self, msg):
        '''Color yellow message / for warning messages'''
        self.statusbar.showMessage(msg)
        self.statusbar.setStyleSheet(
            "color: yellow; background: rgba(20, 20, 20, 255);")

    def error(self, msg):
        '''Color RED message / for failed operations'''
        self.statusbar.showMessage(msg)
        self.statusbar.setStyleSheet(
            "color: red; background: rgba(20, 20, 20, 255);")
