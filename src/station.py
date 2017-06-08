# coding: utf-8

from mem import mem
from register import reg


class Station(object):
    """docstring for Station

    Data Member:
        name  : ld/st/add/mult
        size  : entry size
        entry : item dict
        entry format:
            { name : [-1/destOP, sourceOP1, sourceOP2, add/sub(True/False), inst_num]}
    """

    def __init__(self, name, size):
        super().__init__()
        self.name = name
        self.size = size
        self.entry = {"%s%d"%(self.name, x):[-1, -1, -1, True, -1] for x in range(self.size)}

    def add(self, inst_num, arg1, arg2, arg3, types=True):
        """add an instruction to the reservation station. if the station is full, return False"""

        choose = None
        for item in self.entry:
            if self.entry[item][0] == -1:
                choose = item
                break

        if choose == None:
            return False

        if arg3 == "load":
            # LD
            self.entry[choose][0] = arg1
            reg.identify(arg1, choose)
            self.entry[choose][1] = arg2
        elif arg3 == "store":
            # ST
            self.entry[choose][0] = reg.get(arg1)
            self.entry[choose][1] = arg2
        else:
            # ADDD | SUBD | MULT | DIVD
            self.entry[choose][0] = arg1
            reg.identify(arg1, choose)
            self.entry[choose][1] = reg.get(arg2)
            self.entry[choose][2] = reg.get(arg3)
            self.entry[choose][3] = types

        self.entry[choose][4] = inst_num
        return True

    def empty(self):
        """check whether the station is empty or not"""

        for item in self.entry:
            if self.entry[item][0] != -1:
                return False

        return True

    def choose(self):
        """choose an usable instruction"""

        ret = (False, None)
        min_inst_num = 0xffffffff
        for (name, inst) in self.entry.items():
            if inst[0] != -1:
                flag = True
                for addr in inst:
                    if type(addr) == str:
                        flag = False
                        break

                if flag and inst[4] < min_inst_num:
                    ret = (name, inst[:])
                    min_inst_num = inst[4]

        return ret

    def checkMem(self, mem_addr, inst_num):
        """check the store/load station mem_addr and judge whether an LD/ST instruction can be executed now or not"""

        for (name, inst) in self.entry.items():
            if inst[0] != -1 and inst[1] == mem_addr and inst[4] < inst_num:
                return False

        return True

    def update(self, name, value):
        """update the item identifiers"""

        for item in self.entry:
            for x in range(3):
                if self.entry[item][x] == name:
                    self.entry[item][x] = value

    def reset(self, key):
        """reset the choosed item"""

        if key in self.entry:
            self.entry[key][0] = -1

    def getAll(self):
        return self.entry

    def print(self):
        print(self.name, self.entry)
