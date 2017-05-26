$(document).ready(()=> {
    let currentPC = 0;
    let codeLines = [];
    let timerRun = null;
    let intRegs = [];
    const IntRegCount = 11;
    for (let i = 0; i < IntRegCount; ++i) {
        intRegs[i] = {register: "R" + i.toString(), expression: "3 + " + i.toString(), value: 3 + i};
    }

    (() => {
        let data = [];
        for (let i = 0; i < 10; i++) {
            let obj = {};
            for (let j = 0; j < 16; ++j) {
                obj["0x" + j.toString(16)] = sprintf("%02x", i * 27 + j * 4 + 5);
            }
            obj["address"] = "0x" + (i * 16).toString(16);
            data.push(obj);
        }
        let fields = [];
        fields.push({name: "address", type: "text", width: 62, editing: false});
        for (let i = 0; i < 16; i++) {
            fields.push({name: "0x" + i.toString(16), type: "text", width: 50, filtering: false})
        }
        $("#memoryEditor").jsGrid({
            width: '1000px',
            height: '400px',

            editing: true,
            sorting: true,

            data: data,

            fields: fields
        });
    })();
    (() => {
        let data = [];
        for (let i = 0; i <= 10; i++) {
            data.push({register: "F" + i.toString(), expression: "2 + 3", value: 5});
        }
        $("#tableFloatRegs").jsGrid({
            width: '400px',
            height: '520px',

            editing: true,
            sorting: true,
            paging: true,
            filtering: true,

            data: data,

            fields: [
                {name: "register", type: "text"},
                {name: "expression", type: "text"},
                {name: "value", type: "text"},
            ]
        });

    })();
    (() => {
        let data = [];
        for (let i = 0; i < IntRegCount; i++) {
            data.push(intRegs[i]);
        }
        $("#tableIntRegs").jsGrid({
            width: '400px',
            height: '520px',

            editing: true,
            sorting: true,
            paging: true,
            filtering: true,

            data: data,

            fields: [
                {name: "register", type: "text"},
                {name: "expression", type: "text"},
                {name: "value", type: "text"},
            ]
        });

    })();

    (() => {
        let data = [];
        for (let i = 0; i <= 10; i++) {
            data.push({
                name: "Inst" + i.toString(),
                busy: "True",
                address: i.toString(),
                cache: "123",
            });
        }
        $("#tableLoadQueue").jsGrid({
            width: '300px',
            height: '520px',

            editing: true,
            sorting: true,
            paging: true,
            filtering: true,

            data: data,

            fields: [
                {name: "name", type: "text"},
                {name: "busy", type: "text", width: 50},
                {name: "address", type: "text", width: 50},
                {name: "cache", type: "text"},
            ]
        });

    })();

    (() => {
        let data = [];
        for (let i = 0; i <= 10; i++) {
            data.push({
                name: "Inst" + i.toString(),
                busy: "True",
                address: i.toString(),
                cache: "123",
            });
        }
        $("#tableStoreQueue").jsGrid({
            width: '300px',
            height: '520px',

            editing: true,
            sorting: true,
            paging: true,
            filtering: true,

            data: data,

            fields: [
                {name: "name", type: "text"},
                {name: "busy", title: "Busy", type: "text", width: 50},
                {name: "address", "title": "Addr", type: "text", width: 50},
                {name: "cache", type: "text", width: 60},
            ]
        });

    })();

    (() => {
        let data = [];
        for (let i = 0; i <= 10; i++) {
            data.push({
                time: "time",
                name: "Inst" + i.toString(),
                busy: "True",
                op: "op",
            });
        }
        $("#tableReservationStations").jsGrid({
            width: '1000px',
            height: '520px',

            editing: true,
            sorting: true,
            paging: true,
            filtering: true,

            data: data,

            fields: [
                {name: "time", type: "text"},
                {name: "name", type: "text"},
                {name: "busy", title: "Busy", type: "text", width: 50},
                {name: "op", "title": "Op", type: "text", width: 50},
            ]
        });

    })();

    function setPC(pc) {
        currentPC = pc;
        emulator.emu.setPC(currentPC);
        $("#textCurrentPC").text("0x" + currentPC.toString(16));
        cm.setCursor({line: currentPC, ch: 0});
    }
    function step() {
        emulator.emu.step();
        currentPC++;
        $("#textCurrentPC").text("0x" + currentPC.toString(16));
        cm.setCursor({line: currentPC, ch: 0});
        syncData();
    }
    function run() {
        stop();
        syncData();
        timerRun = setInterval(() => {
            if (currentPC < codeLines.length) {
                step();
            }
            else {
                stop();
            }
        }, 200);
    }
    function stop() {
        if (timerRun !== null) {
            clearInterval(timerRun);
        }
    }
    function syncIntRegisters() {
        const tb = $("#tableIntRegs");
        for (let i = 0; i <= 10; i++) {
            let {expression: exp, value: val} = emulator.emu.getReg("R", i);

            const name = "R" + i.toString();
            const line = {register: name, expression: exp, value: val};

            const rowJq = tb.jsGrid("rowByItem", intRegs[i]);
            tb.jsGrid("updateItem", rowJq, line)
        }
        // tb.jsGrid("refresh");
    }
    function syncData() {
        syncIntRegisters();
    }

    $("#btnLoad").click((e) => {
        const lines = cm.getValue().split("\n");
        const code = lines.map((line) => {
            line.replace(",", "").split(" ");
        });
        codeLines = code;
        emulator.emu.loadCode(code);
        setPC(0);
    });
    $("#btnStep").click((e) => {
        step();
    });
    $("#btnRun").click((e) => {
        run();
    });
    $("#btnStop").click((e) => {
        stop();
    })
});
