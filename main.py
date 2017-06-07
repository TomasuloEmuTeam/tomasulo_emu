from mem import mem
from register import reg
from station import *

from queue import Queue

load  = Station("ld", 3)
store = Station("st", 3)
adder = Station("add", 3)
mult  = Station("mult", 2)

# cycle number
cycle = 0
inst_num = 0

instructions = []
stations = {}
states   = []

def init(inst_list):
    # set instruction lists
    def setInst(inst_list):
        global instructions

        instructions = inst_list[:]

    def initStation():
        global stations

        stations = {
            load  : {
                "num"  : -1,
                "iden" : None,
                "inst" : None
            },
            store : {
                "num"  : -1,
                "iden" : None,
                "inst" : None
            },
            adder : {
                "num"  : -1,
                "iden" : None,
                "inst" : None
            },
            mult  : {
                "num"  : -1,
                "iden" : None,
                "inst" : None
            }
        }

    global cycle, inst_num, states
    cycle = 0
    inst_num = 0
    setInst(inst_list)
    initStation()
    states = [[None, None, None] for x in range(len(instructions))]

def getStates():
    return states

def setAllMem(data):
    mem.setAll(data)

def getAllMem():
    return mem.getAll()

def getAllReg():
    reg_vect = reg.getAll()
    # print("reg.getAll() = \n", reg_vect)
    ret = []
    for item in reg_vect:
        if type(item) == str:
            ret.append([None, item])
        else:
            ret.append([item, None])

    return ret

def getLoadQueue():
    load_vect = load.getAll()
    ret = []
    for (name, inst) in load_vect.items():
        item = [name]
        if inst[0] == -1:
            item += ["N", None, None]
        else:
            item += (["Y"] + inst[0:2])

        ret.append(item)

    return ret

def getStoreQueue():
    store_vect = store.getAll()
    ret = []
    for (name, inst) in store_vect.items():
        item = [name]
        if inst[0] == -1:
            item += ["N", None, None, None]
        else:
            item.append("Y")
            item.append(inst[1])
            if type(inst[0]) == str:
                item += [inst[0], None]
            else:
                item += [None, inst[0]]

        ret.append(item)

    return ret

def getReservation():
    ret = []

    adder_vect = adder.getAll()
    mult_vect  = mult.getAll()
    all_items  = list(adder_vect.items()) + list(mult_vect.items())

    for (name, inst) in all_items:
        item = [name]
        if inst[0] == -1:
            item.append("N")
            for x in range(5):
                item.append(None)
        else:
            item.append("Y")
            # for x in range(3):
            item.append(inst[0])
            for i in range(1, 3):
                if type(inst[i]) == str:
                    item += [inst[i], None]
                else:
                    item += [None, inst[i]]

        ret.append(item)

    return ret


def step():
    global cycle, inst_num, states

    def update(arg):
        (reg_addr, name, value) = arg
        reg.update(reg_addr, value)
        for sta in stations:
            sta.update(name, value)

    def reset(name):
        for sta in stations:
            sta.reset(name)

    def execute(name, inst):
        # print("exec", name, inst)
        cur_inst_num = inst[4]

        if name[:-1] == "ld":
            # update(inst[0], name, mem.get(inst[1]))
            return (inst[0], name, mem.get(inst[1]))
        elif name[:-1] == "st":
            # update(inst[0], name, reg.get(inst[0]))
            mem.set(inst[1], inst[0])
            return (None, name, None)
        else:
            # reg_val1 = reg.get(inst[1])
            reg_val1 = inst[1]
            reg_val2 = inst[2]
            # reg_val2 = reg.get(inst[2])
            if name[:-1] == "add":
                if inst[3]:
                    # add
                    value = reg_val1 + reg_val2
                else:
                    # sub
                    value = reg_val1 - reg_val2
                # update(inst[0], name, value)
                return (inst[0], name, value)
            elif name[:-1] == "mult":
                if inst[3]:
                    # mult
                    value = reg_val1 * reg_val2
                else:
                    # div
                    try:
                        value = reg_val1 / reg_val2
                    except Exception:
                        value = float("nan")

                # update(inst[0], name, value)
                return (inst[0], name, value)

    def exeDone():
        if inst_num != len(instructions):
            return False

        for sta in stations:
            if not sta.check():
                return False

        return True

    if inst_num < len(instructions):
        instruct = instructions[inst_num]
        s = instruct.split(" ")

        # print("instruct:", instruct)

        flag = None
        if s[0] == "LD":
            flag = load.add(inst_num, int(s[1][1:]), int(s[2], 16), "load")
        elif s[0] == "ST":
            flag = store.add(inst_num, int(s[1][1:]), int(s[2], 16), "store")
        elif s[0] == "ADDD":
            flag = adder.add(inst_num, int(s[1][1:]), int(s[2][1:]), int(s[3][1:]))
        elif s[0] == "SUBD":
            flag = adder.add(inst_num, int(s[1][1:]), int(s[2][1:]), int(s[3][1:]), False)
        elif s[0] == "MULD":
            flag = mult.add(inst_num, int(s[1][1:]), int(s[2][1:]), int(s[3][1:]))
        elif s[0] == "DIVD":
            flag = mult.add(inst_num, int(s[1][1:]), int(s[2][1:]), int(s[3][1:]), False)
        else:
            print("wrong instruction: (%s)!!!"%instruct)
            # return False

        if flag:
            states[inst_num][0] = cycle
            inst_num += 1

    # choose instructions to execute
    for sta in stations:
        num = stations[sta]["num"]
        if num == -1:
            choose = sta.choose()
            if choose[0] != False:
                # print("choose", choose)
                if sta == mult:
                    if choose[1][3] == True:
                        # muld
                        stations[sta]["num"] = 10
                    else:
                        # divd
                        stations[sta]["num"] = 40
                else:
                    stations[sta]["num"] = 2

                stations[sta]["name"] = choose[0]
                stations[sta]["inst"] = choose[1]
        else:
            if num == 1:
                stations[sta]["iden"] = execute(stations[sta]["name"], stations[sta]["inst"])

                if sta == store:
                    stations[sta]["num"] = -1
                    reset(stations[sta]["iden"][1])
                else:
                    stations[sta]["num"] = 0

                cur_inst_num = stations[sta]["inst"][4]
                states[cur_inst_num][1] = cycle
            elif num == 0:
                stations[sta]["num"] = -1
                inst = stations[sta]["iden"]
                update(inst)
                reset(inst[1])

                cur_inst_num = stations[sta]["inst"][4]
                states[cur_inst_num][2] = cycle
            else:
                stations[sta]["num"] -= 1

    cycle += 1
    return exeDone()


if __name__ == '__main__':
    # main()
    file_path = "./inst/test3.inst"
    with open(file_path) as f:
        insts = [line.strip() for line in f.readlines()]

    for x in range(4096):
        mem.set(x, x * 1.0)

    init(insts)

    while not step():
        if cycle % 10 == 0:
            print("load queue: ", getLoadQueue())
            print("store queue:", getStoreQueue())
            print("reser queue:", getReservation())
            print("states:", getStates())
            print()

        pass
    # print("states:", getStates())

    print("All registers:\n", getAllReg())
