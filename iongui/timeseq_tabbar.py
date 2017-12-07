__author__ = 'cqt'

from PyQt4 import QtGui, QtCore


class TabBarTest(QtGui.QTabBar):
    def __init__(self, parent):
        QtGui.QTabBar.__init__(self, parent)
        pass

class TabBar(QtGui.QTabBar):
    def __init__(self, parent):
        QtGui.QTabBar.__init__(self, parent)
        self._editor = QtGui.QLineEdit(self)
        self._editor.setWindowFlags(QtCore.Qt.Popup)
        self._editor.setFocusProxy(self)
        self._editor.editingFinished.connect(self.handleEditingFinished)
        self._editor.installEventFilter(self)

        self.create_context_menu()
        self.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        QtCore.QObject.connect(self, QtCore.SIGNAL('customContextMenuRequested(const QPoint&)'), self.on_context_menu)
        self.menu_index = 0

    def create_context_menu(self):
        self.popMenu = QtGui.QMenu(self)
        self.enable_item = QtGui.QAction('Enable', self)
        self.popMenu.addAction(self.enable_item)
        self.disable_item = QtGui.QAction('Disable', self)
        self.popMenu.addAction(self.disable_item)
        self.rename_item = QtGui.QAction('Rename', self)
        self.popMenu.addAction(self.rename_item)
        self.enable_item.triggered.connect(self.enable_slot)
        self.disable_item.triggered.connect(self.disable_slot)
        self.rename_item.triggered.connect(self.rename_slot)

    def enable_slot(self):
        print "enable", self.menu_index
        self.setTabTextColor(self.menu_index, QtCore.Qt.darkGreen)
        self.emit(QtCore.SIGNAL('enableTab'), self.menu_index, True)

    def disable_slot(self):
        print "disable", self.menu_index
        self.setTabTextColor(self.menu_index, QtCore.Qt.red)
        self.emit(QtCore.SIGNAL('enableTab'), self.menu_index, False)

    def rename_slot(self):
        print "rename", self.menu_index
        name, result = QtGui.QInputDialog.getText(self, "New name", "Enter new name")
        if result and (len(name) > 0):
            self.emit(QtCore.SIGNAL('renameTab'), str(name), self.menu_index)

    def setActive(self, active, index):
        self.menu_index = index
        if active:
            self.setTabTextColor(self.menu_index, QtCore.Qt.darkGreen)
        else:
            self.setTabTextColor(self.menu_index, QtCore.Qt.red)

    def setLabel(self, name, index):
        self.menu_index = index
        self.setTabText(self.menu_index, name)

    def eventFilter(self, widget, event):
        if ((event.type() == QtCore.QEvent.MouseButtonPress and
             not self._editor.geometry().contains(event.globalPos())) or
            (event.type() == QtCore.QEvent.KeyPress and
             event.key() == QtCore.Qt.Key_Escape)):
            self._editor.hide()
            return True
        return QtGui.QTabBar.eventFilter(self, widget, event)

    def mouseDoubleClickEvent(self, event):
        index = self.tabAt(event.pos())
        if index >= 0:
            self.editTab(index)

    def editTab(self, index):
        rect = self.tabRect(index)
        self._editor.setFixedSize(rect.size())
        self._editor.move(self.parent().mapToGlobal(rect.topLeft()))
        self._editor.setText(self.tabText(index))
        if not self._editor.isVisible():
            self._editor.show()

    def handleEditingFinished(self):
        index = self.currentIndex()
        if index >= 0:
            self._editor.hide()
            self.setTabText(index, self._editor.text())
            self.emit(QtCore.SIGNAL('renameTab'), index, self._editor.text())

    def on_context_menu(self, point):
        self.menu_index = self.tabAt(point)
        print "on context ", point, self.menu_index
        self.popMenu.exec_(self.mapToGlobal(point))
