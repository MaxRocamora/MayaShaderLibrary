# --------------------------------------------------------------------------------------------
# Maya Shader Library
# Author: maxirocamora@gmail.com
#
# Observer its loaded by the main app
# Holds selected shader from UI and the main UI
# When a shader is selected, the shader clicked signal
# sends itself to this class using 'selectedShader'
# property and updates ui texts
# --------------------------------------------------------------------------------------------

class ObserverUI(object):
    def __init__(self, main, ui):
        self.main = main
        self.ui = ui
        self.shader = False
        self.category = False
        self._categoryList = []

    @property
    def categoryList(self):
        return self._categoryList

    @categoryList.setter
    def categoryList(self, v):
        self._categoryList = v

    @property
    def selectedCategory(self):
        return self.category

    @selectedCategory.setter
    def selectedCategory(self, v):
        self.category = v
        if not v:
            self.shader = False
            return
        print('Category selected: {} Shaders {}'.format(
            v.name, len(v.shaders()))
        )

    @property
    def selectedShader(self):
        return self.shader

    @selectedShader.setter
    def selectedShader(self, v):
        self.shader = v
        self.updateUI()

    def updateUI(self):
        ''' update ui when user selects a shader '''
        self.ui.lbl_shaderName.setText(
            self.shader.name + ' / ' + self.shader.category.name)
        self.ui.lbl_shaderType.setText(self.shader.shaderType)
        self.ui.lbl_shaderUserPC.setText(
            self.shader.user + ' / ' + self.shader.pc)
        self.ui.lbl_shaderCode.setText(self.shader.idName)
        self.ui.te_notes.setText(self.shader.notes)
