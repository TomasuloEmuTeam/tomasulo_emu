module.exports = function () {
    $.ajaxSetup({
        contentType: "application/json; charset=utf-8"
    });
    return {
        init: (code, cb) => {
            $.ajax({
                type: "POST",
                url: 'http://localhost:5000/init',
                dataType: 'json',
                data: JSON.stringify({data: code}),
                success: function (data) {
                    if (cb) cb(data);
                    console.log(data)
                },
            });
        },
        setAllMem: (mem, cb) => {
            $.ajax({
                type: "POST",
                url: 'http://localhost:5000/setAllMem',
                dataType: 'json',
                data: JSON.stringify({data: mem}),
                success: function (data) {
                    cb(data)
                },
            });
        },
        step: (cb) => {
            $.ajax({
                type: "POST",
                url: 'http://localhost:5000/step',
                dataType: 'json',
                success: function (data) {
                    cb(data);
                    console.log(JSON.stringify(data))
                },
            });
        },
        getAllReg: (cb) => {
            $.ajax({
                type: "GET",
                url: 'http://localhost:5000/getAllReg',
                dataType: 'json',
                success: function (data) {
                    cb(data);
                },
            });
        },
        getAllMem: (cb) => {
            $.ajax({
                type: "GET",
                url: 'http://localhost:5000/getAllMem',
                dataType: 'json',
                success: function (data) {
                    cb(data);
                },
            });
        },
        getLoadQueue: (cb) => {
            $.ajax({
                type: "GET",
                url: 'http://localhost:5000/getLoadQueue',
                dataType: 'json',
                success: function (data) {
                    cb(data);
                },
            });
        },
        getStoreQueue: (cb) => {
            $.ajax({
                type: "GET",
                url: 'http://localhost:5000/getStoreQueue',
                dataType: 'json',
                success: function (data) {
                    cb(data);
                },
            });
        },
        getReservationStation: (cb) => {
            $.ajax({
                type: "GET",
                url: 'http://localhost:5000/getReservation',
                dataType: 'json',
                success: function (data) {
                    cb(data);
                },
            });
        },
        getStates: (cb) => {
            $.ajax({
                type: "GET",
                url: 'http://localhost:5000/getStates',
                dataType: 'json',
                success: function (data) {
                    cb(data);
                },
            });
        },
    };
}