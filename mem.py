# coding: utf-8

class Mem(object):
    """docstring for Memory"""
    def __init__(self, size=4096):
        super(Mem, self).__init__()

        # memory size
        self.size = size

        # init memory as zero
        self.arr  = [0.0 for x in range(size)]
        
    def set(self, i, con):
        # print("set mem[%d] as %f"%(i, con))
        self.arr[i] = con

    def setAll(self, data):
        for x in range(self.size):
            self.arr[x] = data[x]

    def get(self, i):
        # print("get mem[%d]"%i)
        return self.arr[i]

    def getAll(self):
        return self.arr[:]

mem = Mem()
