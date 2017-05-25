from itertools import chain

class Emulator:

    def loadCode(self, code):
        return True

    def setPC(self):
        return True

    def step(self):
        return True

    def getAllMem(self):
        return 123

    def setAllMem(self, data):
        return 123

    def getReg(self, name):
        return 111

    def setReg(self, name, value):
        return True

emu = Emulator()

