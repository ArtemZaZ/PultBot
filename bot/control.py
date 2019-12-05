from utility import receiver
from utility.eventmaster import EventMaster, Event


class Control:
    def __init__(self):
        self._ip = None
        self._port = None
        self._receiver = None
        self._eventDict = {
            "turnForward": Event("turnForward"),
            "move": Event("move"),
            "rotate": Event("rotate"),
            "turnAll": Event("turnAll"),
            "setAuto": Event("setAuto"),
            "setCamera": Event("setCamera"),
            "turnFirstAxisArg": Event("turnFirstAxisArg"),
            "turnSecondAxisArg": Event("turnSecondAxisArg"),
            "turnThirdAxisArg": Event("turnThirdAxisArg"),
            "turnFourthAxisArg": Event("turnFourthAxisArg"),
            "turnFifthAxisArg": Event("turnFifthAxisArg"),
            "setSensivityArg": Event("setSensivityArg"),
            "setIntensivityArg": Event("setIntensivityArg"),
        }
        self._oldPackage = [None, None, None, None, None, None, None, None, None, None, None, None, None]
        self._eventMaster = EventMaster()
        self._eventMaster.append(self._eventDict.get("turnForward"))
        self._eventMaster.append(self._eventDict.get("move"))
        self._eventMaster.append(self._eventDict.get("rotate"))
        self._eventMaster.append(self._eventDict.get("turnAll"))
        self._eventMaster.append(self._eventDict.get("setCamera"))
        self._eventMaster.append(self._eventDict.get("turnFirstAxisArg"))
        self._eventMaster.append(self._eventDict.get("turnSecondAxisArg"))
        self._eventMaster.append(self._eventDict.get("turnThirdAxisArg"))
        self._eventMaster.append(self._eventDict.get("turnFourthAxisArg"))
        self._eventMaster.append(self._eventDict.get("turnFifthAxisArg"))
        self._eventMaster.append(self._eventDict.get("setAuto"))
        self._eventMaster.append(self._eventDict.get("setSensivityArg"))
        self._eventMaster.append(self._eventDict.get("setIntensivityArg"))
        self._eventMaster.start()

    def connect(self, ip, port):
        self._receiver = receiver.Receiver(ip, port)
        self._receiver.packageFormat = "fbbff5f?bb"

        def onReceive(data):
            if data[0] != self._oldPackage[0]:
                self._eventDict["turnForward"].push(data[0])

            if data[1] != self._oldPackage[1]:
                self._eventDict["move"].push(data[1])

            if data[2] != self._oldPackage[2]:
                self._eventDict["rotate"].push(data[2])

            if data[3] != self._oldPackage[3]:
                self._eventDict["turnAll"].push(data[3])

            if data[4] != self._oldPackage[4]:
                self._eventDict["setCamera"].push(data[4])

            if data[5] != self._oldPackage[5]:
                self._eventDict["turnFirstAxisArg"].push(data[5])

            if data[6] != self._oldPackage[6]:
                self._eventDict["turnSecondAxisArg"].push(data[6])

            if data[7] != self._oldPackage[7]:
                self._eventDict["turnThirdAxisArg"].push(data[7])

            if data[8] != self._oldPackage[8]:
                self._eventDict["turnFourthAxisArg"].push(data[8])

            if data[9] != self._oldPackage[9]:
                self._eventDict["turnFifthAxisArg"].push(data[9])

            if data[10] != self._oldPackage[10]:
                self._eventDict["setAuto"].push(data[10])

            if data[11] != self._oldPackage[11]:
                self._eventDict["setAuto"].push(data[11])

            if data[12] != self._oldPackage[12]:
                self._eventDict["setAuto"].push(data[12])

            self._oldPackage = data[:]

        self._receiver.connectToEvent(onReceive, "onReceive")
        self._receiver.connect()

    def disconnect(self):
        self._receiver.disconnect()

    def connectToEvent(self, foo, toEvent):
        event = self._eventDict[toEvent]
        event.connect(foo)
