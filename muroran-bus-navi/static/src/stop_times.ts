"use strict";
import "modaal";
import "modaal/dist/css/modaal.min.css";
// import * as $ from 'jquery';

$(function(){
    const get_params = (location.href).split("?", 2);
    const params     = get_params.length == 2?get_params[1].split("&"):[];

    let paramArray = [];
    for (let i = 0; i < params.length; i++ ) {
        const kv = params[i].split("=");
        paramArray[kv[0]] = kv[1];
    }

    if (paramArray["f_id"]) {
        $('input[name="f_id"]').val(paramArray["f_id"]);
    }
    if (paramArray["t_id"]) {
        $('input[name="t_id"]').val(paramArray["t_id"]);
    }

    $('input[name="from_q"]').change(function() {
        $('input[name="f_id"]').val("");
    });
    $('input[name="to_q"]').change(function() {
        $('input[name="t_id"]').val("");
    });
    (<any>$('.stop-list .modaal-ajax')).modaal({
      type: 'ajax',
      loading_content: 'Loading content, please wait.'
    });
});
