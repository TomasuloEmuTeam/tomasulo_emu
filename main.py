from mem import Mem
from register import Reg
from station import *

from queue import Queue

load  = Station("ld", 3)
store = Station("st", 3)
adder = Station("add", 3)
mult  = Station("mult", 2)

# cycle number
cycle = 0

# current instruction num
inst_num = 0

# instruction list
instructions = []

# station states
stations = {}

# operation states
states   = []

def init(inst_list):
    """init all global var"""

    def setInst(inst_list):
        """set instruction lists"""
        global instructions

        instructions = inst_list[:]

    def initStation():
        """init station states"""
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
    """states layout:
    [
        [launch_num, exec_num, writeback_num],
        ...
    ]

    eg.
    [
        [0, 2, 3],
        [1, 6, 7], 
        ...
        [8, None, None]
    ]
    """
    return states

def setAllMem(data):
    """data format:
    [val_0, val_1, ..., val_4095]
    """
    mem.setAll(data)

def getAllMem():
    """Mem data format:
    [val_0, val_1, ..., val_4095]
    """
    return mem.getAll()

def getAllReg():
    """reg data format:
    [
        [V, Q],
        ...
    ]

    eg.
    [
        [1.0, None],
        [None, "ld2"],
        ...
        [0.0, None]
    ]
    """
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
    """load queue data format:
    [
        [name, busy(Y/N), reg_num, mem_addr],
        ...
    ]

    eg.
    [
        ['ld0', 'N', None, None],
        ['ld1', 'Y', 1, 2],
        ['ld2', 'Y', 2, 5]
    ]
    """
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
    """store queue data format:
    [
        [name, busy(Y/N), reg_val, reg_iden, mem_addr],
        ...
    ]

    eg.
    [
        ['st0', 'Y', 'ld1', None, 9],
        ['st1', 'Y', 'ld2', None, 8],
        ['st2', 'N', None, None, None]
    ]
    """
    store_vect = store.getAll()
    ret = []
    for (name, inst) in store_vect.items():
        item = [name]
        if inst[0] == -1:
            item += ["N", None, None, None]
        else:
            item.append("Y")
            if type(inst[0]) == str:
                item += [inst[0], None]
            else:
                item += [None, inst[0]]
            item.append(inst[1])

        ret.append(item)

    return ret

def getReservation():
    """reservation queue data format:
    [
        [name, busy(Y/N), Op, Vi, Qi, Vj, Qj],
        ...
    ]

    eg.
    [
        ['add0', 'Y', 2, 1.0, None, 2.0, None],
        ['add1', 'N', None, None, None, None, None],
        ['add2', 'N', None, None, None, None, None],
        ['mult0', 'Y', 3, -1.0, None, 2.0, None],
        ['mult1', 'Y', 4, None, 'mult0', -1.0, None]]
    ]
    """
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
            item.append(inst[0])
            for i in range(1, 3):
                if type(inst[i]) == str:
                    item += [None, inst[i]]
                else:
                    item += [inst[i], None]

        ret.append(item)

    return ret

def step():
    """step & return whether execute done or not"""

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
            if not sta.empty():
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
                if sta == load or sta == store:
                    mem_addr = choose[1][1]
                    cur_inst_num = choose[1][4]
                    if load.checkMem(mem_addr, cur_inst_num) and store.checkMem(mem_addr, cur_inst_num):
                        pass
                    else:
                        continue

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

    # for x in range(4096):
        # mem.set(x, x * 1.0)
    setAllMem([x * 1.0 for x in range(4096)])

    init(insts)

    while not step():
        if cycle % 10 == 0:
            print("Cycle %d"%(cycle))
            # print("load queue: ", getLoadQueue())
            # print("store queue:", getStoreQueue())
            # print("reser queue:", getReservation())
            # print("states:", getStates())
            print("Reg", getAllReg())
            print()

        pass

    print("\nStates:", getStates())
    print("\nAll registers:\n", getAllReg())
