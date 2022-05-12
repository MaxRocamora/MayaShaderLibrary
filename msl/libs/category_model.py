from PySide2.QtGui import QIcon
from PySide2.QtCore import Qt, QAbstractListModel

from msl.ui.icons import get_icon


class CategoryModel(QAbstractListModel):
    def __init__(self, items=None):
        super().__init__()
        ''' list model for assets '''
        self.categories = items or []
        self.icons = {}

    def data(self, index, role):
        if role in [Qt.DisplayRole, Qt.EditRole]:
            text = self.categories[index.row()].name()
            return text

        if role == Qt.DecorationRole:
            return QIcon(get_icon('appIcon'))

    def getItem(self, index):
        row = index.row()
        if index.isValid() and 0 <= row < self.rowCount():
            return self.categories[row]

    def rowCount(self, index=0):
        return len(self.categories)
