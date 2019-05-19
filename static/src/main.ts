"use strict";
import "bootstrap-rin";
import "./index.scss";
import * as $ from 'jquery';
import { Feedback } from '@ivoviz/feedback.js';

import { getStopNameHistory, addStopNameHistory } from "./stopname_history_localstore"

const feedback = new Feedback({
  footnote: 'あなたのフィードバック、追加情報が送られます。プライバシーポリシーと利用規約をご覧ください。',
  endpoint: '/feedback/'
});
$(document).ready(function() {
  $("body").append('<button class="btn btn-primary feedback-btn fixed">Feedback を送る</button>');
  $(".feedback-btn").click(function(){
    feedback.open();
  });
});


$(function () {
    $(".stop-list.select-stop li a").on('click',function(){
        const sid = $(this).closest("li.list-group-item").data("mbn-stop_id");
        const name = $(this).closest("li.list-group-item").data("mbn-stop_name");
        addStopNameHistory(sid, name);
    });
    // if ($("#stop_candidate").size()) {
    if ($("#stop_candidate")) {
        $("#stop_candidates").empty();
        const his = getStopNameHistory();
        const opt = $('<optgroup label="入力履歴">');
        $.each(his["list"],function(){
            opt.append($("<option/>").text(this["name"]));
        });
        $("#stop_candidate").append(opt);
    }
});
