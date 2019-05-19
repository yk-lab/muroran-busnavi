import * as $ from 'jquery';

export function getStopNameHistory() {
    if(('localStorage' in window) && (window.localStorage !== null)) {
        const str = localStorage.getItem("StopNameHistry");
        if (str !== undefined && str !== null && str !== ""){
            return JSON.parse(str);
        }
    }
    return {"list":[]};
}

export function addStopNameHistory(sid, name) {
    var sn_history = getStopNameHistory();
    if (sid in sn_history && sn_history[sid] > 0) {
        sn_history["list"].splice(sn_history[sid] - 1, 1);
    }
    sn_history["list"].unshift({"sid": sid, "name": name});
    sn_history = {"list": sn_history["list"].splice(0, 10)};
    for (var index in sn_history["list"]) {
        sn_history[sn_history["list"][index]["sid"]] = Number(index) + 1;
    }
    if(('localStorage' in window) && (window.localStorage !== null)) {
        localStorage.setItem("StopNameHistry", JSON.stringify(sn_history));
    }
    return sn_history;
}
