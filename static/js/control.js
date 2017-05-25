$(document).ready(()=> {
    (() => {
        let data = [];
        for (let i = 0; i < 10; i++) {
            let obj = {};
            for (let j = 0; j < 16; ++j) {
                obj["0x" + j.toString(16)] = sprintf("%02x", i * 27 + j * 4 + 5);
            }
            obj["address"] = i;
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
        for (let i = 0; i <= 10; i++) {
            data.push({register: "R" + i.toString(), expression: "2 + 3", value: 5});
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

    $("#btnRun").click((e) => {
        alert(emulator.solarSystem.greet());
    });
});
