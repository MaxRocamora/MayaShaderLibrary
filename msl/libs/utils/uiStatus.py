# --------------------------------------------------------------------------------------------
# UI StatusBar Class
#
# imported as uiStatusBar
# instanced as: self.uiBar = uiStatus.uiStatusbar()
# This class connects the ui status bar widget to some diplay messages methods.
# --------------------------------------------------------------------------------------------


class Statusbar():
    def __init__(self, _qwidget):
        '''
         _qwidget ::: widget of the status bar ui
        '''
        self.uiBar = _qwidget
        self.success('', timed=0)

    def success(self, msg, timed=0):
        # Color green message / For succesful operations
        if timed > 0:
            self.uiBar.showMessage(msg, timed)
        else:
            self.uiBar.showMessage(msg)
        self.uiBar.setStyleSheet("color: lime; background: rgba(20, 20, 20, 255);")  # green warning

    def inform(self, msg, timed=0):
        # Color orange message / for inform messages
        if timed > 0:
            self.uiBar.showMessage(msg, timed)
        else:
            self.uiBar.showMessage(msg)
        self.uiBar.setStyleSheet("color: orange; background: rgba(20, 20, 20, 255);")  # orange warning

    def warning(self, msg):
        # Color yellow message / for warning messages
        self.uiBar.showMessage(msg)
        self.uiBar.setStyleSheet("color: yellow; background: rgba(20, 20, 20, 255);")  # yellow warning

    def error(self, msg):
        # Color RED message / # for failed operations
        self.uiBar.showMessage(msg)
        self.uiBar.setStyleSheet("color: red; background: rgba(20, 20, 20, 255);")  # red warning
