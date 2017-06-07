from mem import mem
from register import reg
from station import *

from queue import Queue

load  = Station("ld", 3)
store = Station("st", 3)
adder = Station("add", 3)
mult  = Station("mult", 2)

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

def update(reg_addr, name, value):
    reg.update(reg_addr, value)
    for sta in stations:
        sta.update(name, value)

def execute(name, inst):
    print("exec", name, inst)
    if name[:-1] == "ld":
        update(inst[0], name, mem.get(inst[1]))
        load.reset(name)
    elif name[:-1] == "st":
        # update(inst[0], name, reg.get(inst[0]))
        mem.set(inst[1], inst[0])
        store.reset(name)
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
            update(inst[0], name, value)
            adder.reset(name)
        elif name[:-1] == "mult":
            if inst[3]:
                # mult
                value = reg_val1 * reg_val2
            else:
                # div
                value = reg_val1 / reg_val2
            update(inst[0], name, value)
            mult.reset(name)


def main():

    inst_queue = Queue()
    file_path = "./inst/test3.inst"
    with open(file_path) as f:
        for line in f.readlines():
            inst_queue.put(line.strip())

    # mem.set(0x30, 1.0)
    # mem.set(0x77, 3.0)

    # mem.set(0x34, 3.0)
    # mem.set(0x45, 5.0)
    for x in range(4096):
        mem.set(x, x * 1.0)

    def exeDone():
        # for sta in stations:
        #     if stations[sta]["num"] != -1:
        #         return False
        return reg.checkAll()

    # for instruct in instructions:
    while not inst_queue.empty() or not exeDone():
        if not inst_queue.empty():
            instruct = inst_queue.get()
            s = instruct.split(" ")

            print("instruct:", instruct)

            flag = None
            if s[0] == "LD":
                flag = load.add(int(s[1][1:]), int(s[2], 16), "load")
            elif s[0] == "ST":
                flag = store.add(int(s[1][1:]), int(s[2], 16), "store")
            elif s[0] == "ADDD":
                flag = adder.add(int(s[1][1:]), int(s[2][1:]), int(s[3][1:]))
            elif s[0] == "SUBD":
                flag = adder.add(int(s[1][1:]), int(s[2][1:]), int(s[3][1:]), False)
            elif s[0] == "MULD":
                flag = mult.add(int(s[1][1:]), int(s[2][1:]), int(s[3][1:]))
            elif s[0] == "DIVD":
                flag = mult.add(int(s[1][1:]), int(s[2][1:]), int(s[3][1:]), False)
            else:
                print("wrong instruction: (%s)!!!"%instruct)
                return False

            if not flag:
                inst_queue.put(instruct)

        # choose instructions to execute
        for sta in stations:
            num = stations[sta]["num"]
            if num == -1:
                choose = sta.choose()
                if choose[0] != False:
                    print("choose", choose)
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
                    stations[sta]["num"] = -1
                    execute(stations[sta]["name"], stations[sta]["inst"])
                    # update all identifiers
                else:
                    stations[sta]["num"] -= 1

    reg.print()

if __name__ == '__main__':
    main()
