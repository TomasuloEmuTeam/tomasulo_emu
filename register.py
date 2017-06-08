# coding: utf-8

class Reg(object):
    """Register class
    the register format:
        | content/station identifier |
    """
    def __init__(self, size=11):
        super(Reg, self).__init__()
        self.size = size

        # init registers
        self.arr  = [0.0 for x in range(self.size)]
        
    def identify(self, i, name):
        # print("identify register %d as %s"%(i, name))
        self.arr[i] = name

    def update(self, i, con):
        # print("update register %d as %f"%(i, con))
        self.arr[i] = con

    def get(self, i):
        return self.arr[i]

    def getAll(self):
        return self.arr[:]

    def print(self):
        print("All registers:")
        for x in range(self.size):
            print("reg F%d:"%(x), self.arr[x])
        print()

# global register variable
reg = Reg()
