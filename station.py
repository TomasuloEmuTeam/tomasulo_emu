# coding: utf-8

from mem import mem
from register import reg


class Station(object):
    """docstring for Station"""
    def __init__(self, name, size):
        super(Station, self).__init__()
        self.name = name
        self.size = size
        self.entry = {"%s%d"%(self.name, x):[-1, -1, -1, True, -1] for x in range(self.size)}

    def add(self, inst_num, arg1, arg2, arg3, types=True):
        choose = None
        for item in self.entry:
            if self.entry[item][0] == -1:
                choose = item
                break

        if choose == None:
            # print("station %s is full"%self.name)
            return False

        if arg3 == "load":
            self.entry[choose][0] = arg1
            reg.identify(arg1, choose)
            self.entry[choose][1] = arg2
        elif arg3 == "store":
            self.entry[choose][0] = reg.get(arg1)
            self.entry[choose][1] = arg2
        else:
            # addd | subd | mult | divd
            self.entry[choose][0] = arg1
            reg.identify(arg1, choose)
            self.entry[choose][1] = reg.get(arg2)
            self.entry[choose][2] = reg.get(arg3)
            self.entry[choose][3] = types

        self.entry[choose][4] = inst_num
        # print("%s : %s add a new instruction"%(self.name, choose))
        return True

    def check(self):
        for item in self.entry:
            if self.entry[item][0] != -1:
                return False

        return True

    def choose(self):
        for item in self.entry:
            if self.entry[item][0] != -1:
                flag = True
                for addr in self.entry[item]:
                    if type(addr) == str:
                        flag = False
                        # print(item, ":", self.entry[item])
                        break

                if flag:
                    # print("station %s choose %s"%(self.name, item))
                    ret = (item, self.entry[item][:])
                    # reset the choosed entry
                    # self.entry[item][0] = -1
                    return ret

        return False, None

    def update(self, name, value):
        for item in self.entry:
            for x in range(3):
                if self.entry[item][x] == name:
                    self.entry[item][x] = value

    def reset(self, key):
        if key in self.entry:
            self.entry[key][0] = -1

    def getAll(self):
        return self.entry


# class LoadStation(Station):
#     """docstring for LoadStation"""
#     def __init__(self, name="ld", size=3):
#         super(LoadStation, self).__init__(name, size)
    
#     def execute(self, identifier):
#         reg_addr = self.entry[identifier][0]
#         mem_addr = self.entry[identifier][1]
#         reg.update(reg_addr, mem.get(mem_addr))
#         self.entry[identifier][0] = -1


# class StoreStation(Station):
#     """docstring for StoreStation"""
#     def __init__(self, name="st", size=3):
#         super(StoreStation, self).__init__(name, size)
    
#     def execute(self, identifier):
#         reg_addr = self.entry[identifier][0]
#         mem_addr = self.entry[identifier][1]
#         mem.set(mem_addr, reg.get(reg_addr))
#         self.entry[identifier][0] = -1
        
