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

class ObdInterface(QObject):
    speedChangeSignal = pyqtSignal(int)
    engineLoadChangeSignal = pyqtSignal(int)
    rpmChangeSignal = pyqtSignal(int)
    coolantTempChangeSignal = pyqtSignal(int)
    kmsChangeSignal = pyqtSignal(int)

    def __init__(self,win):
        super(ObdInterface, self).__init__(win)
        self.win = win
        #self.rpmNeedle.setProperty('value',0)
        #self.speedNeedle.setProperty('value',0)
        #self.fuelNeedle.setProperty('value',0)
        self.connection = obd.Async(portstr="/dev/rfcomm0",fast=False,timeout=30)
        obd.logger.setLevel(obd.logging.DEBUG)
        self.speedChangeSignal.connect(self.updateSpeedUI, Qt.QueuedConnection)
        self.engineLoadChangeSignal.connect(self.updateEngineLoadUI, Qt.QueuedConnection)
        self.coolantTempChangeSignal.connect(self.updateCoolantTempUI, Qt.QueuedConnection)
        self.rpmChangeSignal.connect(self.updateRpmUI, Qt.QueuedConnection)
        self.kmsChangeSignal.connect(self.updateKmsUI, Qt.QueuedConnection)
        self.connection.watch(obd.commands.RPM, callback=self.updateRpm)
        self.connection.watch(obd.commands.SPEED, callback=self.updateSpeed)
        self.connection.watch(obd.commands.ENGINE_LOAD, callback=self.updateFuel)
        self.connection.watch(obd.commands.DISTANCE_W_MIL, callback=self.updateKms)
        self.connection.watch(obd.commands.COOLANT_TEMP, callback=self.updateTemp)

    def updateRpm(self,r):
        if not r.is_null():
            print("RPM "+str(r.value))
            self.rpmChangeSignal.emit(r.value.magnitude)

    def updateKms(self,r):
        if not r.is_null():
            print("Kms "+str(r.value))
            self.kmsChangeSignal.emit(r.value.magnitude)

    def updateTemp(self,r):
        if not r.is_null():
            print("Temp "+str(r.value))
            self.coolantTempChangeSignal.emit(r.value.magnitude)

    def updateSpeed(self,r):
        if not r.is_null():
            print("SPEED "+str(r.value))
            self.speedChangeSignal.emit(r.value.magnitude)

    def updateKmsUI(self,value):
        totalKms = self.win.findChild(QObject, 'totalKms')
        totalKms.setProperty('text',int(value))
        print("Kms set success")
 
    def updateSpeedUI(self,value):
        speedNeedle = self.win.findChild(QObject, 'speedoNeedle')
        speedNeedle.setProperty('value',int(value))
        print("Speed set success")
 
    def updateRpmUI(self,value):
        rpmNeedle = self.win.findChild(QObject, 'rpmNeedle')
        rpmNeedle.setProperty('value',int(value))
        print("RPM set success")
 
    def updateCoolantTempUI(self,value):
        enginTemp = self.win.findChild(QObject, 'enginTemp')
        enginTemp.setProperty('text',int(value))
        print("CoolantTemp set success")
 

    def updateEngineLoadUI(self,value):
        fuelNeedle = self.win.findChild(QObject, 'fuelNeedle')
        fuelNeedle.setProperty('value',int(value))
        print("Engine Load set success")
 
    def updateFuel(self,r):
        if not r.is_null():
            print("Engine Load "+str(r.value))
            self.engineLoadChangeSignal.emit(r.value.magnitude)

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

    speedChangeSignal = pyqtSignal(int)
    
    def __init__(self, context, loop, parent=None):
        super(MainApp, self).__init__(parent)
        self.win = parent
        self.ctx = context
        self.loop = loop
        self.speedChangeSignal.connect(self.updateSpeed, Qt.QueuedConnection)
        self.mockSpeed = ObdMock(20,10,100,0)
        self.mockRpm = ObdMock(1000,400,5000,0)
        self.mockFuel = ObdMock(100,1,100,0)
        self.mockEngineTemp = ObdMock(30,5,100,0)
        self.mockKm = ObdMock(4000,1,10000,0)

    async def setSpeed(self):
        print("started scanning speed")
        while True:
            speed = self.mockSpeed.getValue()
            print("speed "+str(speed))
            self.speedChangeSignal.emit(speed)
            await asyncio.sleep(1)


    def updateSpeed(self,value):
            speedNeedle = self.win.findChild(QObject, 'speedoNeedle')
            speedNeedle.setProperty('value',value)
        


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
            print("fuel "+str(fuel))
            rpmNeedle.setProperty('value',fuel)
            await asyncio.sleep(2)

    async def setKm(self):
        print("started scanning Kms")
        while True:
            totalKms = self.win.findChild(QObject, 'totalKms')
            kms = self.mockKm.getValue()
            print("kms "+str(kms))
            totalKms.setProperty('text',kms)
            await asyncio.sleep(2)

    async def setCoolantTemp(self):
        print("started scanning Temperature ")
        while True:
            engineTemp = self.win.findChild(QObject, 'enginTemp')
            temp = self.mockEngineTemp.getValue()
            print("temp "+str(temp))
            engineTemp.setProperty('text',temp)
            await asyncio.sleep(2)

    @Slot(QVariant)
    def startJob(self):
        loop = asyncio.get_event_loop()
        task = loop.create_task(self.setSpeed());
        asyncio.ensure_future(self.setSpeed());
        asyncio.ensure_future(self.setRpm());
        asyncio.ensure_future(self.setFuel());
        asyncio.ensure_future(self.setKm());
        asyncio.ensure_future(self.setCoolantTemp());

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
    #py_mainapp = MainApp(ctx, loop, win )
    win.show();
    print("aquiring the interface")
    try:
        obdi = ObdInterface(win)
        obdi.start()
    except:
        print("Error connecting")
        time.sleep(2)
        traceback.print_exc()
    #py_mainapp.startJob();
    #QtCore.QTimer.singleShot(1000000, py_mainapp.onStart())
    loop.run_forever()
    print("Program ended")
    #sys.exit(app.exec_())
