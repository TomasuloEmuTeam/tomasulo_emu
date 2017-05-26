from itertools import chain

class Emulator:

    def __init__(self):
        self.codeLines = None
        self.pc = 0

    def loadCode(self, code):
        self.codeLines = code
        return True

    def setPC(self, pc):
        self.pc = pc
        return True

    def step(self):
        self.pc += 1
        return True

    def getAllMem(self):
        return 123

    def setAllMem(self, data):
        return 123

    def getReg(self, type, addr):
        return {
            "expression": "2 + " + str(addr+self.pc),
            "value": 2 + addr + self.pc
        }

emu = Emulator()

