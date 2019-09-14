# -*- coding: utf-8 -*-


import sys
import quamash
import asyncio
import random
import obd
import time

try:
    from PySide import QtCore
    from PySide import QtWidgets
except:
    from PyQt5.QtCore import pyqtSlot as Slot, QVariant
    from PyQt5 import QtCore
    from PyQt5.QtCore import *
    from PyQt5.QtWidgets import *
    from PyQt5 import QtWidgets
    from PyQt5.QtQml import QQmlApplicationEngine,QQmlEngine, QQmlComponent
    import resources

class ObdInterface:
    def __init__(self,win):
        self.win = win
        self.connection = obd.Async("/dev/rfcomm0")
        self.rpmNeedle = self.win.findChild(QObject, 'rpmNeedle')
        self.speedNeedle = self.win.findChild(QObject, 'speedoNeedle')
        self.fuelNeedle = self.win.findChild(QObject, 'fuelNeedle')
        self.rpmNeedle.setProperty('value',0)
        self.speedNeedle.setProperty('value',0)
        self.fuelNeedle.setProperty('value',0)
        self.connection.watch(obd.commands.RPM, callback=self.updateRpm)
        self.connection.watch(obd.commands.SPEED, callback=self.updateSpeed)
        #self.connection.watch(obd.commands.FUEL_LEVEL, callback=self.updateFuel)

    def updateRpm(self,r):
        if not r.is_null():
            print("RPM "+str(r.value.magnitude))
            self.rpmNeedle.setProperty('value',r.value.magnitude)

    def updateSpeed(self,r):
        if not r.is_null():
            print("SPEED "+str(r.value.magnitude))
            self.speedNeedle.setProperty('value',r.value.magnitude)

    def updateFuel(self,r):
        if not r.is_null():
            print("FUEL "+str(r.value))
            self.fuelNeedle.setProperty('value',r.value.magnitude)

    def start(self):
        self.connection.start()


class ObdMock:
    def __init__(self,baseValue,maxIncrement,maxValue,minValue):
        self.test=True
        self.baseValue=baseValue
        self.maxIncrement=maxIncrement
        self.maxValue=maxValue
        self.minValue=minValue
        self.increasing = True

    def getValue(self):
        speedVariance = random.randint(0, self.maxIncrement)
        if(self.increasing):
            self.baseValue += speedVariance
            if(self.baseValue>self.maxValue):
                self.increasing=False
        else:
            self.baseValue -= speedVariance
            if(self.baseValue<self.minValue):
                self.increasing = True

        return self.baseValue



class MainApp(QObject):
    def __init__(self, context, loop, parent=None):
        super(MainApp, self).__init__(parent)
        self.win = parent
        self.ctx = context
        self.loop = loop
        self.mockSpeed = ObdMock(20,10,100,0)
        self.mockRpm = ObdMock(1000,400,5000,0)
        self.mockFuel = ObdMock(100,1,100,0)

    async def setSpeed(self):
        print("started scanning speed")
        while True:
            speedNeedle = self.win.findChild(QObject, 'speedoNeedle')
            rpmNeedle = self.win.findChild(QObject, 'rpmNeedle')
            rpmNeedle = self.win.findChild(QObject, 'fuelNeedle')
            speed = self.mockSpeed.getValue()
            print("speed "+str(speed))
            speedNeedle.setProperty('value',speed)
            await asyncio.sleep(1)

    async def setRpm(self):
        print("started scanning rpm")
        while True:
            rpmNeedle = self.win.findChild(QObject, 'rpmNeedle')
            rpm = self.mockRpm.getValue()
            print("rpm "+str(rpm))
            rpmNeedle.setProperty('value',rpm)
            await asyncio.sleep(0.3)

    async def setFuel(self):
        print("started scanning fuel")
        while True:
            rpmNeedle = self.win.findChild(QObject, 'fuelNeedle')
            fuel = self.mockFuel.getValue()
            print("rpm "+str(fuel))
            rpmNeedle.setProperty('value',fuel)
            await asyncio.sleep(2)

    @Slot(QVariant)
    def startJob(self):
        loop = asyncio.get_event_loop()
        #task = loop.create_task(self.setSpeed());
        asyncio.ensure_future(self.setSpeed());
        asyncio.ensure_future(self.setRpm());
        asyncio.ensure_future(self.setFuel());

    def onStart(self):
        print("Test");
        task = asyncio.create_task(self.setSpeed());
        loop.run_until_complete(task,loop=self.loop)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    loop = quamash.QEventLoop(app)
    print("setting event loop")
    asyncio.set_event_loop(loop)  # NEW must set the event loop
    engine = QQmlApplicationEngine()
    ctx = engine.rootContext()
    #ctx.setContextProperty("py_mainapp", py_mainapp)
    engine.load(QUrl('qrc:/main.qml'))
    win = engine.rootObjects()[0]
    py_mainapp = MainApp(ctx, loop, win )
    win.show();
    #obdi = ObdInterface(win)
    #obdi.start()
    py_mainapp.startJob();
    #QtCore.QTimer.singleShot(1000000, py_mainapp.onStart())
    loop.run_forever()
    #sys.exit(app.exec_())
