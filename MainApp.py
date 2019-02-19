# -*- coding: utf-8 -*-


import sys
try:
    from PySide import QtCore
    from PySide import QtWidgets
except:
    from PyQt5.QtCore import pyqtSlot as Slot
    from PyQt5 import QtCore
    from PyQt5.QtCore import *
    from PyQt5.QtWidgets import *
    from PyQt5 import QtWidgets
    from PyQt5.QtQml import QQmlApplicationEngine,QQmlEngine, QQmlComponent
    import resources



class MainApp(QObject):
    def __init__(self):
        super(MainApp, self).__init__(parent)
        self.win = parent
        self.ctx = context


if __name__ == "__main__":
    app = QApplication(sys.argv)
    engine = QQmlApplicationEngine()
    ctx = engine.rootContext()
    engine.load(QUrl('qrc:/main.qml'))
    # win = engine.rootObjects()[0]
    # py_mainapp = MainApp(ctx, win)
    # ctx.setContextProperty("py_mainapp", py_mainapp)
    sys.exit(app.exec_())
