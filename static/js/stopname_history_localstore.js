function getStopNameHistory() {
    if(('localStorage' in window) && (window.localStorage !== null)) {
        str = localStorage.getItem("StopNameHistry");
        if (str !== undefined && str !== null && str != ""){
            return JSON.parse(str);
        }
    }
    return {"list":[]};
}

function addStopNameHistory(sid, name) {
    sn_history = getStopNameHistory();
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

$(function () {
    $(".stop-list.select-stop li a").on('click',function(){
        sid = $(this).closest("li.list-group-item").data("mbn-stop_id");
        name = $(this).closest("li.list-group-item").data("mbn-stop_name");
        addStopNameHistory(sid, name);
    });
    if ($("#stop_candidate").size()) {
        $("#stop_candidates").empty();
        his = getStopNameHistory();
        opt = $('<optgroup label="入力履歴">');
        $.each(his["list"],function(){
            opt.append($("<option/>").text(this["name"]));
        });
        $("#stop_candidate").append(opt);
    }
});
