# coding: utf-8

class Reg(object):
    """Register class
    the register format:
        | True/False | content/station identifier |
    """
    def __init__(self, size=11):
        super(Reg, self).__init__()
        self.size = size

        # init registers
        self.arr  = [0.0 for x in range(self.size)]
        
    def identify(self, i, name):
        print("identify register %d as %s"%(i, name))
        self.arr[i] = name

    def update(self, i, con):
        print("update register %d as %f"%(i, con))
        self.arr[i] = con

    def get(self, i):
        # if self.arr[i][0]:
        #     print("get register %d, its content is %f"%(i, self.arr[i][1]))
        # else:
        #     print("get register %d, its identifier is %f"%(i, self.arr[i][1]))
        # return self.arr[i][0], self.arr[i][1]
        return self.arr[i]

    def print(self):
        print("All registers:")
        for x in range(self.size):
            print("reg F%d:"%(x), self.arr[x])
        print()

    def checkAll(self):
        for x in range(self.size):
            if type(self.arr[x]) == str:
                return False

        return True

reg = Reg()
