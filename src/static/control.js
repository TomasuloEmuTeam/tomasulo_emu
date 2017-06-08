const jQuery = require("jquery");
const $ = jQuery;
require("jsgrid");
const CodeMirror = require("codemirror");
const sprintf = require("sprintf-js").sprintf;
const getEmuApi = require('./emu');
const toastr = require('toastr');
toastr.options.timeOut = 2500; // How long the toast will display without user interaction
toastr.options.extendedTimeOut = 10000; // How long the toast will display after a user hovers over it

$(document).ready(()=> {
    // Code Mirror
    cm = CodeMirror.fromTextArea(document.getElementById("textInstructions"), {
        lineNumbers: true,
        matchBrackets: true,
        styleActiveLine: true,
        gutters: ["CodeMirror-linenumber", "breakpoints"],

    });
    cm.on("gutterClick", function(cm, n) {
        let info = cm.lineInfo(n);
        cm.setGutterMarker(n, "breakpoints", info.gutterMarkers ? null : makeMarker());
    });

    toastr.warning("Please wait for the server to be alive");
    const timer = setInterval(() => {
        $.get("http://localhost:5000/ping", (status) => {
            toastr.success("Server alive!");
            $("#btnLoad").prop('disabled', false);
            clearInterval(timer);
        })

    }, 300);

    function makeMarker() {
        let marker = document.createElement("div");
        marker.style.color = "#822";
        marker.innerHTML = "●";
        return marker;
    }

    let currentPC = 0;
    let timerRun = null;
    const emu = getEmuApi();

    (() => {
        let data = [];
        let fields = [];
        fields.push({name: "address", title: "Addr", type: "text", width: 30, editing: false});
        for (let i = 0; i < 16; i++) {
            fields.push({name: "0x" + i.toString(16), type: "text", width: 20, filtering: false})
        }
        fields.push({"type": "control", width: 30});
        $("#memoryEditor").jsGrid({
            width: '930px',
            height: '350px',

            editing: true,
            sorting: true,

            data: data,

            fields: fields,
            onItemUpdated: function(args) {
                const d = args.grid.data;
                let data = [];
                for (const item of d) {
                    for (let i = 0; i < 16; ++i) {
                        const val = parseInt(item["0x" + i.toString(16)], 16);
                        data.push(val);
                    }
                }
                emu.setAllMem(data, (_data) => {});
            }
        });
    })();
    (() => {
        let data = [];
        $("#runningStatus").jsGrid({
            width: '300px',
            height: '315px',

            editing: true,
            sorting: true,

            data: data,

            fields: [
                {name: "line", title: "Line", type: "text", width: 40, editing: false},
                {name: "emit", title: "Emit", type: "text", width: 62, editing: false},
                {name: "done", title: "Done", type: "text", width: 62, editing: false},
                {name: "writeBack", title: "Wb", type: "text", width: 62, editing: false},
            ]
        });
    })();
    (() => {
        let data = [];
        $("#tableFloatRegs").jsGrid({
            width: '400px',
            height: '350px',

            sorting: true,
            paging: true,

            data: data,

            fields: [
                {name: "register", type: "text"},
                {name: "value", type: "text"},
                {name: "pointer", type: "text"},
            ]
        });

    })();
    (() => {
        let data = [];
        $("#tableLoadQueue").jsGrid({
            width: '300px',
            height: '350px',

            sorting: true,
            paging: true,

            data: data,

            fields: [
                {name: "name", title: "Name", type: "text", width: 50},
                {name: "busy", title: "Busy", type: "text", width: 50},
                {name: "memoryAddress", title: "Mem", type: "text", width: 50},
                {name: "register", title: "Reg", type: "text"},
            ]
        });

    })();
    (() => {
        let data = [];
        $("#tableStoreQueue").jsGrid({
            width: '300px',
            height: '350px',

            sorting: true,
            paging: true,

            data: data,

            fields: [
                {name: "name", title: "Name", type: "text", width: 50},
                {name: "busy", title: "Busy", type: "text", width: 50},
                {name: "memoryAddress", title: "Mem", type: "text", width: 50},
                {name: "register", title: "Reg", type: "text"},
            ]
        });

    })();
    (() => {
        let data = [];
        $("#tableReservationStations").jsGrid({
            // width: '1000px',
            height: '400px',

            sorting: true,
            paging: true,

            data: data,

            fields: [
                {name: "name", title: "Name", type: "text", width: 100},
                {name: "busy", title: "Busy", type: "text", width: 100},
                {name: "op", "title": "Op", type: "text", width: 70},
                {name: "vi", "title": "Vi", type: "text", width: 70},
                {name: "vk", "title": "Vk", type: "text", width: 70},
                {name: "qj", "title": "Qj", type: "text", width: 70},
                {name: "qk", "title": "Qk", type: "text", width: 70},
            ]
        });

    })();

    function setPC(pc) {
        currentPC = pc;
        // emu.setPC(currentPC);
        $("#textCurrentPC").text("0x" + currentPC.toString(16));
        cm.setCursor({line: currentPC, ch: 0});
    }
    function step() {
        emu.step((data) => {
            const status = data.data[0];
            const line = data.data[1];

            if (status) {
                stop();
            }
            currentPC = line;
            $("#textCurrentPC").text("0x" + currentPC.toString(16));
            cm.setCursor({line: currentPC, ch: 0});
            syncData();
        });
    }
    function run() {
        stop();
        $("#btnRun").prop('disabled', true);
        syncData();
        timerRun = setInterval(() => {
            step();
        }, 100);
        toastr.success("Emulator running");
    }
    function stop() {
        $("#btnRun").prop('disabled', false);
        if (timerRun !== null) {
            clearInterval(timerRun);
        }
    }
    function syncFloatRegs() {
        const tb = $("#tableFloatRegs");
        emu.getAllReg((_data) => {
            const regs = _data['data'];
            let data = [];
            for (let i = 0; i <= 10; i++) {
                let [v, p] = regs[i];
                const line = {register: "F" + i.toString(), value: v, pointer: p};
                data.push(line);
            }
            tb.jsGrid({data: data});
        });
    }
    function syncMem() {
        const tb = $("#memoryEditor");
        emu.getAllMem((_data) => {
            const mem = _data['data'];
            let data = [];
            for (let i = 0; i < 256; i++) {
                let obj = {};
                for (let j = 0; j < 16; ++j) {
                    const addr = i * 16 + j;
                    const val = mem[addr];
                    obj["0x" + j.toString(16)] = sprintf("%02x", val);
                }
                obj["address"] = "0x" + (i * 16).toString(16);
                obj["_address"] = i * 16;
                obj["_data"] = mem.slice(i * 16, (i+1) * 16);
                data.push(obj);
            }
            tb.jsGrid({data: data});

        });
    }
    function syncLoadQueue() {
        const tb = $("#tableLoadQueue");
        emu.getLoadQueue((_data) => {
            let data = _data.data.map((item) => {
                return {"name": item[0], "busy": item[1], "memoryAddress": item[2], "register": item[3]}
            });
            tb.jsGrid({data: data});
        });
    }
    function syncStoreQueue() {
        const tb = $("#tableStoreQueue");
        emu.getStoreQueue((_data) => {
            let data = _data.data.map((item) => {
                return {"name": item[0], "busy": item[1], "memoryAddress": item[2], "register": item[3]}
            });
            tb.jsGrid({data: data});
        });
    }
    function syncReservationStations() {
        const tb = $("#tableReservationStations");
        emu.getReservationStation((_data) => {
            let data = _data.data.map((item) => {
                return {name: item[0], busy: item[1], op: item[2], vi: item[3], vk: item[4], qj: item[5], qk: item[6]}
            });
            tb.jsGrid({data: data});
        });
    }
    function syncRunningStatus() {
        const tb = $("#runningStatus");
        emu.getStates((_data) => {
            let data = [];
            for (let i = 0; i < _data.data.length; ++i) {
                const item = _data.data[i];
                data.push({line: i, emit: item[0], done: item[1], writeBack: item[2]})
            }
            tb.jsGrid({data: data});
        });
    }
    function syncData() {
        syncFloatRegs();
        syncMem();
        syncLoadQueue();
        syncStoreQueue();
        syncReservationStations();
        syncRunningStatus();
    }

    $("#btnLoad").click((e) => {
        const lines = cm.getValue().split("\n");
        emu.init(lines);
        setPC(0);
        let a = [];
        for (let i = 0; i < 4096; ++i) {
            a[i] = i % 256;
        }
        emu.setAllMem(a, (data) => {});
        $("#btnRun").prop("disabled", false);
        $("#btnStop").prop("disabled", false);
        $("#btnStep").prop("disabled", false);
        toastr.success("Code sucessfully loaded into memory!");
        syncData();
    });
    $("#btnStep").click((e) => {
        step();
    });
    $("#btnRun").click((e) => {
        run();
    });
    $("#btnStop").click((e) => {
        stop();
        toastr.success("Emulator stopped");
    })
});

